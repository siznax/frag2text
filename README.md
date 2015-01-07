Robustly reverse-Markdown (html2text) web page fragments by CSS
selector or Xpath expression.

### Usage

```shell
$ frag2text.py -h
usage: frag2text.py [-h] [-r] [-c] [-v] endpoint {css,xpath} selector

reverse Markdown (html2text) HTML fragments.

positional arguments:
  endpoint       URL or file
  {css,xpath}    fragment selector type
  selector       CSS select statement or Xpath expression

optional arguments:
  -h, --help     show this help message and exit
  -r, --raw      output raw fragment
  -c, --clean    output lxml.html.clean fragment
  -v, --verbose  print status, encoding, headers
```

### CSS Select

```shell
$ frag2text.py http://en.wikipedia.org/wiki/Amanita css .infobox

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
