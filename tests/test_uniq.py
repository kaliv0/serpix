import subprocess

import pytest
from click.testing import CliRunner

from app.cli.commands import uniq

DUPLICATES_FILE = "tests/resources/uniq/duplicates.txt"
MINI_FILE = "tests/resources/uniq/mini_duplicates.txt"
FIRST_LETTERS_FILE = "tests/resources/uniq/first_letters.txt"
SKIP_LETTERS_FILE = "tests/resources/uniq/skip_letters.md"
IGNORE_CASE_FILE = "tests/resources/uniq/ignore_case.md"
NON_EXISTENT_FILE = "test/resources/uniq/bazz.yaml"
NON_EXISTENT_DIR = "test/resources/uniq/"


runner = CliRunner()


def test_uniq() -> None:
    assert (
        runner.invoke(uniq, [DUPLICATES_FILE]).output
        == subprocess.run(["uniq", DUPLICATES_FILE], capture_output=True, text=True).stdout
    )


@pytest.mark.parametrize(
    "uniq_option, file",
    [
        ("-c", DUPLICATES_FILE),
        ("-u", DUPLICATES_FILE),
        ("-d", DUPLICATES_FILE),
        ("-d", MINI_FILE),
        ("-D", DUPLICATES_FILE),
        ("-D", MINI_FILE),
        ("-i", IGNORE_CASE_FILE),
        ("-w3", FIRST_LETTERS_FILE),
        ("-w4", FIRST_LETTERS_FILE),
        ("-s3", SKIP_LETTERS_FILE),
    ],
)
def test_uniq_single_option(uniq_option, file) -> None:
    assert (
        runner.invoke(uniq, [uniq_option, file]).output
        == subprocess.run(["uniq", uniq_option, file], capture_output=True, text=True).stdout
    )


@pytest.mark.parametrize(
    "uniq_options, file",
    [
        ("-cd", DUPLICATES_FILE),
        ("-di", FIRST_LETTERS_FILE),
        ("-di", IGNORE_CASE_FILE),
        ("-Di", IGNORE_CASE_FILE),
    ],
)
def test_uniq_combined_options(uniq_options, file) -> None:
    assert (
        runner.invoke(uniq, [uniq_options, file]).output
        == subprocess.run(["uniq", uniq_options, file], capture_output=True, text=True).stdout
    )


@pytest.mark.parametrize("path", [NON_EXISTENT_FILE, NON_EXISTENT_FILE])
def test_uniq_non_existent(path) -> None:
    assert runner.invoke(uniq, path).exception.args[0] == subprocess.run(
        ["uniq", path], capture_output=True, text=True
    ).stderr.rstrip("\n")


@pytest.mark.parametrize("file, output", [(MINI_FILE, ("foo", "bar")), (MINI_FILE, ("."))])
def test_uniq_invalid_output(file, output) -> None:
    assert runner.invoke(uniq, [file, *output]).exception.args[0] == subprocess.run(
        ["uniq", file, *output], capture_output=True, text=True
    ).stderr.replace("\nTry 'uniq --help' for more information.", "").rstrip("\n")


@pytest.mark.parametrize(
    "invalid_options, error_message",
    [
        ("-cu", "uniq: printing all lines and repeat counts is meaningless"),
        ("-cD", "uniq: printing all lines and repeat counts is meaningless"),
        ("-ud", "uniq: meaningless flag combination"),
        ("-uD", "uniq: meaningless flag combination"),
        ("-w3 -s3", "uniq: unsupported flag combination"),
    ],
)
def test_uniq_invalid_options(invalid_options, error_message) -> None:
    assert runner.invoke(uniq, invalid_options, MINI_FILE).exception.args[0] == error_message
