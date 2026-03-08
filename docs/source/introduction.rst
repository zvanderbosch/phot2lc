Introduction
============

* `What is phot2lc?`_
* `Currently Supported Photometry Pipelines`_
* `Currently Supported Telescopes`_


What is phot2lc?
----------------

**phot2lc** is a program that ingests the output from various photometry pipelines and provides users with a set of tools to extract and manipulate divided light curves. It is largely inspired by `WQED <https://ui.adsabs.harvard.edu/abs/2009JPhCS.172a2081T/abstract>`_, and provides functionality such as comparison star selection, aperture size selection, removing poor-quality data, polynomial fitting, and barycentric time corrections.


Currently Supported Photometry Pipelines
----------------------------------------

**phot2lc** can be configured to work with the outputs from a variety of photometry pipelines. Currently supported pipelines include:

* ccd_hsp (`Kanaan et al. 2002 <https://ui.adsabs.harvard.edu/abs/2002A%26A...389..896K/abstract>`_, source code = hsp)
* MAESTRO (`Dalessio 2010 <https://ui.adsabs.harvard.edu/abs/2010AAS...21545209D/abstract>`_, `2013 <https://ui.adsabs.harvard.edu/abs/2013PhDT.......170D/abstract>`_, source code = mae)
* ULTRACAM (`Dhillon et al. 2007 <https://ui.adsabs.harvard.edu/abs/2007MNRAS.378..825D/abstract>`_, source code = ucm)
* HiPERCAM (`Dhillon et al. 2021 <https://ui.adsabs.harvard.edu/abs/2021MNRAS.507..350D/abstract>`_, source code = hcm)

If your preferred photometry pipeline is not listed here, please :ref:`contact Zach Vanderbosch<Contact>` about adding support for it in **phot2lc**.


Currently Supported Telescopes
------------------------------

**phot2lc** also loads in one or more of the actual images (FITS, ucm, or hcm format), both for display purposes and to grab some key header information such as observer name, filter name, exposure time, observation timestamps, etc. For different telescopes and instruments, the header keywords may have different names or the timestamps may have different formats, so **phot2lc** needs to be properly configured to read the FITS images from each telescope/instrument. This is done by specifying a telescope code, which also specifies to phot2lc the site longitude, latitude, and elevation in order to perform barycentric time corrections.

The following telescopes/instruments are currently supported, and their phot2lc telescope codes shown on the left:

```
adu60  = ADU60 at Adiyaman Observatory, Turkey Andor CCD/EMCCD (SDK2)
amag   = Amagi Observatory E-4240bi
ap05   = ARCSAT 0.5m at Apache Point dcam-spare
bake   = Baker Observatory 20 inch, CDK20 Apogee USB/Net
bnt    = Xinglong 0.85m telescope, BNT Andor Tech
cdk500 = CDK500 at Krakow Apogee USB/Net
coud   = McDonald 2.7m Coude Guide
dot    = 3.5m DOT at ARIES TIRCAM2
hao    = HAO68 at Horten Observatory, Norway Moravian Instruments, G2-1600 MkII
kped   = KPED 2.1m KPED
krak50 = Krakow 50 cm QHY-600M
lco1   = LCOGT 1.0m Sinistro
luli   = Lulin 1m, LOT Andor CCD/EMCCD (SDK2)
mcd2   = McDonald 2.1m ProEM
oanspm = OAN-SPM 1.5m CAMILA
opd    = OPD 1.6m Cam1+Ixon
opd16  = SPARC4 on OPD 1.6m SPARC4
p200   = Palomar 200in CHIMERA
pat    = Nanshan 0.43m telescope, PAT QHYCCD-Cameras2-Capture
perk   = Perkins 1.8m PRISM
pisz   = 1m RCC Telescope at Piszkéstető Observatory, Hungary sicamera
pjmo   = PJMO 0.6m Roper PVCAM
sact   = SARA CT Andor Camera
sakp   = SARA KP Arc Camera
sakt   = SARA KP Arc Camera
sarm   = SARA RM SARA-RM Andor Ikon-L
stew   = 61 inch Mt. Bigelow mont4k
suho   = Mt. Suhora Obs. Small Dome SBIG ST-10 Dual CCD Camera
tnt    = Xinglong 0.8m telescope, TNT CCD
tshao  = Zeiss-1000 (1m) at Tian Shan Astronomical Observatory FLI
tueb   = Tuebingen Observatory 0.8m SBIG STL-1001 3 CCD Camera
tymce  = Remote 14inch run by Krakow Observatory, by Ukraine border ASI Camera
uh88   = STACam on the UH88 STACam
unca   = Lookout Observatory 14inch, UNCA ASCOM Camera
warw   = Warwaick remote 1-meter at RM CCD
xing60 = Xinglong 0.6m telescope CCD
```


If your preferred telescope+instrument is not listed here, please :ref:`contact Zach Vanderbosch<Contact>` about adding support for it in **phot2lc**. In this case, however, users may find it relatively easy to add support for a new instrument themselves by adding a new entry into the "teledat.py" script that is installed with **phot2lc**.
