#!/usr/bin/env python3
import struct
import argparse
from datetime import datetime
from collections import namedtuple
import os.path

from affinity import AffinityFile

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Loads Affinity Designer files")
    parser.add_argument('input', metavar='INPUT', type=str, help = "The input .afdesign file")
    parser.add_argument('output', metavar='OUTPUT', type=str, help = "Where to write the files to")
    #parser.add_argument('output', metavar='OUTPUT', type=str, help="The output file to write")
    
    args = parser.parse_args()

    inp = args.input

    af = AffinityFile(inp)

    print("This document has {} embedded documents".format(len(af.documents)));

    for document_name, entry in af.documents.items():
        outfile = os.path.join(args.output, document_name)
        dirname = os.path.dirname(outfile)

        if not os.path.exists(dirname):
            os.makedirs(dirname)

        print("Writing {}...".format(outfile))
        with open(outfile, "wb+") as output:
            output.write(entry.data)