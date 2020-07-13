Quickstart
==========

This quickstart guide assumes you have already performed aperture photometry using either IRAF's ccd_hsp or the Matlab-based MAESTRO software, and have already :ref:`configured phot2lc<Configuration>` to run properly on your machine. 

* `Basic Usage`_
* `Input Files`_
* `Startup`_
* `Command Options`_
* `Aperture Selection`_
* `Output Files`_

Basic Usage
-----------

phot2lc is a command line tool, and can be executed from the command line by simply typing 

.. code-block:: bash

   phot2lc

phot2lc also has several command line arguments available which can be used individually, or all at once:

.. code-block:: text

  -h --help      Show command line options
  -c --codes     Print a list of available telescope codes
  -t --telescope Code name for telescope used
  -s --source    Code name for photometry program used
  -i --image     Name of specific image instead of list
  -o --object    Name of object matching stars.dat entry

If these command line options are used, they will override the defaults that are set within the config.dat file by the photconfig program.


Input Files
-----------

For ccd_hsp output, phot2lc will assume the photometry files have base names of *runbase* followed by the aperture size (e.g. runbase2.5), while for MAESTRO output the photometry files are assumed to have base names of *counts*, again followed by the aperture size (e.g. counts_02.5).

In addition, the following files/info should be present:

* :ref:`stars.dat<The stars.dat File>` (for RA and Dec coordinates)
* The first FITS image (or all images within **image_list_name**)
* If available, the file pointed to by **pixloc_name**
* An entry within teledat.py corresponding to your telescope/instrument
  
  * If you need to add a new entry into teledat.py for your telescope/instrument, you can do this yourself by manually editing the teledat.py file. The format for teledat.py entries is explained within the script itself. Alternatively, you can :ref:`send a request to Zach Vanderbosch<Contact>` to add your telescope configuration into the official phot2lc package.



Startup
-------

Once you have started phot2lc and it successfully loads all the necessary files, the following three windows will appear (*click to enlarge*):

|first-image| |raw-photometry| |divided-lc|

.. |first-image| image:: ./images/first_image.png
                 :width: 32%
                 :alt: First Image

.. |raw-photometry| image:: ./images/raw_photometry.png
                    :width: 32%
                    :alt: Raw Photometry

.. |divided-lc| image:: ./images/divided_lc.png
   		:width: 32%
   		:alt: Divided Light Curve

From left to right, these windows are named:

* **First Image**: Displays the first image. The target and comparison stars are marked if a *pixloc_name* file was provided, otherwise this will just be an unmarked image.
* **Raw Photometry**: Displays the raw photometry for target and comparison stars, along with the amount of sky subtracted from the target. The mean values are displayed to the right of each light curve.
* **Divided Light Curve**: Primarily displays the divided light curve, but also displaying the summed comparison star flux (top right panel) and the polynomial being used to de-trend the light curve (top left panel). This is where most of the interactive tools are used.


Command Options
---------------

Similar to WQED, commands in phot2lc are executed via keyboard inputs. After startup and once you have clicked within one of the windows, you can print out a full list of command options in your terminal by pressing "?". The output will look like the following:

.. code-block:: text


  COMMAND LIST - Divided Light Curve:
    - Type '?' to re-print this list of commands.
    - Type 'd' to delete the point nearest the cursor.
    - Type 'a' to add back a deleted point.
    - Type 'A' to add back ALL deleted points.
    - Type 'g' to activate/deactivate garbage rectangle.
    - Type 'r' to activate/deactivate reverse garbage rectangle.
    - Type 'z' to activate/deactivate zoom rectangle.
    - Type 'Z' to restore zoom to original.
    - Type 'x' to perform sigma clipping.
    - Type 's' to toggle the display of deleted points.
    - Type 'f' to choose the degree of polynomial fit.
    - Type 'c' to choose comparison stars for division.
    - Type 'v' to move to previous aperture size.
    - Type 'w' to move to next aperture size.
    - Type 'Q' to close plots and exit the program.
    - Type 'W' to close plots and continue without grid search.
    - Type 'G' to close plots and continue with grid search.

  COMMAND LIST - Aperture Selection:
    - Type '?' to re-print this list of commands.
    - Type 'd' to delete the point nearest the cursor.
    - Type 'A' to add back all deleted points.
    - Type 'Q' to close plots and exit the program.
    - Type 'W' to save lightcurve with *USER* Selection.
    - Type 'G' to save lightcurve with *GRID* Selection.

