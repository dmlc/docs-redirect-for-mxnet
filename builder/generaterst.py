#!/usr/bin/env python
"""Tool to generate a set of .rst
files to be used with sphinx/readthedocs.org
that all redirect to a parallel site in another domain.

e.g. In your old docs site, run

make html
find . > /tmp/filelist.txt

to generate your filelist.
"""

import argparse
import os


def command_args(defaults=False):
    parser = argparse.ArgumentParser(description=__doc__,
            formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-fl","--filelist",
            help="List of files built by the original docs site",
            default="data/filelist.txt",
            type=str)
    parser.add_argument("-xl","--exceptionlist",
            help="List of mapping exceptions",
            default="data/exceptions.txt",
            type=str)
    parser.add_argument("-o","--output-path",
            help="Path where rst files should be written",
            default="docs/")
    parser.add_argument("-t","--target-url",
            help="URL prefix to redirect to",
            default="http://mxnet.io/")
    if defaults:
        return parser.parse_args([])
    else:
        return parser.parse_args()


def ensure_dir(fn):
    dirname, filename = os.path.split(fn)
    if not os.path.exists(dirname):
        os.makedirs(dirname)


class RedirectGenerator(object):

    def __init__(self, cmd):
        self.cmd = cmd
        self.load_exceptions()

    def load_exceptions(self):
        exception_lines = open(self.cmd.exceptionlist).readlines()
        self.exceptions = {}
        for line in exception_lines:
            line = line.rstrip()
            a,b = line.split(',')
            if b == "0":
                b = False
            self.exceptions[a] = b

    def generate_url(self, fn):
        if self.exceptions.has_key(fn):
            suffix = self.exceptions[fn]
        else:
            suffix = fn
        return self.cmd.target_url + suffix

    def generate_filename(self, fn):
        partial_fn, ext = os.path.splitext(fn)
        return self.cmd.output_path + partial_fn + ".rst"

    def should_skip(self, fn):
        if self.exceptions.has_key(fn):
            exc = self.exceptions[fn]
            if not exc:
                return True
            else:
                return False
        if fn.endswith(".html"):
            return False  # Don't skip HTML files
        return True  # Skip the others

    def process(self, fn):
        if self.should_skip(fn):
            print("Skipping file %s" % fn)
            return
        print("Processing file %s" % fn)
        out_fn = self.generate_filename(fn)
        redir_url = self.generate_url(fn)
        print("Writing redirect file %s to %s" % (out_fn, redir_url))
        ensure_dir(out_fn)
        with open(out_fn,"w") as outf:
            outf.write(".. meta::\n    :http-equiv=refresh: 0;URL='%s'\n" % redir_url)


def main(cmd):
    gen = RedirectGenerator(cmd)
    filelist = open(cmd.filelist).readlines()
    for fn in filelist:
        fn = fn.rstrip()
        if fn.startswith("./"):
            fn = fn[2:]
        gen.process(fn)


if __name__ == "__main__":
    cmd = command_args()
    main(cmd)

    
    

