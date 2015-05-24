:mod:`affinity` --- Load Affinity Designer Files
================================================

.. danger::
    This module WILL change! Continue at your own risk!

.. class:: AffinityFile(file_path)

    Loads and parses an Affinity Designer File

    .. attribute:: header

        The file header info

    .. attribute:: layers

        a list containing the layers in the document

    .. attribute:: documents

        A dictionary containing all documents in the file

.. class:: FATHeader(flags, date, unused, offsets, length, unused_2)

    Parses a FAT header from the root AFD document

    :param int flags: the flags to the header has
    :param datetime.datetime date: the date the file was created
    :param unused: IDK yet
    :param tuple<int> offsets: Some offsets?
    :param int length: length of the FAT section
    :param unused_2: Yet more unused data

    .. staticmethod:: create_from_file(f)

        reads the data from a binary file-object and returns a new FATHeader

.. class:: FATEntry(idk, offset, real_len, c_len, date, compressed, fname_len, filename, data)

    Stores a FAT Entry

    :param idk: I do not know what this is yet
    :param int offset: Offset to the data
    :param int real_len: Length of the uncompressed data
    :param int c_len: Length of the compressed data
    :param datetime.datetime date: The timestamp of the entry
    :param bool compressed: Whether or not the data is compressed
    :param int fname_len: The length of the filename
    :param str filename: The filename
    :param bytes data: the entries file contents

    .. staticmethod:: create_from_file(f)

        parses a ``FATEntry`` from the file-object in ``f``

        :param file f: The file-object to use to crate the ``FATEntry``