The "Divided Light Curve" command list provides your options when you are working within the *Divided Light Curve* window. Within the *First Image* and *Raw Photometry* windows, the only commands available are "?", "Q", "W", and "G". The other command list for aperture selection is for the next window that appears if you decide to continue light curve extraction by typing the "W" or "G" keys when working in the *Divided Light Curve* window.

For more detailed explanations of each command, see the PDF version of the phot2lc user guide (coming soon!).


Aperture Selection
------------------

phot2lc selects the optimal aperture size by identifying the light curve with the lowest average point-to-point (P2P) scatter. The average P2P scatter is defined as:

.. math::

   \langle\mathrm{P2P}\rangle = \sqrt{\frac{\sum(y_{i+1}-y_i)^2}{N}}

The :math:`\langle\mathrm{P2P}\rangle` is determined for all light curves using the same settings defined in the *Divided Light Curve* window (i.e. same deleted points, same polynomial division, same comparison stars used). Currently, this selection is automated and phot2lc does not allow manual selection of a different aperture size. *A future version of phot2lc will likely provide this capability.*

After pressing the "W" or "G" key from any of the previous windows (i.e. *Divided Light Curve*, *Raw Photometry*, or *First Image*), these windows will be closed and a new window will appear named *Aperture Selection*. This window displays the optimal light curve along with its periodogram, and a plot of :math:`\langle\mathrm{P2P}\rangle` versus aperture size for all light curves. 

If you chose the "W" option to continue, only one light curve, periodogram, and :math:`\langle\mathrm{P2P}\rangle` curve will be shown (left image below). If you chose the "G" key, however, a grid search will have been performed considering all possible comparison star and aperture size combinations. In this case, two light curves, periodograms, and :math:`\langle\mathrm{P2P}\rangle` curves will be shown (right image below). One set (colored white) corresponds to the standard optimization procedure performed with the User-selected comparison stars, the same as if you had pressed "W". The second set (colored red), corresponds to the optimal comparison star combination found by the grid search.

|user-selection| |grid-selection|

.. |user-selection| image:: ./images/aperture_selection_user.png
   		    :width: 49%
   		    :alt: First Image

.. |grid-selection| image:: ./images/aperture_selection_grid.png
   		    :width: 49%
  		    :alt: First Image

If you did not perform a grid search, you can now save the optimal light curve by again pressing "W". If you did perform a grid search, you have the option save either the optimal user-selected light curve with "W" or the optimal grid-search-selected light curve with "G".

Output Files
------------

Upon choosing to save your light curve with "W" or "G", phot2lc will perform the :ref:`barycentric time corrections<Barycentric Corrections>` to each point and then provide you with two output files. The **.lc** file contains the divided light curve while the **.phot** file contains the raw photometry corresponding to the optimal aperture size. Again, these files are modeled very closely after the *.lc1* and *.wq* files generated by WQED. 

Both files start with two time columns, the first corresponding to the original times and the second corresponding to the barycentric corrected times. Both are provided in the event that you consider the barycentric corrections for your particular object to be unreliable for any reason.

The naming convention for the files are **<object>_<obs_date>.lc** and **<object>_<obs_date>.phot**, where <object> is replaced by the object name and <obs_date> is replaced by the observation date in YYYYMMDD format.

The .lc File
~~~~~~~~~~~~

The .lc file consists of a header followed by four columns of data. The header provides information with regards to both the observations and the light curve extraction. The four columns are (1) the raw mid exposure times in seconds relative to the first exposure, (2) the barycentric corrected mid-exposure times relative to the first exposure, (3) the relative flux values, and (4) the error on the relative flux. Below is an example .lc1 file showing the header and the first and last three rows of data:

