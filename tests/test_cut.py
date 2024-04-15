import subprocess

import pytest
from click.testing import CliRunner

from app.cli.commands import cut

TSV_FILE = "tests/resources/books1.tsv"
CSV_FILE = "tests/resources/books2.csv"
ALT_CSV_FILE = "tests/resources/books3.csv"
NON_EXISTENT_FILE = "test/resources/bazz.yaml"

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

    # error messages
    ## no options
    assert (
        runner.invoke(cut, [TSV_FILE]).exception.args[0]
        == "cut: you must specify a list of bytes, characters, or fields"
    )

    ## invalid options
    assert (
        runner.invoke(cut, ["-c1", "-b1,", TSV_FILE]).exception.args[0]
        == "cut: only one type of list may be specified"
    )
    assert (
        runner.invoke(cut, ["-c1", "-d,", TSV_FILE]).exception.args[0]
        == "cut: an input delimiter may be specified only when operating on fields"
    )
    assert (
        runner.invoke(cut, ["-f1", "-d_#_", TSV_FILE]).exception.args[0]
        == "cut: the delimiter must be a single character"
    )
    assert (
        runner.invoke(cut, ["-c1", "-s", TSV_FILE]).exception.args[0]
        == "cut: suppressing non-delimited lines makes sense only when operating on fields"
    )

    ## invalid ranges
    assert (
        runner.invoke(cut, ["-c1-x", TSV_FILE]).exception.args[0]
        == "cut: invalid option value '1-x'"
    )
    assert (
        runner.invoke(cut, ["-c-", TSV_FILE]).exception.args[0]
        == "cut: invalid range with no endpoint: -"
    )
    assert runner.invoke(cut, ["-c-1-", TSV_FILE]).exception.args[0] == "cut: invalid range"
    assert (
        runner.invoke(cut, ["-f2", NON_EXISTENT_FILE]).exception.args[0]
        == f"cut: {NON_EXISTENT_FILE}: No such file or directory"
    )


# def test_cut_file_list() -> None:
#     # single option
#     assert (
#         runner.invoke(cut, ["-b1-3", TSV_FILE, CSV_FILE]).output
#         == """pyt
#     sna
#     alp
#     rob
#     hor
#     don
#     ory
#     pyt
#     sna
#     alp
#     rob
#     hor
#     don
#     orn
#     Lor
#     """
#     )
#     assert (
#         runner.invoke(cut, ["-c2-8", TSV_FILE, CSV_FILE]).output
#         == """ython\tP
#     nail\tSS
#     lpaca\tI
#     obin\tMy
#     orse\tLi
#     onkey\tC
#     ryx\tWri
#     ython,P
#     nail,SS
#     lpaca,I
#     obin,My
#     orse,Li
#     onkey,C
#     rnyx,Wr
#     orem Ip
#     """
#     )

#     # combined options
#     assert (
#         runner.invoke(cut, ["-f1", "-d,", CSV_FILE, ALT_CSV_FILE]).output
#         == """python
#     snail
#     alpaca
#     robin
#     horse
#     donkey
#     ornyx
#     Lorem Ipsum et cetera res vana
#     English
#     French
#     Greek
#     That book you never really read...
#     Latin
#     """
#     )
#     assert (
#         runner.invoke(cut, ["-f1", "-d,", "-s", CSV_FILE, ALT_CSV_FILE]).output
#         == """python
#     snail
#     alpaca
#     robin
#     horse
#     donkey
#     ornyx
#     English
#     French
#     Greek
#     Latin
#     """
#     )
#     assert (
#         runner.invoke(cut, ["-f2-3", NON_EXISTENT_FILE, TSV_FILE]).output
#         == """cut: test/resources/bazz.yaml: No such file or directory
#     Programming Python\t2010
#     SSH, The Secure Shell\t2005
#     Intermediate Perl\t2012
#     MySQL High Availability\t2014
#     Linux in a Nutshell\t2009
#     Cisco IOS in a Nutshell\t2005
#     Writing Word Macros\t1999
#     """
#     )
