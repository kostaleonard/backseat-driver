"""Tests backseat_driver.py."""

import os
from tempfile import TemporaryDirectory
import pytest
from backseat_driver import backseat_driver


@pytest.fixture(name="flat_source_directory")
def fixture_flat_source_directory() -> str:
    """Returns the path to a flat temporary directory containing files.

    The content of each file is the filename.
    """
    with TemporaryDirectory() as temp_dir:
        for filename in {"test1.txt", "test2.txt", "test3.py"}:
            with open(
                os.path.join(temp_dir, filename), "w", encoding="utf-8"
            ) as outfile:
                outfile.write(filename)
        yield temp_dir


@pytest.fixture(name="nested_source_directory")
def fixture_nested_source_directory(flat_source_directory) -> str:
    """Returns the path to a nested temporary directory containing files.

    The content of each file is the filename.
    """
    dir1 = os.path.join(flat_source_directory, "dir1")
    dir2 = os.path.join(flat_source_directory, "dir2")
    dir3 = os.path.join(dir2, "dir3")
    for directory in [dir1, dir2, dir3]:
        os.mkdir(directory)
        with open(os.path.join(directory, "dir.txt"), "w", encoding="utf-8") as outfile:
            outfile.write(directory)
    yield flat_source_directory


def test_get_source_filenames_finds_files_in_flat_directory(
    flat_source_directory,
) -> None:
    """Tests that get_source_filenames finds all files in a flat directory."""
    source_filenames = backseat_driver.get_source_filenames(flat_source_directory)
    assert source_filenames == {
        os.path.join(flat_source_directory, "test1.txt"),
        os.path.join(flat_source_directory, "test2.txt"),
        os.path.join(flat_source_directory, "test3.py"),
    }


def test_get_source_filenames_finds_files_in_nested_directory(
    nested_source_directory,
) -> None:
    """Tests that get_source_filenames finds all files in a nested
    directory."""
    source_filenames = backseat_driver.get_source_filenames(nested_source_directory)
    assert source_filenames == {
        os.path.join(nested_source_directory, "test1.txt"),
        os.path.join(nested_source_directory, "test2.txt"),
        os.path.join(nested_source_directory, "test3.py"),
        os.path.join(nested_source_directory, "dir1", "dir.txt"),
        os.path.join(nested_source_directory, "dir2", "dir.txt"),
        os.path.join(nested_source_directory, "dir2", "dir3", "dir.txt"),
    }


def test_get_source_filenames_filters_files_by_suffix(flat_source_directory) -> None:
    """Tests that get_source_filenames filters files by their suffix."""
    source_filenames = backseat_driver.get_source_filenames(
        flat_source_directory, filter_files_by_suffix=".py"
    )
    assert source_filenames == {
        os.path.join(flat_source_directory, "test3.py"),
    }
    source_filenames = backseat_driver.get_source_filenames(
        flat_source_directory, filter_files_by_suffix=".txt"
    )
    assert source_filenames == {
        os.path.join(flat_source_directory, "test1.txt"),
        os.path.join(flat_source_directory, "test2.txt"),
    }


def test_get_args_returns_namespace_containing_args() -> None:
    """Tests that get_args returns a namespace containing the command line
    arguments."""
    args = backseat_driver.get_args(
        ["--openai_api_key=123", "--fail_under=B", "--filter_files_by_suffix=.py"]
    )
    assert args.source_directory == "."
    assert args.filter_files_by_suffix == ".py"
    assert args.fail_under == "B"
    assert args.openai_api_key == "123"


def test_get_args_raises_error_when_fail_under_invalid() -> None:
    """Tests that get_args raises an error when fail_under is not a letter
    grade."""
    with pytest.raises(SystemExit):
        _ = backseat_driver.get_args(["--openai_api_key=123", "--fail_under=Q"])


def test_get_args_raises_error_when_openai_api_key_unspecified() -> None:
    """Tests that get_args raises an error when openai_api_key is
    unspecified."""
    with pytest.raises(SystemExit):
        _ = backseat_driver.get_args([])