.. code-block:: text

  # Object     : G117-B15A                     # Name of Object
  # RA         : 09 24 15.27                   # Object Right Ascension
  # Dec        : +35 16 51.3                   # Object Declination
  # Telescope  : McDonald 2.1m                 # Name of Telescope
  # Instrument : ProEM                         # Name of Instrument
  # TeleCode   : mcd2                          # Teledat Code Name
  # Date       : 2018-01-26                    # Mid-Exposure UTC Date at T0
  # UTC        : 05:06:01.500                  # Mid-Exposure UTC Time at T0
  # MJD        : 58144.212517361               # Mid-Exposure UTC MJD at T0
  # Exptime    : 15.000000                     # Exposure Time (s)
  # Filter     : BG40                          # Filter Name
  # BJED       : 2458144.718681479             # Mid-Exposure TDB JD at T0
  # ApPhot     : ccd_hsp                       # Photometry Program
  # OrigFile   : runbase6.                     # Source Photometry Filename
  # ApRadius   : 6.00                          # Aperture Radius (pixels)
  # AvgScatter : 1.25                          # Avg. Point-to-Point Scatter (%)
  # Comps      : 2                             # Comparison stars used
  # PolyOrder  : 3                             # Degree of Polynomial Division
  # Nkeep      : 1049                          # Number of points in light curve 
  # Ndelete    : 0                             # Number of points removed
  # Author     : Zach Vanderbosch              # Author of this light curve
  # CreatedOn  : 2020-07-12 21:34:07.518       # Date created
  # Columns: Raw T-mid (s), BaryCorr T-mid (s), Rel. Flux, Rel. Flux Error
       0.000       0.000  -0.031284   0.002743
      15.000      15.000  -0.030957   0.002611
      30.000      30.000  -0.029607   0.002626
      ...         ...        ...        ...
   15690.000   15690.173  -0.011376   0.002271
   15705.000   15705.173  -0.029081   0.002532
   15720.000   15720.174  -0.024124   0.002615


The .phot File
~~~~~~~~~~~~~~

The .phot file also starts with a header providing some of the same information as the .lc file, and is then followed by several columns of data. The first two columns are the same as for the .lc file, providing the raw and barycentric corrected times at mid-exposure with respect to the first exposure.

The remaining columns provide the sky-subtracted photometric counts for the target followed by each comparison star. The last column is always the sky column and represents the amount of background counts subtracted from the target's aperture. Sky subtraction counts are not provided for the comparison stars. The number of comparison star columns will reflect the original number of comparison stars loaded in the *ccd_hsp* or *MAESTRO* photometry files, even if they don't all get used to generate the divided light curve. However, if specific points were deleted from the divided light curve, they will also be removed from this file.

Below is an example .phot file, again showing the header followed by the first and last three rows of data:

.. code-block:: text

  # Object     : G117-B15A                     # Name of Object
  # RA         : 09 24 15.27                   # Object Right Ascension
  # Dec        : +35 16 51.3                   # Object Declination
  # Telescope  : McDonald 2.1m                 # Name of Telescope
  # Instrument : ProEM                         # Name of Instrument
  # TeleCode   : mcd2                          # Teledat Code Name
  # Date       : 2018-01-26                    # Mid-Exp. UTC Start Date
  # UTC        : 05:06:01.500                  # Mid-Exp. UTC Start Time
  # MJD        : 58144.212517361               # Mid Exposure MJD Start
  # Exptime    : 15.000000                     # Exposure Time (s)
  # Filter     : BG40                          # Filter Name
  # BJED       : 2458144.718681479             # Mid Exp. Barycentric Julian Date
  # ApPhot     : ccd_hsp                       # Photometry Program
  # OrigFile   : runbase6.                     # Source Photometry Filename
  # ApRadius   : 6.00                          # Aperture Radius (pixels)
  # Nkeep      : 1049                          # Number of points in light curve 
  # Ndelete    : 0                             # Number of points removed
  # Columns: Raw T-mid (s), BaryCorr T-mid (s), Target, Comp(s), Sky
       0.000       0.000     192620    88577    25195    78351
      15.000      15.000     206569    94587    27371    76162
      30.000      30.000     204690    92457    28212    75914
      ...         ...         ...       ...      ...      ...
   15690.000   15690.173     214079    93761    27382    13946
   15705.000   15705.173     175979    78464    22928    14297
   15720.000   15720.174     166926    73647    22034    15337


