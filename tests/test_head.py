from click.testing import CliRunner

from app.cli.commands import head

LOG_FILE = "tests/resources/log.txt"
POEM_FILE = "tests/resources/poem.txt"


def test_head_single_file() -> None:
    runner = CliRunner()
    # no options
    expected_no_opts_1 = """Hello world
Ciao ragazzi
Bon jour
Bratwurst
De lana caprina rixatur
Aien aristeuein
"""

    expected_no_opts_2 = """Good-night? ah! no; the hour is ill
Which severs those it should unite;
Let us remain together still,
Then it will be GOOD night.

How can I call the lone night good,
Though thy sweet wishes wing its flight?
Be it not said, thought, understood -
Then it will be - GOOD night.

"""
    assert runner.invoke(head, [LOG_FILE]).output == expected_no_opts_1
    assert runner.invoke(head, [POEM_FILE]).output == expected_no_opts_2

    # single option
    expected_v_n3 = """==> tests/resources/log.txt <==
Hello world
Ciao ragazzi
Bon jour
"""

    expected_v_minus_n3 = """==> tests/resources/poem.txt <==
Good-night? ah! no; the hour is ill
Which severs those it should unite;
Let us remain together still,
Then it will be GOOD night.

How can I call the lone night good,
Though thy sweet wishes wing its flight?
Be it not said, thought, understood -
Then it will be - GOOD night.

To hearts which near each other move
"""
    assert runner.invoke(head, ["-v", "-n 3", LOG_FILE]).output == expected_v_n3
    assert runner.invoke(head, ["-v", "-n -3", POEM_FILE]).output == expected_v_minus_n3

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
