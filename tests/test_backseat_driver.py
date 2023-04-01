"""Tests backseat_driver.py."""

import pytest
from backseat_driver import backseat_driver


def test_get_args_returns_namespace_containing_args() -> None:
    """Tests that get_args returns a namespace containing the command line
    arguments."""
    args = backseat_driver.get_args(
        ["--openai_key=123", "--fail_under=B", "--filter_files_by_suffix=.py"]
    )
    assert args.source_directory == "."
    assert args.filter_files_by_suffix == ".py"
    assert args.fail_under == "B"
    assert args.openai_key == "123"


def test_get_args_raises_error_when_fail_under_invalid() -> None:
    """Tests that get_args raises an error when fail_under is not a letter
    grade."""
    with pytest.raises(SystemExit):
        _ = backseat_driver.get_args(["--openai_key=123", "--fail_under=Q"])


def test_get_args_raises_error_when_openai_key_unspecified() -> None:
    """Tests that get_args raises an error when openai_key is unspecified."""
    with pytest.raises(SystemExit):
        _ = backseat_driver.get_args([])
