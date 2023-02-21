Introduction
============

* `What is phot2lc?`_
* `Currently Supported Photometry Pipelines`_
* `Currently Supported Telescopes`_


What is phot2lc?
----------------

First of all, **phot2lc** is *not* a photometry pipeline. Rather, **phot2lc** is a program that ingests the output from various photometric pipelines and provides users with a set of tools to extract and manipulate divided light curves. It is largely inspired by `WQED <https://ui.adsabs.harvard.edu/abs/2009JPhCS.172a2081T/abstract>`_, and provides functionality such as comparison star selection, aperture size selection, removing poor-quality data, polynomial fitting, and barycentric time corrections.


Currently Supported Photometry Pipelines
----------------------------------------

**phot2lc** will not automatically work with photometric data from all pipelines. Each pipeline will produce output with different content and formats, and **phot2lc** must be configured to properly ingest the data. Output from the following photometry pipelines is currently supported:

* ccd_hsp (`Kanaan et al. 2002 <https://ui.adsabs.harvard.edu/abs/2002A%26A...389..896K/abstract>`_)
* MAESTRO (`Dalessio 2010 <https://ui.adsabs.harvard.edu/abs/2010AAS...21545209D/abstract>`_, `2013 <https://ui.adsabs.harvard.edu/abs/2013PhDT.......170D/abstract>`_)
* ULTRACAM (`Dhillon et al. 2007 <https://ui.adsabs.harvard.edu/abs/2007MNRAS.378..825D/abstract>`_)
* HiPERCAM (`Dhillon et al. 2021 <https://ui.adsabs.harvard.edu/abs/2021MNRAS.507..350D/abstract>`_)

If your preferred photometry pipeline is not listed here, please :ref:`contact Zach Vanderbosch<Contact>` about adding support for it in **phot2lc**.


Currently Supported Telescopes
------------------------------

In addition to loading in outputs from photometric pipelines, **phot2lc** also loads in one or more of the actual images (FITS, ucm, or hcm format), both for display purposes and to grab some key header information such as observer name, filter name, exposure time, observation timestamps, etc. For different telescopes and instruments, the header keywords may have different names or the timestamps may have different formats, so **phot2lc** needs to be properly configured to read the data.

Data from the following telescopes/instruments are currently supported:

* McDonald 2.1m with ProEM EMCCD (telcode = mcd2)
* McDonald 2.7m with Coude Guide Camera (telcode = coud)
* Perkins 1.8m with PRISM (telcode = perk)
* Paul and Jane Meyer Observatory 0.6m with ProEM EMCCD (telcode = pjmo)
* Las Cumbres Observatory 1.0m with Sinistro (telcode = lco1)
* Kitt Peak 2.1m with KPED (telcode = kped)
* Palomar 200-in with CHIMERA (telcode = p200)
* Pico dos Dias Observatory 1.6m with Ixon Camera (telcode = opd)

If your preferred telescope+instrument is not listed here, please :ref:`contact Zach Vanderbosch<Contact>` about adding support for it in **phot2lc**. In this case, however, users may find it relatively easy to add support for a new instrument themselves by adding a new entry into the "teledat.py" script that is installed with **phot2lc**.
