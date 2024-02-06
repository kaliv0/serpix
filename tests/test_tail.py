from click.testing import CliRunner

from app.cli.commands import tail

LOG_FILE = "tests/resources/log.txt"
POEM_FILE = "tests/resources/poem.txt"
NON_EXISTENT_FILE = "test/resources/bazz.yaml"
DIR_PATH = "test/resources/"


def test_tail_single_file() -> None:
    runner = CliRunner()
    # no options
    expected_no_opts_1 = """Hello world
Ciao ragazzi
Bon jour
Bratwurst
De lana caprina rixatur
Aien aristeuein
"""

    expected_no_opts_2 = """
How can I call the lone night good,
Though thy sweet wishes wing its flight?
Be it not said, thought, understood -
Then it will be - GOOD night.

To hearts which near each other move
From evening close to morning light,
The night is good; because, my love,
They never SAY good-night.
"""
    assert runner.invoke(tail, [LOG_FILE]).output == expected_no_opts_1
    assert runner.invoke(tail, [POEM_FILE]).output == expected_no_opts_2

    # single option
    expected_v_n3 = """==> tests/resources/log.txt <==
Bratwurst
De lana caprina rixatur
Aien aristeuein
"""

    expected_v_minus_n3 = """==> tests/resources/poem.txt <==
Then it will be GOOD night.

How can I call the lone night good,
Though thy sweet wishes wing its flight?
Be it not said, thought, understood -
Then it will be - GOOD night.

To hearts which near each other move
From evening close to morning light,
The night is good; because, my love,
They never SAY good-night.
"""
    assert runner.invoke(tail, ["-v", "-n 3", LOG_FILE]).output == expected_v_n3
    assert runner.invoke(tail, ["-v", "-n -3", POEM_FILE]).output == expected_v_minus_n3

    expected_c4 = "\nDe lana caprina rixatur\nAien aristeuein\n"
    assert runner.invoke(tail, ["-c 40", LOG_FILE]).output == expected_c4


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

How can I call the lone night good,
Though thy sweet wishes wing its flight?
Be it not said, thought, understood -
Then it will be - GOOD night.

To hearts which near each other move
From evening close to morning light,
The night is good; because, my love,
They never SAY good-night.
"""
    assert runner.invoke(tail, [LOG_FILE, POEM_FILE]).output == expected_multiple_no_opts

    # single option
    expected_multiple_n5 = """==> tests/resources/log.txt <==
Ciao ragazzi
Bon jour
Bratwurst
De lana caprina rixatur
Aien aristeuein

==> tests/resources/poem.txt <==

To hearts which near each other move
From evening close to morning light,
The night is good; because, my love,
They never SAY good-night.
"""
    assert runner.invoke(tail, ["-n 5", LOG_FILE, POEM_FILE]).output == expected_multiple_n5

    # combined options
    expected_multiple_q_n6 = """Hello world
Ciao ragazzi
Bon jour
Bratwurst
De lana caprina rixatur
Aien aristeuein

Then it will be - GOOD night.

To hearts which near each other move
From evening close to morning light,
The night is good; because, my love,
They never SAY good-night.
"""
    assert runner.invoke(tail, ["-q", "-n 6", LOG_FILE, POEM_FILE]).output == expected_multiple_q_n6

    # non-existent file
    expected_multiple_non_existent = f"""tail: cannot open '{NON_EXISTENT_FILE}' for reading: No such file or directory

Then it will be - GOOD night.

To hearts which near each other move
From evening close to morning light,
The night is good; because, my love,
They never SAY good-night.
"""
    assert (
        runner.invoke(tail, ["-q", "-n 6", NON_EXISTENT_FILE, POEM_FILE]).output
        == expected_multiple_non_existent
    )

    # file-path is directory
    assert (
        runner.invoke(tail, [DIR_PATH, NON_EXISTENT_FILE, POEM_FILE]).output
        == f"""tail: cannot open '{DIR_PATH}' for reading: No such file or directory
tail: cannot open '{NON_EXISTENT_FILE}' for reading: No such file or directory

==> tests/resources/poem.txt <==

How can I call the lone night good,
Though thy sweet wishes wing its flight?
Be it not said, thought, understood -
Then it will be - GOOD night.

To hearts which near each other move
From evening close to morning light,
The night is good; because, my love,
They never SAY good-night.
"""
    )
