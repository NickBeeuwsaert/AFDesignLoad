=====================
.afdesign file format
=====================
.. include:: <isonum.txt>

Values are stored in little-endian format

I haven't seen anything that actually looks like a flags field, usually
there are a few boolean feilds so idk what some of these fields are for

Header
======

Size: 68 bytes? Variable length?

+----------------+---------+-------------+---------------------------+
| name           | Count   | Type        | Description               |
+================+=========+=============+===========================+
| signature      |         |             | Signature?                |
+----------------+    1    +  uint32\_t  +---------------------------+
| version        |         |             | Poseinfo                  |
+----------------+---------+-------------+---------------------------+
| unused         |         |             | Prsn? (Personas?)         |
+----------------+    4    +     char    +---------------------------+
| info           |         |             | #Inf - File offsets?      |
+----------------+---------+-------------+---------------------------+
| FAT\_offset    |         |             | See Notes on offset       |
+----------------+         +             +---------------------------+
| FAT\_length    |         |             | See Notes on offset       |
+----------------+         + uint64\_t   +---------------------------+
| zlib\_length   |         |             | See Notes on offset       |
+----------------+         +             +---------------------------+
| unused         |         |             | See Notes on offset       |
+----------------+    1    +-------------+---------------------------+
| creation       |         |             | Date                      |
+----------------+         + uint32\_t   +---------------------------+
| unused         |         |             | for some reason zero      |
+----------------+         +-------------+---------------------------+
| fat\_entries   |         |             | Fat or info sections      |
+----------------+         + uint64\_t   +---------------------------+
| fil\_entries   |         |             | Number of #fil secions?   |
+----------------+---------+-------------+---------------------------+

\* *This is a guess*

Notes
-----

offsets
~~~~~~~

It looks like the first number encountered in the offsets is the
location of the #FAT section

