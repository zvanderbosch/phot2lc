Quickstart
==========

This quickstart guide assumes you have already performed aperture photometry using either IRAF's ccd_hsp or the Matlab-based MAESTRO software, and have already :ref:`configured phot2lc<Configuration>` to run properly on your machine. 


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

In addition, the following files should be present:

* stars.dat (or another file with object names and RA-Dec coordinates)
* The first FITS image (or all images within **image_list_name**)
* If available, the file pointed to by **pixloc_name**


Startup
-------

Once you have started phot2lc and it successfully loads all the necessary files, the following windows will pop up:




