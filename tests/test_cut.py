import subprocess

import pytest
from click.testing import CliRunner

from app.cli.commands import cut

TSV_FILE = "tests/resources/cut/books1.tsv"
CSV_FILE = "tests/resources/cut/books2.csv"
ALT_CSV_FILE = "tests/resources/cut/books3.csv"
NON_EXISTENT_FILE = "test/resources/cut/bazz.yaml"

runner = CliRunner()


@pytest.mark.parametrize("cut_option", ["-b1", "-b4-", "-b-3", "-b1-5"])
def test_cut_bytes(cut_option) -> None:
    assert (
        runner.invoke(cut, [cut_option, TSV_FILE]).output
        == subprocess.run(["cut", cut_option, TSV_FILE], capture_output=True, text=True).stdout
    )


@pytest.mark.parametrize("cut_option", ["-c1", "-c4-", "-c-3", "-c3-8"])
def test_cut_characters(cut_option) -> None:
    assert (
        runner.invoke(cut, [cut_option, TSV_FILE]).output
        == subprocess.run(["cut", cut_option, TSV_FILE], capture_output=True, text=True).stdout
    )


@pytest.mark.parametrize("cut_option", ["-f1", "-f2-", "-f-3", "-f2-4"])
def test_cut_fields(cut_option) -> None:
    assert (
        runner.invoke(cut, [cut_option, TSV_FILE]).output
        == subprocess.run(["cut", cut_option, TSV_FILE], capture_output=True, text=True).stdout
    )


@pytest.mark.parametrize(
    "cut_options",
    [("-f-3", "-d,"), ("-f-3", "-d,", "-s"), ("-f-3", "-d,", "-s", "--output-delimiter=' # '")],
)
def test_cut_fields_combined_options(cut_options) -> None:
    assert (
        runner.invoke(cut, [*cut_options, CSV_FILE]).output
        == subprocess.run(["cut", *cut_options, CSV_FILE], capture_output=True, text=True).stdout
    )


def test_cut_no_options_error() -> None:
    assert runner.invoke(cut, [TSV_FILE]).exception.args[0] == subprocess.run(
        ["cut", TSV_FILE], capture_output=True, text=True
    ).stderr.replace("\nTry 'cut --help' for more information.\n", "")


@pytest.mark.parametrize(
    "invalid_options", [("-c1", "-b1"), ("-c1", "-d"), ("-f1", "-d_#_"), ("-c1", "-s")]
)
def test_cut_invalid_options_error(invalid_options) -> None:
    # NB: error messages lack final redirection to '--help' option
    assert runner.invoke(cut, [*invalid_options, TSV_FILE]).exception.args[0] == subprocess.run(
        ["cut", *invalid_options, TSV_FILE], capture_output=True, text=True
    ).stderr.replace("\nTry 'cut --help' for more information.\n", "")


def test_cut_invalid_ranges_error() -> None:
    # NB: error messages differ from original
    assert (
        runner.invoke(cut, ["-c1-x", TSV_FILE]).exception.args[0]
        == "cut: invalid option value '1-x'"
    )
    assert (
        runner.invoke(cut, ["-c-", TSV_FILE]).exception.args[0]
        == "cut: invalid range with no endpoint: -"
    )
    assert runner.invoke(cut, ["-c-1-", TSV_FILE]).exception.args[0] == "cut: invalid range"


@pytest.mark.parametrize("cut_option", ["-b1-3", "-c2-8"])
def test_cut_file_list(cut_option) -> None:
    assert (
        runner.invoke(cut, [cut_option, TSV_FILE, CSV_FILE]).output
        == subprocess.run(
            ["cut", cut_option, TSV_FILE, CSV_FILE], capture_output=True, text=True
        ).stdout
    )


@pytest.mark.parametrize("cut_options", [("-f1", "-d,"), ("-f1", "-d,", "-s")])
def test_cut_file_list_combined_options(cut_options) -> None:
    assert (
        runner.invoke(cut, [*cut_options, CSV_FILE, ALT_CSV_FILE]).output
        == subprocess.run(
            ["cut", *cut_options, CSV_FILE, ALT_CSV_FILE], capture_output=True, text=True
        ).stdout
    )


def test_cut_nonexistent_file() -> None:
    assert runner.invoke(cut, ["-f2", NON_EXISTENT_FILE]).exception.args[0] == subprocess.run(
        ["cut", "-f2", NON_EXISTENT_FILE], capture_output=True, text=True
    ).stderr.rstrip("\n")

    # reads output from stdout and stderr
    assert (
        runner.invoke(cut, ["-f2-3", NON_EXISTENT_FILE, TSV_FILE]).output
        == subprocess.Popen(
            ["cut", "-f2-3", NON_EXISTENT_FILE, TSV_FILE],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        .communicate()[0]
        .decode()
    )
