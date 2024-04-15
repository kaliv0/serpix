from click.testing import CliRunner

from app.cli.commands import uniq


runner = CliRunner()

def test_uniq() -> None:
    assert runner.invoke(cat, [QUOTE_FILE]).output == """"""

    # single option
    # assert runner.invoke(cat, ["-n", QUOTE_FILE]).output == """"""

    # combined options

    # error messages
    # assert runner.invoke(cat, ["-n", "-b", QUOTE_FILE]).exception.args[0] == ""

    import subprocess

    expected = result = subprocess.run(
        ["uniq", "./tests/resources/duplicates.txt"], capture_output=True, text=True
    ).stdout

    actual = runner.invoke(uniq, ["./tests/resources/duplicates.txt"]).output
    assert expected == actual
