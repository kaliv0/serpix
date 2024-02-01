from click.testing import CliRunner


LOG_FILE = "tests/resources/log.txt"
BOOK_FILE = "tests/resources/book.txt"
NON_EXISTENT_FILE = "test/resources/bazz.yaml"


def test_head_single_file() -> None:
    runner = CliRunner()
    # no options
    # assert runner.invoke(head, [LOG_FILE]).output == f"       5       13       83 {LOG_FILE}\n"
    # assert runner.invoke(head, [BOOK_FILE]).output == f"    7145    58164   342190 {BOOK_FILE}\n"

    # # single option
    # assert runner.invoke(head, ["-c", LOG_FILE]).output == f"      83 {LOG_FILE}\n"
    # assert runner.invoke(head, ["-c", BOOK_FILE]).output == f"  342190 {BOOK_FILE}\n"

    # # combined options
    # assert runner.invoke(head, ["-cl", LOG_FILE]).output == f"       5       83 {LOG_FILE}\n"
    # assert runner.invoke(head, ["-cl", BOOK_FILE]).output == f"    7145   342190 {BOOK_FILE}\n"

    # # non-existent file
    # assert runner.invoke(head, [NON_EXISTENT_FILE]).output == (
    #     f"head: {NON_EXISTENT_FILE}: No such file or directory\n"
    # )


def test_wc_file_list() -> None:
    runner = CliRunner()
    # no options
    # assert runner.invoke(head, [LOG_FILE, BOOK_FILE]).output == (
    #     f"       5       13       83 {LOG_FILE}\n"
    #     f"    7145    58164   342190 {BOOK_FILE}\n"
    # )

    # # single option
    # assert runner.invoke(head, ["-c", LOG_FILE, BOOK_FILE]).output == (
    #     f"      83 {LOG_FILE}\n" f"  342190 {BOOK_FILE}\n" f"  342273 {TOTAL_SUFFIX}\n"
    # )

    # # combined options
    # assert runner.invoke(head, ["-cl", LOG_FILE, BOOK_FILE]).output == (
    #     f"       5       83 {LOG_FILE}\n"
    #     f"    7145   342190 {BOOK_FILE}\n"
    #     f"    7150   342273 {TOTAL_SUFFIX}\n"

    # # non-existent file
    # assert runner.invoke(head, [LOG_FILE, NON_EXISTENT_FILE]).output == (
    #     f"       5       13       83 {LOG_FILE}\n"
    #     f"head: {NON_EXISTENT_FILE}: No such file or directory\n"
    #     f"       5       13       83 {TOTAL_SUFFIX}\n"
    # )
