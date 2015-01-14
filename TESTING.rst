TEST CASES (TBD)
================

SimpleFragment
--------------

``html2text``

::

    $ echo '<ht?+><borkt><h3>hello' > file.txt
    $ html2text file.txt

    HTMLParser.HTMLParseError: malformed start tag, at line 1, column 4

``frag2text``

::

    $ frag2text.py '<ht?+><borkt><h3>hello' css h3

    ### hello


HTMLParseError
--------------

<http://ngm.nationalgeographic.com/print/2007/06/instant-cities/hessler-text>

``html2text`` raises HTMLParseError:

::

    $ html2text <URL>

    HTMLParser.HTMLParseError: malformed start tag, at line 38, column 24

    38:    document.write('<scr' + 'ipt language="JavaScript1.1" SRC="ht

``lynx`` does not preserve formatting:

::

    $ lynx -dump <URL> -nomargins

    169
    170 "Mei shir," Boss Wang said. "No problem."
    171

``frag2text`` parses quickly and preserves formatting

::

    $ frag2text.py <URL> css div

    178
    179 _"Mei shir,"_ Boss Wang said. "No problem."
    180


@siznax
