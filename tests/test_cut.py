from click.testing import CliRunner

from app.cli.commands import cut

TSV_FILE = "tests/resources/books1.tsv"
CSV_FILE = "tests/resources/books2.csv"
NON_EXISTENT_FILE = "test/resources/bazz.yaml"


def test_cut_single_file() -> None:
    runner = CliRunner()

    # single option
    ## bytes
    assert runner.invoke(cut, ["-b1", TSV_FILE]).output == "p\ns\na\nr\nh\nd\no\n"
    assert (
        runner.invoke(cut, ["-b4-", TSV_FILE]).output
        == """hon\tProgramming Python\t2010\tLutz, Mark
il\tSSH, The Secure Shell\t2005\tBarrett, Daniel
aca\tIntermediate Perl\t2012\tSchwartz, Randal
in\tMySQL High Availability\t2014\tBell, Charles
se\tLinux in a Nutshell\t2009\tSiever, Ellen
key\tCisco IOS in a Nutshell\t2005\tBoney, James
x\tWriting Word Macros\t1999\tRoman, Steven
"""
    )
    assert (
        runner.invoke(cut, ["-b-3", TSV_FILE]).output
        == """pyt
sna
alp
rob
hor
don
ory
"""
    )
    assert (
        runner.invoke(cut, ["-b1-5", TSV_FILE]).output
        == """pytho
snail
alpac
robin
horse
donke
oryx
"""
    )

    ## characters
    assert runner.invoke(cut, ["-c1", TSV_FILE]).output == "p\ns\na\nr\nh\nd\no\n"
    assert (
        runner.invoke(cut, ["-c4-", TSV_FILE]).output
        == """hon\tProgramming Python\t2010\tLutz, Mark
il\tSSH, The Secure Shell\t2005\tBarrett, Daniel
aca\tIntermediate Perl\t2012\tSchwartz, Randal
in\tMySQL High Availability\t2014\tBell, Charles
se\tLinux in a Nutshell\t2009\tSiever, Ellen
key\tCisco IOS in a Nutshell\t2005\tBoney, James
x\tWriting Word Macros\t1999\tRoman, Steven
"""
    )
    assert (
        runner.invoke(cut, ["-c-3", TSV_FILE]).output
        == """pyt
sna
alp
rob
hor
don
ory
"""
    )
    assert (
        runner.invoke(cut, ["-c3-8", TSV_FILE]).output
        == """thon\tP
ail\tSS
paca\tI
bin\tMy
rse\tLi
nkey\tC
yx\tWri
"""
    )

    ## fields
    assert (
        runner.invoke(cut, ["-f1", TSV_FILE]).output
        == """python\nsnail\nalpaca\nrobin\nhorse\ndonkey\noryx\n"""
    )
    assert (
        runner.invoke(cut, ["-f2-", TSV_FILE]).output
        == """Programming Python\t2010\tLutz, Mark
SSH, The Secure Shell\t2005\tBarrett, Daniel
Intermediate Perl\t2012\tSchwartz, Randal
MySQL High Availability\t2014\tBell, Charles
Linux in a Nutshell\t2009\tSiever, Ellen
Cisco IOS in a Nutshell\t2005\tBoney, James
Writing Word Macros\t1999\tRoman, Steven
"""
    )
    assert (
        runner.invoke(cut, ["-f-3", TSV_FILE]).output
        == """python\tProgramming Python\t2010
snail\tSSH, The Secure Shell\t2005
alpaca\tIntermediate Perl\t2012
robin\tMySQL High Availability\t2014
horse\tLinux in a Nutshell\t2009
donkey\tCisco IOS in a Nutshell\t2005
oryx\tWriting Word Macros\t1999
"""
    )
    assert (
        runner.invoke(cut, ["-f2-4", TSV_FILE]).output
        == """Programming Python\t2010\tLutz, Mark
SSH, The Secure Shell\t2005\tBarrett, Daniel
Intermediate Perl\t2012\tSchwartz, Randal
MySQL High Availability\t2014\tBell, Charles
Linux in a Nutshell\t2009\tSiever, Ellen
Cisco IOS in a Nutshell\t2005\tBoney, James
Writing Word Macros\t1999\tRoman, Steven
"""
    )

    # combined options
    assert (
        runner.invoke(cut, ["-f-3", "-d,", CSV_FILE]).output
        == """python,Programming Python,2010
snail,SSH The Secure Shell,2005\nalpaca,Intermediate Perl,2012
robin,MySQL High Availability,2014
horse,Linux in a Nutshell,2009
donkey,Cisco IOS in a Nutshell,2005
oryx,Writing Word Macros,1999
Lorem Ipsum et cetera res vana
"""
    )
    assert (
        runner.invoke(cut, ["-f-3", "-d,", "-s", CSV_FILE]).output
        == """python,Programming Python,2010
snail,SSH The Secure Shell,2005\nalpaca,Intermediate Perl,2012
robin,MySQL High Availability,2014
horse,Linux in a Nutshell,2009
donkey,Cisco IOS in a Nutshell,2005
oryx,Writing Word Macros,1999
"""
    )
    assert (
        runner.invoke(cut, ["-f-3", "-d,", "-s", "--output-delimiter=' # '", CSV_FILE]).output
        == """python' # 'Programming Python' # '2010
snail' # 'SSH The Secure Shell' # '2005
alpaca' # 'Intermediate Perl' # '2012
robin' # 'MySQL High Availability' # '2014
horse' # 'Linux in a Nutshell' # '2009
donkey' # 'Cisco IOS in a Nutshell' # '2005
oryx' # 'Writing Word Macros' # '1999
"""
    )


def test_cut_file_list() -> None:
    runner = CliRunner()
    # no options
    assert runner.invoke(cut, [TSV_FILE, CSV_FILE]).output == """"""

    # single option
    assert runner.invoke(cut, ["-", TSV_FILE, CSV_FILE]).output == """"""

    # combined options

    # non-existent file
