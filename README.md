Markdown gives you HTML from plain text and html2text reverses the
process. If you want the plain text version of _a specific section_ of
web page (an HTML fragment), you would normally do the selecting
(parsing) first, then generate the Markdown text to preserve some
formatting.

I made _frag2text_ because I want:

* to easily select a web page fragment by CSS selector or XPath
  expression, e.g. "#article" (just the article without boilerplate)
  or "//p[0]" (just the first paragraph) 
* to get the plain text of the fragment with formatting intact for
  later use with Markdown
* to not shell out to a another program (like lynx -dump)
* to not parse HTML or text directly
* to use html5lib for robust parsing
* to have a simple python module that is easy to maintain,
  encapsulating the tricky business of subclassing parsers,
  treebuilders, and serializers by keeping it simple (this shouldn't
  need the power or resources of BeautifulSoup)

This is a problem I've tinkered with for some time and solved in many
different ways. It seems trivial but gets ridiculous quickly. If you
have any suggestions or want to share your experiences with other
tools, please let me know. I hope this can become useful to others.


## Usage

### python

```python
import frag2text
info = frag2text.frag2text(
    'http://wikipedia.org/wiki/Amanita', 'css', '.infobox')
```

### shell

```shell
$ frag2text.py -h
usage: frag2text.py [-h] [-c] [-r] [-v] endpoint {css,xpath} selector

reverse Markdown (html2text) HTML fragments.

positional arguments:
  endpoint       URL, file, or HTML string
  {css,xpath}    fragment selector type
  selector       CSS select statement or XPath expression

optional arguments:
  -h, --help     show this help message and exit
  -c, --clean    clean fragment (lxml.html.clean defaults)
  -r, --raw      output raw fragment
  -v, --verbose  print status, encoding, headers
```


## Examples

### CSS select

```shell
$ frag2text.py http://wikipedia.org/wiki/Amanita css .infobox
_Amanita_
---
![Fliegenpilz-1.jpg](//upload.wikimedia.org/wikipedia/commons/thumb/d/d1
/Fliegenpilz-1.jpg/230px-Fliegenpilz-1.jpg)
_[Amanita muscaria](/wiki/Amanita_muscaria)_
Albin Schmalfuß, 1897
[Scientific classification](/wiki/Biological_classification)
Kingdom: | [Fungi](/wiki/Fungi)
Division: | [Basidiomycota](/wiki/Basidiomycota)
Class: | [Agaricomycetes](/wiki/Agaricomycetes)
Order: | [Agaricales](/wiki/Agaricales)
Family: | [Amanitaceae](/wiki/Amanitaceae)
Genus: | _**Amanita**_
[Pers.](/wiki/Christian_Hendrik_Persoon) (1794)
[Type species](/wiki/Type_species)
_[Amanita muscaria](/wiki/Amanita_muscaria)_
([L.](/wiki/Linnaeus)) [Lam.](/wiki/Lam.) (1783)
[Diversity](/wiki/Biodiversity)
[c.600 species](/wiki/List_of_Amanita_species)
```

### XPath Expression

```shell
$ frag2text.py http://en.wikipedia.org/wiki/Amanita xpath '//p[1]'

The [genus](/wiki/Genus) _**Amanita**_ contains about 600 [species](/wik
i/Species) of [agarics](/wiki/Agarics) including some of the most [toxic
](/wiki/Toxic) known [mushrooms](/wiki/Mushrooms) found worldwide, as we
ll as some well-regarded edible species. This genus is responsible for a
pproximately 95% of the fatalities resulting from [mushroom poisoning](/
wiki/Mushroom_poisoning), with the [death cap](/wiki/Death_cap) accounti
ng for about 50% on its own. The most potent toxin present in these mush
rooms is α[-amanitin](/wiki/%CE%91-amanitin).
```
