import struct

# Unpack in big-endian order so that they
# will be flipped aproppriately
MARGIN,           = struct.unpack('>I', b'Mrgn')
DATA,             = struct.unpack('>I', b'Data')
ROOT,             = struct.unpack('>I', b'Root')
DESCRIPTION,      = struct.unpack('>I', b'Desc')
BITMAP_WIDTH,     = struct.unpack('>I', b'BmpH')
BITMAP_HEIGHT,    = struct.unpack('>I', b'BmpW')
BITMAP,           = struct.unpack('>I', b'Bitm')
VISIBILITY,       = struct.unpack('>I', b'Visi')
OPACITY,          = struct.unpack('>I', b'Opac')
NODE,             = struct.unpack('>I', b'Node')
FIRST,            = struct.unpack('>I', b'Frst')
SECOND,           = struct.unpack('>I', b'Scnd')
COLOR,            = struct.unpack('>I', b'Colr')
COLOR_DEFINITION, = struct.unpack('>I', b'ColD')
BLEND_MODE,       = struct.unpack('>I', b'Blnd')
XMP_DATA,         = struct.unpack('>I', b'XMPD')