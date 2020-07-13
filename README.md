# phot2lc

**phot2lc** is s pure-Python interactive tool for extracting light curves from time series photometric data.

[![PyPI](https://img.shields.io/pypi/v/phot2lc.svg)](https://pypi.org/project/phot2lc/)
[![Docs](https://readthedocs.org/projects/phot2lc/badge/?version=latest)](https://phot2lc.readthedocs.io/en/latest/?badge=latest)

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
* Python 3.6 (or later)
* matplotlib 3.1.3 (or later)
* Astropy 4.0 (or later)
* LMFIT 1.0.1
