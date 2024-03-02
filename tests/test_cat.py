from click.testing import CliRunner

from app.cli.commands import cat

QUOTE_FILE = "tests/resources/quotes1.txt"
ALT_FILE = "tests/resources/quotes2.txt"
NON_EXISTENT_FILE = "test/resources/bazz.yaml"


def test_cat_single_file() -> None:
    runner = CliRunner()
    # no options
    assert (
        runner.invoke(cat, [QUOTE_FILE]).output
        == """Your heart is the size of an ocean. Go find yourself in its hidden depths.
The Bay of Bengal is hit frequently by cyclones. The months of November and May, in particular, are dangerous in this regard.
Thinking is the capital, Enterprise is the way, Hard Work is the solution.
If You Can\'T Make It Good, At Least Make It Look Good.
Heart be brave. If you cannot be brave, just go. Love\'s glory is not a small thing.
It is bad for a young man to sin; but it is worse for an old man to sin.
If You Are Out To Describe The Truth, Leave Elegance To The Tailor.
O man you are busy working for the world, and the world is busy trying to turn you out.
While children are struggling to be unique, the world around them is trying all means to make them look like everybody else.
These Capitalists Generally Act Harmoniously And In Concert, To Fleece The People.
"""
    )

    # single option
    assert (
        runner.invoke(cat, ["-n", QUOTE_FILE]).output
        == """     1 Your heart is the size of an ocean. Go find yourself in its hidden depths.
     2 The Bay of Bengal is hit frequently by cyclones. The months of November and May, in particular, are dangerous in this regard.
     3 Thinking is the capital, Enterprise is the way, Hard Work is the solution.
     4 If You Can'T Make It Good, At Least Make It Look Good.
     5 Heart be brave. If you cannot be brave, just go. Love's glory is not a small thing.
     6 It is bad for a young man to sin; but it is worse for an old man to sin.
     7 If You Are Out To Describe The Truth, Leave Elegance To The Tailor.
     8 O man you are busy working for the world, and the world is busy trying to turn you out.
     9 While children are struggling to be unique, the world around them is trying all means to make them look like everybody else.
    10 These Capitalists Generally Act Harmoniously And In Concert, To Fleece The People.
"""
    )

    assert (
        runner.invoke(cat, ["-b", ALT_FILE]).output
        == """     1 I Don'T Believe In Failure. It Is Not Failure If You Enjoyed The Process.
     2 Do not get elated at any victory, for all such victory is subject to the will of God.

     3 Wear gratitude like a cloak and it will feed every corner of your life.
     4 If you even dream of beating me you'd better wake up and apologize.

     5 I Will Praise Any Man That Will Praise Me.
     6     One Of The Greatest Diseases Is To Be Nobody To Anybody.
     7 I'm so fast that last night I turned off the light switch in my hotel room and was in bed before the room was dark.



     8 People Must Learn To Hate And If They Can Learn To Hate, They Can Be Taught To Love.
     9 Everyone has been made for some particular work, and the desire for that work has been put in every heart.
    10     The less of the World, the freer you live.
"""
    )

    assert (
        runner.invoke(cat, ["-s", ALT_FILE]).output
        == """I Don'T Believe In Failure. It Is Not Failure If You Enjoyed The Process.
Do not get elated at any victory, for all such victory is subject to the will of God.

Wear gratitude like a cloak and it will feed every corner of your life.
If you even dream of beating me you'd better wake up and apologize.

I Will Praise Any Man That Will Praise Me.
    One Of The Greatest Diseases Is To Be Nobody To Anybody.
I'm so fast that last night I turned off the light switch in my hotel room and was in bed before the room was dark.

People Must Learn To Hate And If They Can Learn To Hate, They Can Be Taught To Love.
Everyone has been made for some particular work, and the desire for that work has been put in every heart.
    The less of the World, the freer you live.
"""
    )

    assert (
        runner.invoke(cat, ["-E", ALT_FILE]).output
        == """I Don'T Believe In Failure. It Is Not Failure If You Enjoyed The Process.$
Do not get elated at any victory, for all such victory is subject to the will of God.$
$
Wear gratitude like a cloak and it will feed every corner of your life.$
If you even dream of beating me you'd better wake up and apologize.$
$
I Will Praise Any Man That Will Praise Me.$
    One Of The Greatest Diseases Is To Be Nobody To Anybody.$
I'm so fast that last night I turned off the light switch in my hotel room and was in bed before the room was dark.$
$
$
$
People Must Learn To Hate And If They Can Learn To Hate, They Can Be Taught To Love.$
Everyone has been made for some particular work, and the desire for that work has been put in every heart.$
    The less of the World, the freer you live.$
"""
    )

    assert (
        runner.invoke(cat, ["-T", ALT_FILE]).output
        == """I Don'T Believe In Failure. It Is Not Failure If You Enjoyed The Process.
Do not get elated at any victory, for all such victory is subject to the will of God.

Wear gratitude like a cloak and it will feed every corner of your life.
If you even dream of beating me you'd better wake up and apologize.

I Will Praise Any Man That Will Praise Me.
^One Of The Greatest Diseases Is To Be Nobody To Anybody.
I'm so fast that last night I turned off the light switch in my hotel room and was in bed before the room was dark.



People Must Learn To Hate And If They Can Learn To Hate, They Can Be Taught To Love.
Everyone has been made for some particular work, and the desire for that work has been put in every heart.
^The less of the World, the freer you live.
"""
    )

    assert (
        runner.invoke(cat, ["-A", ALT_FILE]).output
        == """I Don'T Believe In Failure. It Is Not Failure If You Enjoyed The Process.$
Do not get elated at any victory, for all such victory is subject to the will of God.$
$
Wear gratitude like a cloak and it will feed every corner of your life.$
If you even dream of beating me you'd better wake up and apologize.$
$
I Will Praise Any Man That Will Praise Me.$
^One Of The Greatest Diseases Is To Be Nobody To Anybody.$
I'm so fast that last night I turned off the light switch in my hotel room and was in bed before the room was dark.$
$
$
$
People Must Learn To Hate And If They Can Learn To Hate, They Can Be Taught To Love.$
Everyone has been made for some particular work, and the desire for that work has been put in every heart.$
^The less of the World, the freer you live.$
"""
    )

    assert (
        runner.invoke(cat, ["-A", ALT_FILE]).output == runner.invoke(cat, ["-ET", ALT_FILE]).output
    )

    # combined options
    assert (
        runner.invoke(cat, ["-nE", QUOTE_FILE]).output
        == """     1 Your heart is the size of an ocean. Go find yourself in its hidden depths.$
     2 The Bay of Bengal is hit frequently by cyclones. The months of November and May, in particular, are dangerous in this regard.$
     3 Thinking is the capital, Enterprise is the way, Hard Work is the solution.$
     4 If You Can'T Make It Good, At Least Make It Look Good.$
     5 Heart be brave. If you cannot be brave, just go. Love's glory is not a small thing.$
     6 It is bad for a young man to sin; but it is worse for an old man to sin.$
     7 If You Are Out To Describe The Truth, Leave Elegance To The Tailor.$
     8 O man you are busy working for the world, and the world is busy trying to turn you out.$
     9 While children are struggling to be unique, the world around them is trying all means to make them look like everybody else.$
    10 These Capitalists Generally Act Harmoniously And In Concert, To Fleece The People.$
"""
    )

    assert (
        runner.invoke(cat, ["-bs", ALT_FILE]).output
        == """     1 I Don'T Believe In Failure. It Is Not Failure If You Enjoyed The Process.
     2 Do not get elated at any victory, for all such victory is subject to the will of God.

     3 Wear gratitude like a cloak and it will feed every corner of your life.
     4 If you even dream of beating me you'd better wake up and apologize.

     5 I Will Praise Any Man That Will Praise Me.
     6     One Of The Greatest Diseases Is To Be Nobody To Anybody.
     7 I'm so fast that last night I turned off the light switch in my hotel room and was in bed before the room was dark.

     8 People Must Learn To Hate And If They Can Learn To Hate, They Can Be Taught To Love.
     9 Everyone has been made for some particular work, and the desire for that work has been put in every heart.
    10     The less of the World, the freer you live.
"""
    )

    assert (
        runner.invoke(cat, ["-sT", QUOTE_FILE]).output
        == """Your heart is the size of an ocean. Go find yourself in its hidden depths.
The Bay of Bengal is hit frequently by cyclones. The months of November and May, in particular, are dangerous in this regard.
Thinking is the capital, Enterprise is the way, Hard Work is the solution.\nIf You Can'T Make It Good, At Least Make It Look Good.
Heart be brave. If you cannot be brave, just go. Love's glory is not a small thing.
It is bad for a young man to sin; but it is worse for an old man to sin.
If You Are Out To Describe The Truth, Leave Elegance To The Tailor.
O man you are busy working for the world, and the world is busy trying to turn you out.
While children are struggling to be unique, the world around them is trying all means to make them look like everybody else.
These Capitalists Generally Act Harmoniously And In Concert, To Fleece The People.
"""
    )

    # error messages
    assert (
        runner.invoke(cat, ["-n", "-b", QUOTE_FILE]).exception.args[0]
        == "Contradicting flags passed: 'number' and 'number-nonblank'"
    )
    assert (
        runner.invoke(cat, ["-n", NON_EXISTENT_FILE]).exception.args[0]
        == f"cat: {NON_EXISTENT_FILE}: No such file or directory"
    )


