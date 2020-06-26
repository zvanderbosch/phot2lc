phot2lc
=======

phot2lc is a pure-Python interactive tool for extracting light curves from time-series photometric data. 

phot2lc is largely inspired by WQED (`Thompson & Mullally 2009 <https://ui.adsabs.harvard.edu/abs/2009JPhCS.172a2081T/abstract>`_, `2013 <https://ui.adsabs.harvard.edu/abs/2013ascl.soft04004T/abstract>`_), and is designed to work with the outputs from both MAESTRO (`Dalessio 2010 <https://ui.adsabs.harvard.edu/abs/2010AAS...21545209D/abstract>`_, `2013 <https://ui.adsabs.harvard.edu/abs/2013PhDT.......170D/abstract>`_) and ccd_hsp (`Kanaan et al. 2002 <https://ui.adsabs.harvard.edu/abs/2002A%26A...389..896K/abstract>`_). 


Installation
============

You can install phot2lc simply with pip:

.. code-block:: bash

   pip install phot2lc

The phot2lc project can also be found at `GitHub <https://github.com/zvanderbosch/phot2lc>`_ and at `PyPI <https://pypi.org/project/phot2lc/>`_.


Package Contents
================

* **phot2lc** -- The main light curve extraction program
* **photconfig** -- A program that configures some of phot2lc's defaults
* **weldlc** -- A program that can weld together multiple light curve files into one


Guide
^^^^^

.. toctree::
   :maxdepth: 4
    
   configuration
   quickstart
   license
   help

