Configuration
=============

* `Running photconfig`_
* `The stars.dat File`_


Running photconfig
------------------

When you first install phot2lc, you will need to change some of the default settings before it works properly on your machine and with your data. A script named **photconfig** is provided for this purpose. Run photconfig from the command line by simply typing

.. code-block:: bash

   photconfig

at which a point you will be lead through a series of prompts to edit the configuration file "config.dat." The parameters that need to be set are:

* **author**
* **image_list_name**
* **pixloc_name**
* **stardat_location**
* **default_telescope**
* **default_source**
* **default_image**
* **default_object**

After initially installing phot2lc, the default values for these parameters should be as follows:

.. code-block:: bash

   author            = Zach Vanderbosch
   image_list_name   = olist
   pixloc_name       = phot_coords.orig
   stardat_location  = /home/zachvanderbosch/data/stars.dat
   default_telescope = mcd2
   default_source    = hsp
   default_image     = None
   default_object    = None



Below are detailed descriptions for each parameter's meaning and use:

* **author**: phot2lc User name (e.g. your name).

* **image_list_name**: Name of the file which contains the list of image filenames corresponding to each photometric data point. The images are used for a few purposes, such as grabbing some key header information, and using the first filename in the list to display an image for target and comparison star identification. Depending on which photometry pipeline was used, the image headers may also be used to generate time stamps for each data point in the light curve.
  
    * If using MAESTRO, ULTRACAM, or HiPERCAM output, the time stamps will automatically come from the photometric output files instead of the images, so only the first image listed within image_list_name is used for display purposes and for grabbing some header information. This parameter can be set to **None** as long as a single image name is provided using the **phot2lc** command line option -i (-\\\-image).
  
    * If using ccd_hsp output, this file is only needed if you want to generate time stamps for your light curve by grabbing times from each individual FITS header. If this parameter is set to **None**, then timestamps will be generated using the exposure time multiplied by the number of exposures since the first image. In this case, the name of the first image must be provided using the **phot2lc** command line option -i (-\\\-image).

* **pixloc_name**: Name of the file containing initial guesses for the pixel coordinates of each star. 

    * This is optional, used only by phot2lc for marking stars when displaying the first image, and can be set to **None** if unavailable. When using ULTRACAM or HiPERCAM pipelines, it is assumed that this file will be structured like a ".ape" file created by the setaper routine of the respective pipelines. For ccd_hsp and MAESTRO, a simple ascii file with space-delimited columns is expected, where the first and second columns provide the x and y coordinates, respectively. In all cases, the target is assumed to be the first set of coordinates in the file.

* **stardat_location**: Path and filename for file containing the RA and Dec corresponding to a given object name (e.g. /user/zvander/stars.dat). This parameter is required, as is :ref:`the stars.dat file<The stars.dat file>`.

* **default_telescope**: Default telescope code.

    * Telescope codes correspond to an entry within teledat.py and describe both the telescope, instrument, and FITS header keywords needed to set some phot2lc parameters. For a list of currently supported telescope codes, see the :ref:`Introduction<Introduction>`, or type **phot2lc -c** on the command line. This default setting can be overridden with the **phot2lc** command line option -t (\-\-telescope).

* **default_source**: Default photometry pipeline whose output is being loaded in to **phot2lc**. Must be one of the currently supported pipelines listed in the :ref:`Introduction<Introduction>`. This default setting can be overridden with the **phot2lc** command line option -s (\-\-source).

* **default_image**: Default image name. 

    * When using MAESTRO output, or ccd_hsp output with only the first image for time stamp generation, you may anticipate all of your first images to have the same name (e.g. firstimage.fits). In such a case, you can use this parameter to automatically set the image name instead of having to define it with the **phot2lc** -i command line option. If set, you can still use the -i option to override the default in the event a different image name is used. If unused, set this parameter to **None**. 

* **default_object**: Default object name. 

    * A useful parameter to set if you intend to reduce a lot of light curves at once for a single object whose name cannot be obtained directly from the image header. This object name needs to correspond to an object name within your stars.dat file, since this is how the object's coordinates are acquired for barycentric time corrections. If unused, set to **None**. This default setting can be overridden with the **phot2lc** command line option -o (\-\-object).


The stars.dat File
------------------

stars.dat is a seven-column, whitespace-delimited text file used to store object names and their corresponding RA and Dec coordinates. **The RA and Dec must be ICRS J2000 coordinates for proper** :ref:`barycentric corrections<Barycentric Corrections>`. You can actually name the stars.dat file whatever you want, as long as it matches the filename you provide in your **config.dat** file, but from here on out this documentation will refer to the file as stars.dat. Below are three example lines within a stars.dat file:

.. code-block:: text

   GD358          16 47 18       +32 28 32
   ZTFJ0139+5245  01 39 06.17    +52 45 36.89
   V386ser        16 10 33.62889 -01 02 23.20995

As you can see, each entry needs an object name (*no spaces allowed!*), and an RA and Dec in HMSDMS format with only spaces as delimiters. The decimal values can be to any precision you want, and you can put as many spaces between each column as you want. When you run phot2lc, the program will look for an entry in stars.dat that matches the object name retrieved from the image header or given as a command line argument.
