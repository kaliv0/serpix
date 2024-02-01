from click.testing import CliRunner

from app.cli.commands import head

LOG_FILE = "tests/resources/log.txt"
POEM_FILE = "tests/resources/poem.txt"
NON_EXISTENT_FILE = "test/resources/bazz.yaml"


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

    expected_c4 = "Hello world\nCiao ragazzi\nBon jour\nBratwu\n"
    assert runner.invoke(head, ["-c 40", LOG_FILE]).output == expected_c4


def test_wc_file_list() -> None:
    runner = CliRunner()
    # no options
    expected_multiple_no_opts = """==> tests/resources/log.txt <==
Hello world
Ciao ragazzi
Bon jour
Bratwurst
De lana caprina rixatur
Aien aristeuein

==> tests/resources/poem.txt <==
Good-night? ah! no; the hour is ill
Which severs those it should unite;
Let us remain together still,
Then it will be GOOD night.

How can I call the lone night good,
Though thy sweet wishes wing its flight?
Be it not said, thought, understood -
Then it will be - GOOD night.

"""
    assert runner.invoke(head, [LOG_FILE, POEM_FILE]).output == expected_multiple_no_opts

    # single option
    expected_multiple_n5 = """==> tests/resources/log.txt <==
Hello world
Ciao ragazzi
Bon jour
Bratwurst
De lana caprina rixatur

==> tests/resources/poem.txt <==
Good-night? ah! no; the hour is ill
Which severs those it should unite;
Let us remain together still,
Then it will be GOOD night.

"""
    assert runner.invoke(head, ["-n 5", LOG_FILE, POEM_FILE]).output == expected_multiple_n5

    # combined options
    expected_multiple_q_n6 = """Hello world
Ciao ragazzi
Bon jour
Bratwurst
De lana caprina rixatur
Aien aristeuein

Good-night? ah! no; the hour is ill
Which severs those it should unite;
Let us remain together still,
Then it will be GOOD night.

How can I call the lone night good,
"""
    assert runner.invoke(head, ["-q", "-n 6", LOG_FILE, POEM_FILE]).output == expected_multiple_q_n6

    # non-existent file
    expected_multiple_non_existent = f"""head: cannot open '{NON_EXISTENT_FILE}' for reading: No such file or directory
Good-night? ah! no; the hour is ill
Which severs those it should unite;
Let us remain together still,
Then it will be GOOD night.

How can I call the lone night good,
"""
    assert (
        runner.invoke(head, ["-q", "-n 6", NON_EXISTENT_FILE, POEM_FILE]).output
        == expected_multiple_non_existent
    )
