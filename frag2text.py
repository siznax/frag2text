#!/usr/bin/env python

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
    """robust reverse Markdown (html2text) HTML fragments."""

    def __init__(self, verbose=False, encoding='utf-8'):
        self.verbose = verbose
        self.encoding = encoding

    def read(self, _file):
        with open(_file) as fh:
            data = fh.read()
            if self.verbose:
                print "read %d bytes from %s" % (fh.tell(), _file)
        return data

    def GET(self, url):
        """returns text content of HTTP GET response from URL."""
        r = requests.get(url)
        if self.verbose:
            sys.stdout.write("%s %s\n" % (r.status_code, r.encoding))
            sys.stdout.write(str(r.headers) + "\n")
        self.http_status = r.status_code
        self.encoding = r.encoding
        self.response_headers = r.headers
        return r.text

    def select(self, html, expression, _type):
        """returns WHATWG spec HTML fragment from selector expression."""
        etree = html5lib.parse(html,
                               treebuilder='lxml',
                               namespaceHTMLElements=False)
        if _type == 'css':
            selector = lxml.cssselect.CSSSelector(expression)
            frag = list(selector(etree))
        else:
            frag = etree.xpath(expression)
        if frag:
            return lxml.etree.tostring(frag[0])

    def clean_html(self, html):
        """removes evil HTML per lxml.html.clean defaults."""
        return lxml.html.clean.clean_html(unicode(html, self.encoding))


def safe_exit(output):
    try:
        sys.stdout.write(output)
        sys.stdout.flush()
    except IOError:
        pass


def main(args):
    frag2text = Frag2Text(args.verbose)
    if os.path.exists(args.endpoint):
        html = frag2text.read(args.endpoint)
    else:
        html = frag2text.GET(args.endpoint)
    frag = frag2text.select(html, args.selector, args.type)
    if not frag:
        sys.stdout.write("Error: selector '%s' found None.\n"
                         % args.selector)
        sys.exit(os.EX_DATAERR)
    if args.raw:
        return frag.encode('utf-8')
    if args.clean:
        frag = frag2text.clean_html(frag)
    return html2text.html2text(frag, '', 0).encode('utf-8')


if __name__ == "__main__":
    desc = "reverse Markdown (html2text) HTML fragments."
    argp = argparse.ArgumentParser(description=desc)
    argp.add_argument("endpoint", help="URL or file")
    argp.add_argument("type", choices=['css', 'xpath'],
                      help="fragment selector type")
    argp.add_argument("selector",
                      help="CSS select statement or XPath expression")
    argp.add_argument("-r", "--raw", action="store_true",
                      help="output raw fragment")
    argp.add_argument("-c", "--clean", action="store_true",
                      help="output lxml.html.clean fragment")
    argp.add_argument("-v", "--verbose", action="store_true",
                      help="print status, encoding, headers")
    args = argp.parse_args()

    safe_exit(main(args))


# TEST CASES TBD (but hoping html5lib covers them)
