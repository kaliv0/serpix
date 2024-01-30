from click.testing import CliRunner

from app.cli.commands import wc

LOG_FILE = "tests/resources/log.txt"
BOOK_FILE = "tests/resources/book.txt"
NON_EXISTENT_FILE = "test/resources/bazz.yaml"
TOTAL_SUFFIX = "total   "


def test_wc_single_file() -> None:
    runner = CliRunner()
    # no options
    assert (
        runner.invoke(wc, [LOG_FILE]).output
        == f"       6       13       84 {LOG_FILE}\n"
    )
    assert (
        runner.invoke(wc, [BOOK_FILE]).output
        == f"    7145    58164   342190 {BOOK_FILE}\n"
    )
    # single option
    assert runner.invoke(wc, ["-c", LOG_FILE]).output == f"      84 {LOG_FILE}\n"
    assert runner.invoke(wc, ["-c", BOOK_FILE]).output == f"  342190 {BOOK_FILE}\n"

    assert runner.invoke(wc, ["-l", LOG_FILE]).output == f"       6 {LOG_FILE}\n"
    assert runner.invoke(wc, ["-l", BOOK_FILE]).output == f"    7145 {BOOK_FILE}\n"

    assert runner.invoke(wc, ["-w", LOG_FILE]).output == f"      13 {LOG_FILE}\n"
    assert runner.invoke(wc, ["-w", BOOK_FILE]).output == f"   58164 {BOOK_FILE}\n"

    assert runner.invoke(wc, ["-m", LOG_FILE]).output == f"      84 {LOG_FILE}\n"
    assert runner.invoke(wc, ["-m", BOOK_FILE]).output == f"  339292 {BOOK_FILE}\n"

    # combined options
    assert (
        runner.invoke(wc, ["-cl", LOG_FILE]).output == f"       6       84 {LOG_FILE}\n"
    )
    assert (
        runner.invoke(wc, ["-cl", BOOK_FILE]).output
        == f"    7145   342190 {BOOK_FILE}\n"
    )

    assert (
        runner.invoke(wc, ["-wm", LOG_FILE]).output == f"      13       84 {LOG_FILE}\n"
    )
    assert (
        runner.invoke(wc, ["-wm", BOOK_FILE]).output
        == f"   58164   339292 {BOOK_FILE}\n"
    )

    assert (
        runner.invoke(wc, ["-cwl", LOG_FILE]).output
        == runner.invoke(wc, [LOG_FILE]).output
    )
    assert (
        runner.invoke(wc, ["-cwl", BOOK_FILE]).output
        == runner.invoke(wc, [BOOK_FILE]).output
    )

    # non-existent file
    assert runner.invoke(wc, [NON_EXISTENT_FILE]).output == (
        f"wc: {NON_EXISTENT_FILE}: No such file or directory\n"
    )


def test_wc_file_list() -> None:
    runner = CliRunner()
    # no options
    assert runner.invoke(wc, [LOG_FILE, BOOK_FILE]).output == (
        f"       6       13       84 {LOG_FILE}\n"
        f"    7145    58164   342190 {BOOK_FILE}\n"
        f"    7151    58177   342274 {TOTAL_SUFFIX}\n"
    )

    # single option
    assert runner.invoke(wc, ["-c", LOG_FILE, BOOK_FILE]).output == (
        f"      84 {LOG_FILE}\n" f"  342190 {BOOK_FILE}\n" f"  342274 {TOTAL_SUFFIX}\n"
    )
    assert runner.invoke(wc, ["-l", LOG_FILE, BOOK_FILE]).output == (
        f"       6 {LOG_FILE}\n" f"    7145 {BOOK_FILE}\n" f"    7151 {TOTAL_SUFFIX}\n"
    )
    assert runner.invoke(wc, ["-w", LOG_FILE, BOOK_FILE]).output == (
        f"      13 {LOG_FILE}\n" f"   58164 {BOOK_FILE}\n" f"   58177 {TOTAL_SUFFIX}\n"
    )
    assert runner.invoke(wc, ["-m", LOG_FILE, BOOK_FILE]).output == (
        f"      84 {LOG_FILE}\n" f"  339292 {BOOK_FILE}\n" f"  339376 {TOTAL_SUFFIX}\n"
    )

    # combined options
    assert runner.invoke(wc, ["-cl", LOG_FILE, BOOK_FILE]).output == (
        f"       6       84 {LOG_FILE}\n"
        f"    7145   342190 {BOOK_FILE}\n"
        f"    7151   342274 {TOTAL_SUFFIX}\n"
    )
    assert runner.invoke(wc, ["-wm", LOG_FILE, BOOK_FILE]).output == (
        f"      13       84 {LOG_FILE}\n"
        f"   58164   339292 {BOOK_FILE}\n"
        f"   58177   339376 {TOTAL_SUFFIX}\n"
    )

    assert (
        runner.invoke(wc, ["-cwl", LOG_FILE, BOOK_FILE]).output
        == runner.invoke(wc, [LOG_FILE, BOOK_FILE]).output
    )

    # non-existent file
    assert runner.invoke(wc, [LOG_FILE, NON_EXISTENT_FILE]).output == (
        f"       6       13       84 {LOG_FILE}\n"
        f"wc: {NON_EXISTENT_FILE}: No such file or directory\n"
        f"       6       13       84 {TOTAL_SUFFIX}\n"
    )
