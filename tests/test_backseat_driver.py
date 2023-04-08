"""Tests backseat_driver.py."""

import json
import os
from tempfile import TemporaryDirectory
from unittest import mock
import pytest
from backseat_driver import backseat_driver

SAMPLE_SOURCE_FILE = os.path.join("tests", "fixtures", "sample_source_file.py")


@pytest.fixture(name="flat_source_directory")
def fixture_flat_source_directory() -> str:
    """Returns the path to a flat temporary directory containing files.

    The content of each file is the filename.
    """
    with TemporaryDirectory() as temp_dir:
        for filename in "test1.txt", "test2.txt", "test3.py":
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
            outfile.write("dir.txt")
    yield flat_source_directory


@pytest.fixture(name="sample_source_contents")
def fixture_sample_source_contents() -> str:
    """Returns the contents of the sample source file."""
    with open(SAMPLE_SOURCE_FILE, "r", encoding="utf-8") as infile:
        return infile.read()


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


def test_get_source_contents_reads_contents(nested_source_directory) -> None:
    """Tests that get_source_contents reads the file contents."""
    source_filenames = backseat_driver.get_source_filenames(nested_source_directory)
    sorted_filenames = sorted(source_filenames)
    sorted_contents = backseat_driver.get_source_contents(sorted_filenames)
    assert sorted_contents == [
        "dir.txt",
        "dir.txt",
        "dir.txt",
        "test1.txt",
        "test2.txt",
        "test3.py",
    ]


def test_get_prompt_uses_source_contents(sample_source_contents) -> None:
    """Tests that get_prompt returns a prompt containing some data that appears
    in the source files."""
    prompt = backseat_driver.get_prompt([sample_source_contents])
    assert "fib" in prompt or "fact" in prompt or "hailstone" in prompt


def test_get_prompt_uses_multiple_source_contents(sample_source_contents) -> None:
    """Tests that get_prompt returns a prompt based on multiple source
    files."""
    prompt = backseat_driver.get_prompt(
        [sample_source_contents, sample_source_contents]
    )
    assert prompt.count("factorial") == 2


def test_get_prompt_returns_prompt_shorter_than_max_length(
    sample_source_contents,
) -> None:
    """Tests that get_prompt returns a prompt shorter than the max length, if
    it is provided."""
    max_length = 420
    prompt = backseat_driver.get_prompt([sample_source_contents], max_length=max_length)
    assert "fib" in prompt
    assert len(prompt) <= max_length


def test_get_prompt_splits_too_long_contents_on_newline(sample_source_contents) -> None:
    """Tests that get_prompt splits contents that exceed the max length on a
    newline character."""
    max_length = 425
    prompt = backseat_driver.get_prompt([sample_source_contents], max_length=max_length)
    sample_source_contents_lines = sample_source_contents.split("\n")
    for line in prompt.split("\n"):
        if line in sample_source_contents:
            assert line in sample_source_contents_lines


def _get_sample_model_prediction() -> str:
    """Returns the sample model prediction."""
    with open(
        os.path.join("tests", "fixtures", "sample_model_prediction.json"),
        "r",
        encoding="utf-8",
    ) as infile:
        return json.loads(infile.read())


def test_get_model_prediction_returns_response_json(sample_source_contents) -> None:
    """Tests that get_model_prediction returns the model's response JSON."""
    prompt = backseat_driver.get_prompt([sample_source_contents])
    with mock.patch(
        "openai.ChatCompletion.create", return_value=_get_sample_model_prediction()
    ):
        response = backseat_driver.get_model_prediction(prompt)
    assert response["choices"][0]["message"]["content"].startswith("Grade:")


def test_get_args_returns_namespace_containing_args() -> None:
    """Tests that get_args returns a namespace containing the command line
    arguments."""
    args = backseat_driver.get_args(["--fail_under=B", "--filter_files_by_suffix=.py"])
    assert args.source_directory == "."
    assert args.filter_files_by_suffix == ".py"
    assert args.fail_under == "B"


def test_get_args_raises_error_when_fail_under_invalid() -> None:
    """Tests that get_args raises an error when fail_under is not a letter
    grade."""
    with pytest.raises(SystemExit):
        _ = backseat_driver.get_args(["--fail_under=Q"])
