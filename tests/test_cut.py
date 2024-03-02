from click.testing import CliRunner

from app.cli.commands import cut

TSV_FILE = "tests/resources/books1.tsv"
CSV_FILE = "tests/resources/books2.csv"
ALT_CSV_FILE = "tests/resources/books3.csv"
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


def test_cut_file_list() -> None:
    runner = CliRunner()

    # single option
    assert (
        runner.invoke(cut, ["-b1-3", TSV_FILE, CSV_FILE]).output
        == """pyt
sna
alp
rob
hor
don
ory
pyt
sna
alp
rob
hor
don
ory
Lor
"""
    )
    assert (
        runner.invoke(cut, ["-c2-8", TSV_FILE, CSV_FILE]).output
        == """ython\tP
nail\tSS
lpaca\tI
obin\tMy
orse\tLi
onkey\tC
ryx\tWri
ython,P
nail,SS
lpaca,I
obin,My
orse,Li
onkey,C
ryx,Wri
orem Ip
"""
    )

    # combined options
    assert (
        runner.invoke(cut, ["-f1", "-d,", CSV_FILE, ALT_CSV_FILE]).output
        == """python
snail
alpaca
robin
horse
donkey
oryx
Lorem Ipsum et cetera res vana
English
French
Greek
That book you never really read...
Latin
"""
    )
    assert (
        runner.invoke(cut, ["-f1", "-d,", "-s", CSV_FILE, ALT_CSV_FILE]).output
        == """python
snail
alpaca
robin
horse
donkey
oryx
English
French
Greek
Latin
"""
    )
    assert (
        runner.invoke(cut, ["-f2-3", NON_EXISTENT_FILE, TSV_FILE]).output
        == """cut: test/resources/bazz.yaml: No such file or directory
Programming Python\t2010
SSH, The Secure Shell\t2005
Intermediate Perl\t2012
MySQL High Availability\t2014
Linux in a Nutshell\t2009
Cisco IOS in a Nutshell\t2005
Writing Word Macros\t1999
"""
    )
