# phot2lc

A pure-Python interactive tool for extracting light curves from time series photometric data.

Much of the inspiration for this program came from the [WQED light curve extraction software](https://ui.adsabs.harvard.edu/abs/2013ascl.soft04004T/abstract), but phot2lc includes several new features and the ease of installation that comes with pure-Python programs.

### Features
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
