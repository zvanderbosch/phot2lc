phot2lc
=======

phot2lc is a pure-Python interactive tool for extracting light curves from time-series photometric data. 

phot2lc is largely inspired by WQED (`Thompson & Mullally 2009 <https://ui.adsabs.harvard.edu/abs/2009JPhCS.172a2081T/abstract>`_, `2013 <https://ui.adsabs.harvard.edu/abs/2013ascl.soft04004T/abstract>`_), and is currently designed to work with the photometric outputs from MAESTRO (`Dalessio 2010 <https://ui.adsabs.harvard.edu/abs/2010AAS...21545209D/abstract>`_, `2013 <https://ui.adsabs.harvard.edu/abs/2013PhDT.......170D/abstract>`_), ccd_hsp (`Kanaan et al. 2002 <https://ui.adsabs.harvard.edu/abs/2002A%26A...389..896K/abstract>`_), ULTRACAM (`Dhillon et al. 2007 <https://ui.adsabs.harvard.edu/abs/2007MNRAS.378..825D/abstract>`_), and HiPERCAM (`Dhillon et al. 2021 <https://ui.adsabs.harvard.edu/abs/2021MNRAS.507..350D/abstract>`_).


Installation
============

Current version: |pypi-badge|

.. |pypi-badge| image:: https://img.shields.io/pypi/v/phot2lc.svg
                :target: https://pypi.python.org/pypi/phot2lc
                :alt: PyPI Latest Version

You can install phot2lc with pip:

.. code-block:: bash

   pip install phot2lc

The phot2lc project can also be found at `GitHub <https://github.com/zvanderbosch/phot2lc>`_ and at `PyPI <https://pypi.org/project/phot2lc/>`_.


Requirements
============

* Python >= 3.6
* Matplotlib >= 3.1.3
* Astropy >= 4.0
* LMFIT >= 1.0.1


Package Contents
================

* **phot2lc** -- The main light curve extraction program
* **photconfig** -- Configures some of phot2lc's defaults
* **weldlc** -- Welds together multiple light curve files into one
* **quicklook** -- Generates quicklook plots of light curves and their periodograms


Guide
^^^^^

.. toctree::
   :maxdepth: 7
   
   introduction
   configuration
   quickstart
   barycorr
   additional
   license
   help

