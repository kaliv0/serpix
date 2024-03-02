from click.testing import CliRunner

from app.cli.commands import wc

LOG_FILE = "tests/resources/log.txt"
POEM_FILE = "tests/resources/poem.txt"
NON_EXISTENT_FILE = "test/resources/bazz.yaml"
TOTAL_SUFFIX = "total   "


def test_wc_single_file() -> None:
    runner = CliRunner()
    # no options
    assert runner.invoke(wc, [LOG_FILE]).output == f"       5       13       83 {LOG_FILE}\n"
    assert runner.invoke(wc, [POEM_FILE]).output == f"      13       77      414 {POEM_FILE}\n"
    # single option
    assert runner.invoke(wc, ["-c", LOG_FILE]).output == f"      83 {LOG_FILE}\n"
    assert runner.invoke(wc, ["-c", POEM_FILE]).output == f"     414 {POEM_FILE}\n"

    assert runner.invoke(wc, ["-l", LOG_FILE]).output == f"       5 {LOG_FILE}\n"
    assert runner.invoke(wc, ["-l", POEM_FILE]).output == f"      13 {POEM_FILE}\n"

    assert runner.invoke(wc, ["-w", LOG_FILE]).output == f"      13 {LOG_FILE}\n"
    assert runner.invoke(wc, ["-w", POEM_FILE]).output == f"      77 {POEM_FILE}\n"

    assert runner.invoke(wc, ["-m", LOG_FILE]).output == f"      83 {LOG_FILE}\n"
    assert runner.invoke(wc, ["-m", POEM_FILE]).output == f"     414 {POEM_FILE}\n"

    # combined options
    assert runner.invoke(wc, ["-cl", LOG_FILE]).output == f"       5       83 {LOG_FILE}\n"
    assert runner.invoke(wc, ["-cl", POEM_FILE]).output == f"      13      414 {POEM_FILE}\n"

    assert runner.invoke(wc, ["-wm", LOG_FILE]).output == f"      13       83 {LOG_FILE}\n"
    assert runner.invoke(wc, ["-wm", POEM_FILE]).output == f"      77      414 {POEM_FILE}\n"

    assert runner.invoke(wc, ["-cwl", LOG_FILE]).output == runner.invoke(wc, [LOG_FILE]).output
    assert runner.invoke(wc, ["-cwl", POEM_FILE]).output == runner.invoke(wc, [POEM_FILE]).output

    # non-existent file
    assert (
        runner.invoke(wc, NON_EXISTENT_FILE).exception.args[0]
        == f"wc: {NON_EXISTENT_FILE}: No such file or directory"
    )


def test_wc_file_list() -> None:
    runner = CliRunner()
    # no options
    assert runner.invoke(wc, [LOG_FILE, POEM_FILE]).output == (
        f"       5       13       83 {LOG_FILE}\n"
        f"      13       77      414 {POEM_FILE}\n"
        f"      18       90      497 {TOTAL_SUFFIX}\n"
    )

    # single option
    assert runner.invoke(wc, ["-c", LOG_FILE, POEM_FILE]).output == (
        f"      83 {LOG_FILE}\n" f"     414 {POEM_FILE}\n" f"     497 {TOTAL_SUFFIX}\n"
    )
    assert runner.invoke(wc, ["-l", LOG_FILE, POEM_FILE]).output == (
        f"       5 {LOG_FILE}\n" f"      13 {POEM_FILE}\n" f"      18 {TOTAL_SUFFIX}\n"
    )
    assert runner.invoke(wc, ["-w", LOG_FILE, POEM_FILE]).output == (
        f"      13 {LOG_FILE}\n" f"      77 {POEM_FILE}\n" f"      90 {TOTAL_SUFFIX}\n"
    )
    assert runner.invoke(wc, ["-m", LOG_FILE, POEM_FILE]).output == (
        f"      83 {LOG_FILE}\n" f"     414 {POEM_FILE}\n" f"     497 {TOTAL_SUFFIX}\n"
    )

    # combined options
    assert runner.invoke(wc, ["-cl", LOG_FILE, POEM_FILE]).output == (
        f"       5       83 {LOG_FILE}\n"
        f"      13      414 {POEM_FILE}\n"
        f"      18      497 {TOTAL_SUFFIX}\n"
    )
    assert runner.invoke(wc, ["-wm", LOG_FILE, POEM_FILE]).output == (
        f"      13       83 {LOG_FILE}\n"
        f"      77      414 {POEM_FILE}\n"
        f"      90      497 {TOTAL_SUFFIX}\n"
    )

    assert (
        runner.invoke(wc, ["-cwl", LOG_FILE, POEM_FILE]).output
        == runner.invoke(wc, [LOG_FILE, POEM_FILE]).output
    )

    # non-existent file
    assert runner.invoke(wc, [LOG_FILE, NON_EXISTENT_FILE]).output == (
        f"       5       13       83 {LOG_FILE}\n"
        f"wc: {NON_EXISTENT_FILE}: No such file or directory\n"
        f"       5       13       83 {TOTAL_SUFFIX}\n"
    )
