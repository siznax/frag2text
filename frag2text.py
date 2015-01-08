#!/usr/bin/env python
"""Select and reverse-Markdown (html2text) web page fragments."""

__author__ = "@siznax"
__date__ = "Jan 2015"

import argparse
import html2text
import html5lib
import lxml.cssselect
import lxml.html
import lxml.html.clean
import os
import requests
import sys


class Frag2Text:

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.encoding = 'utf-8'

    def read(self, _file):
        with open(_file) as fh:
            data = fh.read()
            if self.verbose:
                print "read %d bytes from %s" % (fh.tell(), _file)
        return data

    def GET(self, url):
        """returns text content of HTTP GET response."""
        r = requests.get(url)
        if self.verbose:
            sys.stdout.write("%s %s\n" % (r.status_code, r.encoding))
            sys.stdout.write(str(r.headers) + "\n")
        self.http_status = r.status_code
        self.encoding = r.encoding
        self.response_headers = r.headers
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
        if frag:
            return lxml.etree.tostring(frag[0])

    def clean(self, html):
        """removes evil HTML per lxml.html.clean defaults."""
        return lxml.html.clean.clean_html(unicode(html, self.encoding))


def safe_exit(output):
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
        type: { 'css' | 'xpath' }
        selector: CSS selector or XPath expression
    Returns:
        Markdown text
    Options:
        clean: cleans fragment (lxml.html.clean defaults)
        raw: returns raw HTML fragment
        verbose: show http status, encoding, headers
    """
    return main(endpoint, stype, selector, clean, raw, verbose)


def main(endpoint, stype, selector, clean, raw, verbose):
    ftt = Frag2Text(verbose)
    if endpoint.startswith('http'):
        html = ftt.GET(endpoint)
    elif os.path.exists(endpoint):
        html = ftt.read(endpoint)
    else:
        html = endpoint
    frag = ftt.select(html, stype, selector)
    if not frag:
        sys.stdout.write("Error: selector '%s' not found.\n" % selector)
        sys.exit(os.EX_DATAERR)
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