The second section I still can't figure out what it does, but it looks
like the offset to the thumbnail (changing the location of the thumbnail
and setting this to the new location doesn't break the preview),

The third header looks like the length of the compressed data starting
at #Fil, But when there are more than one #FIL section idk what this
means

it looks the the ``#Fil`` and ``#FAT`` sections are ended with
``0xFFFFFFFF``

Idk what the data before the #FIL is, I thought it was compresion level
but if I have embedded images its like 57

#FAT section
============

Ok so, the data ends in the file name or something? a short will
indicate the length of the filename?

It looks like this section will define the offset of the #Fil sections
and their length

Looks like a entry starts with one byte, a 64 bit nubmer and a timestap

It looks like each section starts with 1 byte for flags, then a 8 byte
timestamp

|darr| This might be the FAT header? |darr|

+---------------+---------+-------------+---------------------------------+
| name          | count   | Type        | description                     |
+===============+=========+=============+=================================+
| flags         |         |  uint64\_t  | Flags?                          |
+---------------+         +-------------+---------------------------------+
| date          | 1       |             | UNIX timestamp                  |
+---------------+         +  uint32\_t  +---------------------------------+
| flags         |         |             | more flags                      |
+---------------+---------+-------------+---------------------------------+
| offsets       | 4       |  uint64\_t  | offsets                         |
+---------------+---------+-------------+---------------------------------+
| fat\_length   | 1       |  uint16\_t  | The length of the fat section   |
+---------------+---------+-------------+---------------------------------+
| idk           | 3       | char        |                                 |
+---------------+---------+             +---------------------------------+
| idk           | 2       |             |                                 |
+---------------+---------+-------------+---------------------------------+

^ I am pretty sure this is misaligned, there are more pad/flag bytes
than I want, so I'm probably missing something. Also doc.dat occurs at
the end of the file so this might be half a entry?

Also, the last offset could very well be the number of entries

Sometimes the timestamp seems to be wildly off, but was the file
creation date for the doc.dat

it looks like only one file will have a reliable name ("doc.dat"), and
other files will be in a directory structure (d/a, d/c, b/a...)

+----------------+------------+-------------+----------------------------------------+
| name           |  count     | type        | description                            |
+================+============+=============+========================================+
| idk            |            | uint32\_t   | idk. It's always zero?                 |
+----------------+            +-------------+----------------------------------------+
| idk\_Again     |            | bool        | looks like a bitfield or a number...   |
+----------------+            +-------------+----------------------------------------+
| data\_offset   |            |             | The offset of the data                 |
+----------------+            +             +----------------------------------------+
| real\_len      |            |  uint64\_t  | uncompressed length                    |
+----------------+    1       +             +----------------------------------------+
| data\_len      |            |             | The lengh of the chunk                 |
+----------------+            +-------------+----------------------------------------+
| date           |            | uint32\_t   | the date                               |
+----------------+            +-------------+----------------------------------------+
| compressed     |            | bool        | if the chunk is compressed             |
+----------------+            +-------------+----------------------------------------+
| fname\_len     |            | uint16\_t   | The filename length                    |
+----------------+------------+-------------+----------------------------------------+
| filename       |*fname\_len*| char        | The filename                           |
+----------------+------------+-------------+----------------------------------------+

doc.dat and associated crap
===========================

It looks like the tags were converted to 32-bit integers to be stored
(as they have some meaning when reversed) Also: Each tag looks to be
preceded by a number, idk what that is for yet I'm not counting it until
I know what its for....

.. code-block:: c
  :linenos:

  #include <stdio.h>
  #include <stdint.h>

  int main(){
    union {
      uint32_t tag;
      char name[4];
    };
    strncpy(name, "Prsn", 4);
    printf("0x%X\n", tag);
    // On a little endian system, this should output
    // 0x6E737250
    return 0;
  }

I suspect there is some inspiration taken from the PNG file format with data in the capitalization of the chunk name

BrpS (SprB) (Document properties?)
----------------------------------


Total size: 36 bytes

+-------+-------+-----------+-------------------------------+
| name  | count |  type     | description                   |
+=======+=======+===========+===============================+
| BrpS  |   1   | uint32\_t | Dimension info                |
+-------+-------+-----------+-------------------------------+
|  ?    |   2   |           | Idk? looks to be zero usually |
|       |       |           | Maybe some offset info        |
|       |       |           | like x and y offset           |
|       |       |  double   | maybe w\ |times|\ h+x+y       |
+-------+-------+           +-------------------------------+
| width |   1   |           | Width                         |
+-------+       +           +-------------------------------+
| height|       |           | Height                        |
+-------+-------+-----------+-------------------------------+

capO (Opac)
-----------

Total size: 8 bytes

+-----------+---------+-------------+------------------------------+
| name      | count   | type        | Descrpition                  |
+===========+=========+=============+==============================+
| Opac      | 1       | uint32\_t   | Tag                          |
+-----------+         +-------------+------------------------------+
| opacity   |         | float       | The opacity of the element   |
+-----------+---------+-------------+------------------------------+

isiV (Visi)
-----------

Total Size: 5 Bytes

+-----------+---------+-------------+-----------------------------+
| name      | count   | type        | Descrpition                 |
+===========+=========+=============+=============================+
| Visi      | 1       | uint32\_t   | The tag                     |
+-----------+         +-------------+-----------------------------+
| visible   |         | bool        | visibility of the element   |
+-----------+---------+-------------+-----------------------------+

cseD (Desc)
-----------

Total Size: variable (smallest is 6 bytes)

+--------+---------+-------------+------------------------+
| name   | count   | type        | Descrpition            |
+========+=========+=============+========================+
| Desc   | 1       | uint32\_t   | The tag                |
+--------+         +-------------+------------------------+
| size   |         | uint16\_t   | Length of the name     |
+--------+---------+-------------+------------------------+
| name   | *size*  | char        | The name of the Desc   |
+--------+---------+-------------+------------------------+

ngrM (Mrgn)
-----------

This field is speculation, I haven't gotten time to look at it yet But,
based on the size of the data I am assuming. the order may be incorrect
(assuming it follows the order like CSS...) Total size: 36bytes

+----------+---------+----------+-----------------+
| name     | count   | type     | Descrpition     |
+==========+=========+==========+=================+
| Mrgn     |         | char     | The Tag         |
+----------+         +----------+-----------------+
| top      |         |          | Top margin      |
+----------+         +          +-----------------+
| left     |    1    |          | Left margin     |
+----------+         +  double  +-----------------+
| bottom   |         |          | Bottom margin   |
+----------+         +          +-----------------+
| right    |         |          | Right margin    |
+----------+---------+----------+-----------------+

ataD (Data)
-----------

Total Size: variable (smallest is 6 bytes)

+--------+---------+-------------+----------------------+
| name   |  count  | type        | Descrpition          |
+========+=========+=============+======================+
| Data   |         | uint32\_t   | The tag              |
+--------+    1    +-------------+----------------------+
| size   |         | uint16\_t   | Length of the data   |
+--------+---------+-------------+----------------------+
| data   | *size*  | byte        | The data             |
+--------+---------+-------------+----------------------+

tooR (Root)
-----------

Speculation, again. Presumably the offset of the root node Total Size: 8
bytes

+----------+---------+-------------+-----------------------+
| name     |  count  | type        | Descrpition           |
+==========+=========+=============+=======================+
| Root     |         |             | The tag               |
+----------+    1    +  uint32\_t  +-----------------------+
| offset   |         |             | Offset to Root node   |
+----------+---------+-------------+-----------------------+

NgoL (Logarithm in base N?)
---------------------------
Ok, to be honest I have no clue what this means. I don't know how long it is, 
as I can't figure out where the length is specified

grOU (Groups)
-------------
Groups?

WpmB (Bitmap width)
-------------------
Width of a bitmap

+----------+---------+-------------+-----------------------+
| name     |  count  | type        | Descrpition           |
+==========+=========+=============+=======================+
| tag      |    1    | uint32_t    | WpmB                  |
+----------+---------+-------------+-----------------------+
| width    |    1    | uint32_t    | Width                 |
+----------+---------+-------------+-----------------------+


HpmB (Bitmap Height)
--------------------
Height of a bitmap

+----------+---------+-------------+-----------------------+
| name     |  count  | type        | Descrpition           |
+==========+=========+=============+=======================+
| tag      |    1    | uint32_t    | HpmB                  |
+----------+---------+-------------+-----------------------+
| height   |    1    | uint32_t    | Height                |
+----------+---------+-------------+-----------------------+

Bitm (Bitmap)
-------------

+----------+---------+-------------+-----------------------+
| name     |  count  | type        | Descrpition           |
+==========+=========+=============+=======================+
| tag      |         | uint32_t    | Bitm                  |
+----------+         +-------------+-----------------------+
| flag     |    1    |   bool      | boolean               |
+----------+         +-------------+-----------------------+
| size?    |         | uint32_t    |                       |
+----------+---------+-------------+-----------------------+


tmrF (Format)
-------------

+----------+---------+-------------+-----------------------+
| name     |  count  | type        | Descrpition           |
+==========+=========+=============+=======================+
| tag      |    1    | uint32_t    | Frmt                  |
+----------+---------+-------------+-----------------------+
| flag     |    1    | unit32_t    | Format?               |
+----------+---------+-------------+-----------------------+
