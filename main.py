#!/usr/bin/env python3
import struct
import argparse
from datetime import datetime
from collections import namedtuple
import os.path

from affinity import AffinityFile

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Loads Affinity Designer files")
    parser.add_argument('input', metavar='INPUT', type=argparse.FileType('rb'), help = "The input .afdesign file")
    parser.add_argument('output', metavar='OUTPUT', type=str, help = "Where to write the files to")
    #parser.add_argument('output', metavar='OUTPUT', type=str, help="The output file to write")
    
    args = parser.parse_args()

    inp = args.input

    af = AffinityFile(inp)

    for f in af.fat_entries:
        outfile = os.path.join(args.output, f.filename)
        dirname = os.path.dirname(outfile)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        print("Writing {}...".format(outfile))
        with open(outfile, "wb+") as output:
            output.write(f.data)