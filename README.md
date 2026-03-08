# phot2lc

**phot2lc** is s pure-Python interactive tool for extracting light curves from time series photometric data.

[![PyPI](https://img.shields.io/pypi/v/phot2lc.svg)](https://pypi.org/project/phot2lc/)
[![Docs](https://readthedocs.org/projects/phot2lc/badge/?version=latest)](https://phot2lc.readthedocs.io/en/latest/?badge=latest)
[![DOI](https://zenodo.org/badge/271863975.svg)](https://zenodo.org/badge/latestdoi/271863975)


Much of the inspiration for this program came from the [WQED light curve extraction software](https://ui.adsabs.harvard.edu/abs/2013ascl.soft04004T/abstract), but **phot2lc** includes several new features and the ease of installation that comes with pure-Python programs.

### Installation

**phot2lc** can be installed with:

```bash
$ pip install phot2lc
```
Documentation for **phot2lc** can be found at [phot2lc.readthedocs.io](https://phot2lc.readthedocs.io/en/latest/)

### Main Features
* Comparison star selection
* Aperture size selection
* Polynomial detrending
* Sigma clipping
* Manual data point removal
* Barycentric time corrections

### Requirements:
* python >= 3.11
* numpy >= 2.4
* scipy >= 1.17
* pandas >= 3.0
* matplotlib >= 3.10
* PyQt5 >= 5.15
* astropy >= 7.2
* photutils >= 2.3
* lmfit >= 1.3
