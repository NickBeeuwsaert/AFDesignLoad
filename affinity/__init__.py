#!/usr/bin/env python
from collections import namedtuple
import struct
from datetime import datetime
import zlib

Header = namedtuple('Header', ('signature', 'version', 'offsets', 'creation_date'))
unpack = lambda f, fmt: struct.unpack(fmt, f.read(struct.calcsize(fmt)))
#FATHeader = namedtuple('FATHeader', 'unused timestamp flags offset_1 offset_2 offset_3 offseet_4 fat_length idk')


class FATEntry(object):
    def __init__(self, idk, offset, real_len, c_len, date, compressed, fname_len, filename, data):
        self.idk = idk
        self.offset = offset
        self.real_len = real_len
        self.c_len = c_len
        self.date = date
        self.compressed = compressed
        self.fname_len = fname_len
        self.filename = filename
        self.data = data
        print("""
            date: {}
            start: {}
            length: {}
            compressed: {}
            filename: {}""".format(
                self.date,
                self.offset,
                self.c_len,
                not not self.compressed,
                self.filename)
            )
        

    @staticmethod
    def create_from_file(f):
        idk = unpack(f, "<5s")
        data_offset, real_len, data_len, date, compressed,fname_len = unpack(f, "<3QI?H")
        date = datetime.fromtimestamp(date)
        filename, = unpack(f, "<{}s".format(fname_len))
        filename = filename.decode('utf8')

        #save the file location
        pos = f.tell()
        f.seek(data_offset)
        fil_sig, = unpack(f, "<4s")
        assert fil_sig == b'#Fil'
        data = f.read(data_len)

        if compressed:
            data = zlib.decompress(data)
        #restore position
        f.seek(pos)
        return FATEntry(idk, data_offset, real_len, data_len, date, compressed, fname_len, filename, data)


class FATHeader(object):
    def __init__(self, flags, date, unused, offsets, length, unused_2):
        self.flags = flags
        self.date = date
        self.unused = unused, unused_2
        self.offsets = offsets
        self.fat_length = length
        print("""
            date:       {}
            offsets:    {}
            FAT length: {}""".format(self.date, self.offsets, self.fat_length))

    @staticmethod
    def create_from_file(f):
        flags, timestamp, unused = unpack(f, "<QII")
        timestamp = datetime.fromtimestamp(timestamp)
        offsets = unpack(f, "<4Q")
        fat_length, unused_2 = unpack(f, "<H5s")
        return FATHeader(flags, timestamp, unused, offsets, fat_length, unused_2)


class AffinityFile(object):
    def __init__(self, filename):
        f = open(filename, 'rb')
        #self.headers = Header(*unpack(f, "<III"))
        signature, version, prsn = unpack(f, "<2I4s")
        assert prsn == b'nsrP', "This doesn't look like an AffinityDesigner file!"

        inf, = unpack(f, "<4s")
        assert inf == b'#Inf', 'Expected #Inf section!'


        offsets = unpack(f, "<4Q")
        timestamp, = unpack(f, "<I")
        timestamp = datetime.fromtimestamp(timestamp)

        self.header = Header(signature, version, offsets, timestamp)

        self.uh = unpack(f, "<IQQ")
        fat_offset, fat_end, _, _ = offsets

        # Seek to the FAT Section and start reading data

        f.seek(fat_offset)
        fat_flag, = unpack(f, "<4s")
        assert fat_flag == b'#FAT'
        fh = FATHeader.create_from_file(f)

        self.documents = {}
        for i in range(fh.offsets[-1]):
            entry = FATEntry.create_from_file(f)
            self.documents[entry.filename] = entry

        # For when we get to reading the layers
        self.layers = {}
