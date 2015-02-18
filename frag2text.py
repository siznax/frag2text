#!/usr/bin/env python
"""Select and reverse-Markdown (html2text) web page fragments."""

import argparse
import cssselect
import html2text
import html5lib
import lxml.cssselect
import lxml.html
import lxml.html.clean
import os
import requests
import sys

__author__ = "Steve @siznax"
__date__ = "Feb 2015"
__license__ = "MIT"
__version__ = '0.0.5'


class Frag2Text:

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.encoding = 'utf-8'

    def user_agent():
        """return user-agent for HTTP requests."""
        pass

    def read(self, _file):
        """return local file contents as endpoint."""
        with open(_file) as fh:
            data = fh.read()
            if self.verbose:
                sys.stdout.write("read %d bytes from %s\n"
                                 % (fh.tell(), _file))
        return data

    def GET(self, url):
        """returns text content of HTTP GET response."""
        r = requests.get(url)
        if self.verbose:
            sys.stdout.write("%s %s\n" % (r.status_code, r.encoding))
            sys.stdout.write(str(r.headers) + "\n")
        self.encoding = r.encoding
        return r.text

    def select(self, html, stype, expression):
        """returns WHATWG spec HTML fragment from selector expression."""
        etree = html5lib.parse(html,
                               treebuilder='lxml',
                               namespaceHTMLElements=False)
        if stype == 'css':
            selector = lxml.cssselect.CSSSelector(expression)
            frag = list(selector(etree))
        else:
            frag = etree.xpath(expression)
        if not frag:
            raise RuntimeError("Nothing found for: %s" % expression)
        return "".join([lxml.etree.tostring(x) for x in frag])

    def clean(self, html):
        """removes evil HTML per lxml.html.clean defaults."""
        return lxml.html.clean.clean_html(unicode(html, self.encoding))


def safe_exit(output):
    """exit without breaking pipes."""
    try:
        sys.stdout.write(output)
        sys.stdout.flush()
    except IOError:
        pass


def frag2text(endpoint, stype, selector,
              clean=False, raw=False, verbose=False):
    """returns Markdown text of selected fragment.

    Args:
        endpoint: URL, file, or HTML string
        stype: { 'css' | 'xpath' }
        selector: CSS selector or XPath expression
    Returns:
        Markdown text
    Options:
        clean: cleans fragment (lxml.html.clean defaults)
        raw: returns raw HTML fragment
        verbose: show http status, encoding, headers
    """
    try:
        return main(endpoint, stype, selector, clean, raw, verbose)
    except StandardError as err:
        return err


def main(endpoint, stype, selector, clean, raw, verbose):

    ftt = Frag2Text(verbose)
    if endpoint.startswith('http'):
        html = ftt.GET(endpoint)
    elif os.path.exists(endpoint):
        html = ftt.read(endpoint)
    else:
        html = endpoint

    try:
        frag = ftt.select(html, stype, selector)
    except lxml.etree.XPathEvalError as err:
        raise Exception("XPathEvalError: %s" % err)
    except cssselect.parser.SelectorSyntaxError as err:
        raise Exception("SelectorSyntaxError: %s" % err)
    except RuntimeError as err:
        raise Exception(err)

    if clean:
        frag = ftt.clean(frag)
    if raw:
        return frag.encode('utf-8')
    return html2text.html2text(frag, '', 0).encode('utf-8')


if __name__ == "__main__":
    desc = "reverse Markdown (html2text) HTML fragments."
    argp = argparse.ArgumentParser(description=desc)
    argp.add_argument("endpoint", help="URL, file, or HTML string")
    argp.add_argument("type", choices=['css', 'xpath'],
                      help="fragment selector type")
    argp.add_argument("selector",
                      help="CSS select statement or XPath expression")
    argp.add_argument("-c", "--clean", action="store_true",
                      help="clean fragment (lxml.html.clean defaults)")
    argp.add_argument("-r", "--raw", action="store_true",
                      help="output raw fragment")
    argp.add_argument("-v", "--verbose", action="store_true",
                      help="print status, encoding, headers")
    args = argp.parse_args()

    safe_exit(main(args.endpoint, args.type, args.selector,
                   args.clean, args.raw, args.verbose))
