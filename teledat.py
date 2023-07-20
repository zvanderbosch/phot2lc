import numpy as np

"""
Script containing information for each
telescope

Author: 
    Zach Vanderbosch

For a description of updates, see the 
version_history.txt file.
"""

# For new entries, follow the given format:
#
# telename: Name of telescope used
# instname: Name of instrument used
# code    : 4-letter code for this entry
# objname : FITS keyword for name of the object observed (None if unavailable or unused)
# filter  : FITS keyword for filter used for observations
# observer: FITS keyword for name or initials of observer
# date    : FITS keyword for UTC date of observation
# time    : FITS keyword for UTC time of observation (None if unavailable or unused)
# texp    : FITS heyword for exposure time of observation
# dformat : number describing the date format
#               0 = YYYY MM DD with any kind of separator
#               1 = YYYY-MM-DDThh:mm:ss (ISOT format)
#               2 = Julian Date
# tformat : number describing the time format
#               0 = hh mm ss with any kind of separator and 
#                   with or without fractional seconds
#               1 = get time from date when dformat = 1 or 2
# dark    : Dark noise for instrument in e-/s/pixel or ADU/s/pixel (np.nan if unavailable)
# read    : Read noise for instrument in e-/pixel or ADU/pixel (np.nan if unavailable)
# gain    : Gain in e-/ADU if read and dark are in e- units. or 1.0 otherwise


def get_telinfo():

    tele_info = [

    {"telename":"McDonald 2.1m",
     "instname":"ProEM",
     "code"    :"mcd2",
     "objname" :"OBJECT",
     "filter"  :"FILTER",
     "observer":"OBSERVER",
     "date"    :"DATE-OBS",
     "time"    :"TIME-OBS",
     "texp"    :"EXPTIME",
     "dformat" :0,
     "tformat" :0,
     "dark"    :1.6,
     "read"    :6.1,
     "gain"    :0.87},

    {"telename":"McDonald 2.7m",
     "instname":"Coude Guide",
     "code"    :"coud",
     "objname" :"OBJECT",
     "filter"  :"FILTER",
     "observer":"OBSERVER",
     "date"    :"DATE-OBS",
     "time"    :"UT",
     "texp"    :"EXPTIME",
     "dformat" :0,
     "tformat" :0,
     "dark"    :np.nan,
     "read"    :np.nan,
     "gain"    :1.00},

    {"telename":"Perkins 1.8m",
     "instname":"PRISM",
     "code"    :"perk",
     "objname" :None,
     "filter"  :"FILTNME3",
     "observer":"OBSERVER",
     "date"    :"DATE-OBS",
     "time"    :None,
     "texp"    :"EXPTIME",
     "dformat" :1,
     "tformat" :1,
     "dark"    :np.nan,
     "read"    :np.nan,
     "gain"    :1.00},

    {"telename":"PJMO 0.6m",
     "instname":"Roper PVCAM",
     "code"    :"pjmo",
     "objname" :"OBJECT",
     "filter"  :"FILTER",
     "observer":"OBSERVER",
     "date"    :"JD",
     "time"    :None,
     "texp"    :"EXPTIME",
     "dformat" :2,
     "tformat" :1,
     "dark"    :np.nan,
     "read"    :12.96,
     "gain"    :1.73},
    
    {"telename":"LCOGT 1.0m",
     "instname":"Sinistro",
     "code"    :"lco1",
     "objname" :"OBJECT",
     "filter"  :"FILTER",
     "observer":"USERID",
     "date"    :"DATE-OBS",
     "time"    :None,
     "texp"    :"EXPTIME",
     "dformat" :1,
     "tformat" :1,
     "dark"    :0.002,
     "read"    :7.60,
     "gain"    :1.00},

     {"telename":"KPED 2.1m",
     "instname":"KPED",
     "code"    :"kped",
     "objname" :"OBJECT",
     "filter"  :"FILTER",
     "observer":"OBSERVER",
     "date"    :"DATE-OBS",
     "time"    :"TIME-OBS",
     "texp"    :"EXPTIME",
     "dformat" :0,
     "tformat" :0,
     "dark"    :np.nan,
     "read"    :np.nan,
     "gain"    :1.00},

     {"telename":"Palomar 200in",
     "instname":"CHIMERA",
     "code"    :"p200",
     "objname" :"OBJECT",
     "filter"  :"FILTER",
     "observer":"OBSERVER",
     "date"    :"DATE-OBS",
     "time"    :"TIME-OBS",
     "texp"    :"EXPTIME",
     "dformat" :0,
     "tformat" :0,
     "dark"    :np.nan,
     "read"    :np.nan,
     "gain"    :1.00},

     {"telename":"OPD 1.6m",
     "instname":"Cam1+Ixon",
     "code"    :"opd",
     "objname" :"OBJECT",
     "filter"  :"FILTER",
     "observer":"OBSERVER",
     "date"    :"DATE-OBS",
     "time"    :None,
     "texp"    :"EXPTIME",
     "dformat" :1,
     "tformat" :1,
     "dark"    :np.nan,
     "read"    :np.nan,
     "gain"    :1.00},]

    return tele_info

