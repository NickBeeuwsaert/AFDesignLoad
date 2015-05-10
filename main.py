#!/usr/bin/env python3
import struct
import argparse
from datetime import datetime
from collections import namedtuple
import os.path

unpack = lambda f, fmt: struct.unpack(fmt, f.read(struct.calcsize(fmt)))

Header = namedtuple(
    'AFDesignHeader',
    (
        'signature',
        'version',
        'inexplicably_prsn'
    )
)

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

#    header = Header(*unpack(inp, "<II4s"))
#
#    print("""
#        Signature:         {h.signature:08x}
#        Version:           {h.version}
#        Inexplicably Prsn: {h.inexplicably_prsn}
#    """.format(h=header))
#
#    offsets = []
#    chunk, = unpack(inp, "<4s")
#    assert(chunk == "#Inf")
#
#    fat_offset, fat_length, maybe_fil_length, zero = unpack(inp, "<4Q");
#    print("""
#            FAT at: {},
#            Length: {},
#            As of yet, still undiscovered offset: {}
#            usually zero: {}
#            """.format(fat_offset, fat_length - fat_offset, maybe_fil_length, zero))
#    timestamp, = unpack(inp, "<I")
#    print("Creation date: {:%Y-%m-%d %H:%M:%S}".format(datetime.fromtimestamp(timestamp)))
#    print("Creation date: {}".format(datetime.fromtimestamp(timestamp).isoformat()))
#
#
#    inp.seek(fat_offset)
#    fat = inp.read(fat_length - fat_offset)
#    print("Read FAT!");
#
#    #if unpack(inp, '<4s') == ('#Inf',):
#    #    print("Reading offsets...")
#    #    while True:
#    #        offset, = unpack(inp, "<Q")
#    #        print(offset)
#    #        if offset == 0: break
#    #        offsets += [offset]
#
#    #print(offsets)
