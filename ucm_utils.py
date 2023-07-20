"""
A stripped down version of the rucm function from
Tom Marsh's ultracam pipeline:

https://github.com/trmrsh/trm-ultracam

Renamed here to read_ucm, this allows phot2lc to 
open .ucm files for plotting purposes.
"""

import struct
import numpy as np

# Integer type numbers
ITYPE_DOUBLE    = 0
ITYPE_CHAR      = 1
ITYPE_INT       = 2
ITYPE_UINT      = 3
ITYPE_LINT      = 4
ITYPE_ULINT     = 5
ITYPE_FLOAT     = 6
ITYPE_STRING    = 7
ITYPE_BOOL      = 8
ITYPE_DIR       = 9
ITYPE_DATE      = 10
ITYPE_TIME      = 11
ITYPE_POSITION  = 12
ITYPE_DVECTOR   = 13
ITYPE_UCHAR     = 14
ITYPE_TELESCOPE = 15
ITYPE_USINT     = 16
ITYPE_IVECTOR   = 17
ITYPE_FVECTOR   = 18

# ucm magic number
MAGIC           = 47561009

def check_ucm(fobj):
    """
    Check a file opened for reading in binary mode to see if it is a ucm.
    Returns endian which is a string to be passed
    to later routines indicating endian-ness.
    """

    # read the format code
    fbytes = fobj.read(4)
    fcode  = struct.unpack('i',fbytes)[0]
    if fcode != MAGIC:
        fcode = struct.unpack('>i',fbytes)[0]
        if fcode != MAGIC:
            fobj.close()
            raise('UltracamError: check_ucm: could not recognise first 4 bytes of ' +
                                fname + ' as a ucm file')
        endian = '>'
    else:
        endian = '<'
    return endian


def read_string(fobj, endian=''):
    """
    Reads a string written in binary format by my C++ code
    fobj   -- file object opened for binary input
    endian -- '>' for big-endian, '' for little-endian.
    """
    nchar  = struct.unpack(endian + 'i', fobj.read(4))[0]
    strng  = struct.unpack(endian + str(nchar) + 's', fobj.read(nchar))[0]
    return strng.decode('utf-8')


def read_ucm(fname, flt=True):
        """
        Factory method to produce an MCCD from a ucm file.
        fname -- ucm file name. '.ucm' will be appended if not supplied.
        flt    -- convert to 4-byte floats whatever the input data, or not. ucm
                  files can either contain 4-bytes floats or for reduced disk
                  footprint, unsigned 2-byte integers. If flt=True, either type
                  will end up as float32 internally. If flt=False, the disk type
                  will be retained. The latter is unsafe when arithematic is involved
                  hence the default is to convert to 4-byte floats.
        Exceptions are thrown if the file cannot be found, or an error during the
        read occurs.
        """    

        # Assume it is a file object, if that fails, assume it is
        # the name of a file.
        if not fname.endswith('.ucm'): fname += '.ucm'
        uf = open(fname, 'rb')
        start_format = check_ucm(uf)

        # read the header
        lmap = struct.unpack(start_format + 'i', uf.read(4))[0]

        head = {}
        for i in range(lmap):
            name    = read_string(uf, start_format)
            itype   = struct.unpack(start_format + 'i', uf.read(4))[0]
            comment = read_string(uf, start_format)

            if itype == ITYPE_DOUBLE:
                value = struct.unpack(start_format + 'd', uf.read(8))[0]
            elif itype == ITYPE_INT:
                value = struct.unpack(start_format + 'i', uf.read(4))[0]
            elif itype == ITYPE_UINT:
                value = struct.unpack(start_format + 'I', uf.read(4))[0]
            elif itype == ITYPE_FLOAT:
                value = struct.unpack(start_format + 'f', uf.read(4))[0]
            elif itype == ITYPE_STRING:
                value = read_string(uf, start_format)
            elif itype == ITYPE_BOOL:
                value = struct.unpack(start_format + 'B', uf.read(1))[0]
            elif itype == ITYPE_DIR:
                value = None
            elif itype == ITYPE_TIME:
                value = struct.unpack(start_format + 'id', uf.read(12))
            elif itype == ITYPE_DVECTOR:
                nvec  = struct.unpack(start_format + 'i', uf.read(4))[0]
                value = struct.unpack(start_format + str(nvec) + 'd', uf.read(8*nvec))
            elif itype == ITYPE_UCHAR:
                value = struct.unpack(start_format + 'c', uf.read(1))[0]
            elif itype == ITYPE_USINT:
                value = struct.unpack(start_format + 'H', uf.read(2))[0]
            elif itype == ITYPE_IVECTOR:
                nvec  = struct.unpack(start_format + 'i', uf.read(4))[0]
                value = struct.unpack(start_format + str(nvec) + 'i', uf.read(4*nvec))
            elif itype == ITYPE_FVECTOR:
                nvec  = struct.unpack(start_format + 'i', uf.read(4))[0]
                value = struct.unpack(start_format + str(nvec) + 'f', uf.read(4*nvec))
            else:
                raise('UltracamError: do not recognize itype = ' + str(itype))
                
            # store header information, fast method
            head[name] = [value,comment]


        # read number of CCDs
        nccd = struct.unpack(start_format + 'i', uf.read(4))[0]
        
        # read number of wndows
        nwin = struct.unpack(start_format + 'i', uf.read(4))[0]
        
        if (nccd > 1) | (nwin > 1):
            uf.close()
            return None,None
        
        else:
            llx,lly,nx,ny,xbin,ybin,nxmax,nymax,iout = struct.unpack(start_format + '9i', uf.read(36))
            if iout == 0:
                win = np.fromfile(file=uf, dtype=np.float32, count=nx*ny)
            elif iout == 1:
                if flt:
                    win = np.fromfile(file=uf, dtype=np.uint16, count=nx*ny).astype(np.float32)
                else:
                    win = np.fromfile(file=uf, dtype=np.uint16, count=nx*ny)
            else:
                raise(f'UltracamError: iout = {iout} not recognised')
            win = win.reshape((ny,nx))            

            uf.close()
            return win, head