def test_cat_file_list() -> None:
    runner = CliRunner()
    # no options
    assert (
        runner.invoke(cat, [QUOTE_FILE, ALT_FILE]).output
        == """Your heart is the size of an ocean. Go find yourself in its hidden depths.
The Bay of Bengal is hit frequently by cyclones. The months of November and May, in particular, are dangerous in this regard.
Thinking is the capital, Enterprise is the way, Hard Work is the solution.
If You Can'T Make It Good, At Least Make It Look Good.
Heart be brave. If you cannot be brave, just go. Love's glory is not a small thing.
It is bad for a young man to sin; but it is worse for an old man to sin.
If You Are Out To Describe The Truth, Leave Elegance To The Tailor.
O man you are busy working for the world, and the world is busy trying to turn you out.
While children are struggling to be unique, the world around them is trying all means to make them look like everybody else.
These Capitalists Generally Act Harmoniously And In Concert, To Fleece The People.
I Don'T Believe In Failure. It Is Not Failure If You Enjoyed The Process.
Do not get elated at any victory, for all such victory is subject to the will of God.

Wear gratitude like a cloak and it will feed every corner of your life.
If you even dream of beating me you'd better wake up and apologize.

I Will Praise Any Man That Will Praise Me.
    One Of The Greatest Diseases Is To Be Nobody To Anybody.
I'm so fast that last night I turned off the light switch in my hotel room and was in bed before the room was dark.



People Must Learn To Hate And If They Can Learn To Hate, They Can Be Taught To Love.
Everyone has been made for some particular work, and the desire for that work has been put in every heart.
    The less of the World, the freer you live.
"""
    )

    # single option
    assert (
        runner.invoke(cat, ["-n", QUOTE_FILE, ALT_FILE]).output
        == """     1 Your heart is the size of an ocean. Go find yourself in its hidden depths.
     2 The Bay of Bengal is hit frequently by cyclones. The months of November and May, in particular, are dangerous in this regard.
     3 Thinking is the capital, Enterprise is the way, Hard Work is the solution.
     4 If You Can'T Make It Good, At Least Make It Look Good.
     5 Heart be brave. If you cannot be brave, just go. Love's glory is not a small thing.
     6 It is bad for a young man to sin; but it is worse for an old man to sin.
     7 If You Are Out To Describe The Truth, Leave Elegance To The Tailor.
     8 O man you are busy working for the world, and the world is busy trying to turn you out.
     9 While children are struggling to be unique, the world around them is trying all means to make them look like everybody else.
    10 These Capitalists Generally Act Harmoniously And In Concert, To Fleece The People.
    11 I Don'T Believe In Failure. It Is Not Failure If You Enjoyed The Process.
    12 Do not get elated at any victory, for all such victory is subject to the will of God.
    13 
    14 Wear gratitude like a cloak and it will feed every corner of your life.
    15 If you even dream of beating me you'd better wake up and apologize.
    16 
    17 I Will Praise Any Man That Will Praise Me.
    18     One Of The Greatest Diseases Is To Be Nobody To Anybody.
    19 I'm so fast that last night I turned off the light switch in my hotel room and was in bed before the room was dark.
    20 
    21 
    22 
    23 People Must Learn To Hate And If They Can Learn To Hate, They Can Be Taught To Love.
    24 Everyone has been made for some particular work, and the desire for that work has been put in every heart.
    25     The less of the World, the freer you live.
"""
    )

    assert (
        runner.invoke(cat, ["-b", QUOTE_FILE, ALT_FILE]).output
        == """     1 Your heart is the size of an ocean. Go find yourself in its hidden depths.
     2 The Bay of Bengal is hit frequently by cyclones. The months of November and May, in particular, are dangerous in this regard.
     3 Thinking is the capital, Enterprise is the way, Hard Work is the solution.
     4 If You Can'T Make It Good, At Least Make It Look Good.
     5 Heart be brave. If you cannot be brave, just go. Love's glory is not a small thing.
     6 It is bad for a young man to sin; but it is worse for an old man to sin.
     7 If You Are Out To Describe The Truth, Leave Elegance To The Tailor.
     8 O man you are busy working for the world, and the world is busy trying to turn you out.
     9 While children are struggling to be unique, the world around them is trying all means to make them look like everybody else.
    10 These Capitalists Generally Act Harmoniously And In Concert, To Fleece The People.
    11 I Don'T Believe In Failure. It Is Not Failure If You Enjoyed The Process.
    12 Do not get elated at any victory, for all such victory is subject to the will of God.

    13 Wear gratitude like a cloak and it will feed every corner of your life.
    14 If you even dream of beating me you'd better wake up and apologize.

    15 I Will Praise Any Man That Will Praise Me.
    16     One Of The Greatest Diseases Is To Be Nobody To Anybody.
    17 I'm so fast that last night I turned off the light switch in my hotel room and was in bed before the room was dark.



    18 People Must Learn To Hate And If They Can Learn To Hate, They Can Be Taught To Love.
    19 Everyone has been made for some particular work, and the desire for that work has been put in every heart.
    20     The less of the World, the freer you live.
"""
    )

    assert (
        runner.invoke(cat, ["-s", QUOTE_FILE, ALT_FILE]).output
        == """Your heart is the size of an ocean. Go find yourself in its hidden depths.
The Bay of Bengal is hit frequently by cyclones. The months of November and May, in particular, are dangerous in this regard.
Thinking is the capital, Enterprise is the way, Hard Work is the solution.
If You Can'T Make It Good, At Least Make It Look Good.\nHeart be brave. If you cannot be brave, just go. Love's glory is not a small thing.
It is bad for a young man to sin; but it is worse for an old man to sin.
If You Are Out To Describe The Truth, Leave Elegance To The Tailor.
O man you are busy working for the world, and the world is busy trying to turn you out.
While children are struggling to be unique, the world around them is trying all means to make them look like everybody else.
These Capitalists Generally Act Harmoniously And In Concert, To Fleece The People.
I Don'T Believe In Failure. It Is Not Failure If You Enjoyed The Process.
Do not get elated at any victory, for all such victory is subject to the will of God.

Wear gratitude like a cloak and it will feed every corner of your life.
If you even dream of beating me you'd better wake up and apologize.

I Will Praise Any Man That Will Praise Me.
    One Of The Greatest Diseases Is To Be Nobody To Anybody.
I'm so fast that last night I turned off the light switch in my hotel room and was in bed before the room was dark.

People Must Learn To Hate And If They Can Learn To Hate, They Can Be Taught To Love.
Everyone has been made for some particular work, and the desire for that work has been put in every heart.
    The less of the World, the freer you live.
"""
    )

    # combined options
    assert (
        runner.invoke(cat, ["-nE", QUOTE_FILE, ALT_FILE]).output
        == """     1 Your heart is the size of an ocean. Go find yourself in its hidden depths.$
     2 The Bay of Bengal is hit frequently by cyclones. The months of November and May, in particular, are dangerous in this regard.$
     3 Thinking is the capital, Enterprise is the way, Hard Work is the solution.$
     4 If You Can'T Make It Good, At Least Make It Look Good.$
     5 Heart be brave. If you cannot be brave, just go. Love's glory is not a small thing.$
     6 It is bad for a young man to sin; but it is worse for an old man to sin.$
     7 If You Are Out To Describe The Truth, Leave Elegance To The Tailor.$
     8 O man you are busy working for the world, and the world is busy trying to turn you out.$
     9 While children are struggling to be unique, the world around them is trying all means to make them look like everybody else.$
    10 These Capitalists Generally Act Harmoniously And In Concert, To Fleece The People.$
    11 I Don'T Believe In Failure. It Is Not Failure If You Enjoyed The Process.$
    12 Do not get elated at any victory, for all such victory is subject to the will of God.$
    13 $
    14 Wear gratitude like a cloak and it will feed every corner of your life.$
    15 If you even dream of beating me you'd better wake up and apologize.$
    16 $
    17 I Will Praise Any Man That Will Praise Me.$
    18     One Of The Greatest Diseases Is To Be Nobody To Anybody.$
    19 I'm so fast that last night I turned off the light switch in my hotel room and was in bed before the room was dark.$
    20 $
    21 $
    22 $
    23 People Must Learn To Hate And If They Can Learn To Hate, They Can Be Taught To Love.$
    24 Everyone has been made for some particular work, and the desire for that work has been put in every heart.$
    25     The less of the World, the freer you live.$
"""
    )

    assert (
        runner.invoke(cat, ["-bs", QUOTE_FILE, ALT_FILE]).output
        == """     1 Your heart is the size of an ocean. Go find yourself in its hidden depths.
     2 The Bay of Bengal is hit frequently by cyclones. The months of November and May, in particular, are dangerous in this regard.
     3 Thinking is the capital, Enterprise is the way, Hard Work is the solution.
     4 If You Can'T Make It Good, At Least Make It Look Good.
     5 Heart be brave. If you cannot be brave, just go. Love's glory is not a small thing.
     6 It is bad for a young man to sin; but it is worse for an old man to sin.
     7 If You Are Out To Describe The Truth, Leave Elegance To The Tailor.
     8 O man you are busy working for the world, and the world is busy trying to turn you out.
     9 While children are struggling to be unique, the world around them is trying all means to make them look like everybody else.
    10 These Capitalists Generally Act Harmoniously And In Concert, To Fleece The People.
    11 I Don'T Believe In Failure. It Is Not Failure If You Enjoyed The Process.
    12 Do not get elated at any victory, for all such victory is subject to the will of God.

    13 Wear gratitude like a cloak and it will feed every corner of your life.
    14 If you even dream of beating me you'd better wake up and apologize.

    15 I Will Praise Any Man That Will Praise Me.
    16     One Of The Greatest Diseases Is To Be Nobody To Anybody.
    17 I'm so fast that last night I turned off the light switch in my hotel room and was in bed before the room was dark.

    18 People Must Learn To Hate And If They Can Learn To Hate, They Can Be Taught To Love.
    19 Everyone has been made for some particular work, and the desire for that work has been put in every heart.
    20     The less of the World, the freer you live.
"""
    )

    assert (
        runner.invoke(cat, ["-sT", QUOTE_FILE, ALT_FILE]).output
        == """Your heart is the size of an ocean. Go find yourself in its hidden depths.
The Bay of Bengal is hit frequently by cyclones. The months of November and May, in particular, are dangerous in this regard.
Thinking is the capital, Enterprise is the way, Hard Work is the solution.
If You Can'T Make It Good, At Least Make It Look Good.
Heart be brave. If you cannot be brave, just go. Love's glory is not a small thing.
It is bad for a young man to sin; but it is worse for an old man to sin.
If You Are Out To Describe The Truth, Leave Elegance To The Tailor.
O man you are busy working for the world, and the world is busy trying to turn you out.
While children are struggling to be unique, the world around them is trying all means to make them look like everybody else.
These Capitalists Generally Act Harmoniously And In Concert, To Fleece The People.
I Don'T Believe In Failure. It Is Not Failure If You Enjoyed The Process.
Do not get elated at any victory, for all such victory is subject to the will of God.

Wear gratitude like a cloak and it will feed every corner of your life.
If you even dream of beating me you'd better wake up and apologize.

I Will Praise Any Man That Will Praise Me.
^One Of The Greatest Diseases Is To Be Nobody To Anybody.
I'm so fast that last night I turned off the light switch in my hotel room and was in bed before the room was dark.

People Must Learn To Hate And If They Can Learn To Hate, They Can Be Taught To Love.
Everyone has been made for some particular work, and the desire for that work has been put in every heart.
^The less of the World, the freer you live.
"""
    )

    # non-existent file
    assert (
        runner.invoke(cat, [QUOTE_FILE, NON_EXISTENT_FILE]).output
        == """Your heart is the size of an ocean. Go find yourself in its hidden depths.
The Bay of Bengal is hit frequently by cyclones. The months of November and May, in particular, are dangerous in this regard.
Thinking is the capital, Enterprise is the way, Hard Work is the solution.
If You Can'T Make It Good, At Least Make It Look Good.
Heart be brave. If you cannot be brave, just go. Love's glory is not a small thing.
It is bad for a young man to sin; but it is worse for an old man to sin.
If You Are Out To Describe The Truth, Leave Elegance To The Tailor.
O man you are busy working for the world, and the world is busy trying to turn you out.
While children are struggling to be unique, the world around them is trying all means to make them look like everybody else.
These Capitalists Generally Act Harmoniously And In Concert, To Fleece The People.
cat: test/resources/bazz.yaml: No such file or directory
"""
    )
