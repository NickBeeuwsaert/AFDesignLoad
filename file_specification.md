# .afdesign file format
Values are stored in little-endian format

I haven't seen anything that actually looks like a flags field, usually there are a few boolean feilds so idk what some of these fields are for

## Header

Size: 68 bytes? Variable length?


|     name    |    Count    |    Type   | Description                |
|:-----------:|:-----------:|:---------:|----------------------------|
| signature   |      1      | uint32_t  | Signature?                 |
| version     |      1      | uint32_t  | Poseinfo                   |
| unused      |      4      |    char   | Prsn? (Personas?)          |
| info        |      4      |    char   | #Inf - File offsets?       |
| FAT_offset  |      1      | uint64_t  | See Notes on offset        |
| FAT_length  |      1      | uint64_t  | See Notes on offset        |
| zlib_length |      1      | uint64_t  | See Notes on offset        |
| unused      |      1      | uint64_t  | See Notes on offset        |
| creation    |      1      | uint32_t  | Date                       | 
| unused      |      1      | uint32_t  | for some reason zero       |
| fat_entries |      1      | uint64_t  | Fat or info sections       |
| fil_entries |      1      | uint64_t  | Number of #fil secions?    |

\* _This is a guess_

## Notes
### offsets
It looks like the first number encountered in the offsets is the location of the #FAT section

The second section I still can't figure out what it does, but it looks like the offset to the thumbnail (changing the location of the thumbnail and setting this to the new location doesn't break the preview), 

The third header looks like the length of the compressed data starting at #Fil, But when there are more than one #FIL section idk what this means

it looks the the `#Fil` and `#FAT` sections are ended with `0xFFFFFFFF`

Idk what the data before the #FIL is, I thought it was compresion level but if I have embedded images its like 57

#\#FAT section
Ok so, the data ends in the file name or something? a short will indicate the length of the filename?

It looks like this section will define the offset of the #Fil sections and their length

<strike>Looks like a entry starts with one byte, a 64 bit nubmer and a timestap</strike>

<strike>It looks like each section starts with 1 byte for flags, then a 8 byte timestamp</strike>

\/ This might be the FAT header? \/

|    name    | count |   Type   |  description                          |
|:----------:|:-----:|:--------:|---------------------------------------|
|    flags   |   1   | uint64_t | Flags?                                |
|    date    |   1   | uint32_t | UNIX timestamp                        |
|    flags   |   1   | uint32_t | more flags                            |
|   offsets  |   4   | uint64_t | offsets                               |
| fat_length |   1   | uint16_t | The length of the fat section         |
|    idk     |   3   |   char   |                                       |
|    idk     |   2   |   char   |                                       |


^ I am pretty sure this is misaligned, there are more pad/flag bytes than I want, so I'm probably missing something. Also doc.dat occurs at the end of the file so this might be half a entry? 

Also, the last offset could very well be the number of entries

Sometimes the timestamp seems to be wildly off, but was the file creation date for the doc.dat

it looks like only one file will have a reliable name ("doc.dat"), and other files will be in a directory structure (d/a, d/c, b/a...)


|    name    | count |   type   | description                           |
|------------|:-----:|:--------:|---------------------------------------|
| idk        |   1   | uint32_t | idk. It's always zero?                |
| idk_Again  |   1   |   bool   | looks like a bitfield or a number...  |
| data_offset|   1   | uint64_t | The offset of the data                |
|  real_len  |   1   | uint64_t | uncompressed length                   |
|  data_len  |   1   | uint64_t | The lengh of the chunk                |
|    date    |   1   | uint32_t | the date                              |
| compressed |   1   |   bool   | if the chunk is compressed            |
|  fname_len |   1   | uint16_t | The filename length                   |
|  filename  |   *   |   char   | The filename                          |

## doc.dat and associated crap
It looks like the tags were converted to 32-bit integers to be stored (as they have some meaning when reversed)
Also: Each tag looks to be preceded by a number, idk what that is for yet
I'm not counting it until I know what its for....

# BrpS (SprB) (Document properties?)
Total size: 36 bytes
| name  | count |   type   | description                   |
|:-----:|:-----:|:--------:|-------------------------------|
| BrpS  |   1   | uint32_t | Dimension info                |
|  ?    |   2   |  double  | Idk? looks to be zero usually |
| width |   1   |  double  | Width                         |
| height|   1   |  double  | Height                        |

# capO (Opac)
Total size: 8 bytes

|   name  | count |   type   | Descrpition                   |
|:-------:|:-----:|:--------:|-------------------------------|
| Opac    |   1   | uint32_t | Tag                           |
| opacity |   1   |   float  | The opacity of the element    |

# isiV (Visi)
Total Size: 5 Bytes

|   name  | count |   type   | Descrpition                   |
|:-------:|:-----:|:--------:|-------------------------------|
| Visi    |   1   | uint32_t | The tag                       |
| visible |   1   |   bool   | visibility of the element     |


# cseD (Desc)
Total Size: variable (smallest is 6 bytes)

|   name  | count |   type   | Descrpition                   |
|:-------:|:-----:|:--------:|-------------------------------|
| Desc    |   1   | uint32_t | The tag                       |
| size    |   1   | uint16_t | Length of the name            |
| name    |  size | char     | The name of the Desc          |

# ngrM (Mrgn)
This field is speculation, I haven't gotten time to look at it yet
But, based on the size of the data I am assuming. the order may be incorrect (assuming it follows the order like CSS...)
Total size: 36bytes

|   name  | count |   type   | Descrpition                   |
|:-------:|:-----:|:--------:|-------------------------------|
| Mrgn    |   1   |    1     | The Tag                       |
| top     |   1   |  double  | Top margin                    |
| left    |   1   |  double  | Left margin                   |
| bottom  |   1   |  double  | Bottom margin                 |
| right   |   1   |  double  | Right margin                  |

# ataD (Data)
Total Size: variable (smallest is 6 bytes)

|   name  | count |   type   | Descrpition                   |
|:-------:|:-----:|:--------:|-------------------------------|
| Data    |   1   | uint32_t | The tag                       |
| size    |   1   | uint16_t | Length of the data            |
| data    |  size | byte     | The data                      |

# tooR (Root)
Speculation, again. Presumably the offset of the root node
Total Size: 8 bytes

|   name  | count |   type   | Descrpition                   |
|:-------:|:-----:|:--------:|-------------------------------|
|   Root  |   1   | uint32_t | The tag                       |
|  offset |   1   | uint32_t | Offset to Root node           |
