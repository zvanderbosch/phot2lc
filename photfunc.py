import os
import sys
import numpy as np
from astropy.io import fits
from astropy.time import Time
from astropy.coordinates import EarthLocation
from astropy.timeseries import LombScargle as ls


"""
Script containing many functions needed by the 
main phot2lc.py program.

Author: 
    Zach Vanderbosch

For a description of updates, see the 
version_history.txt file.
"""



#############################################################
##  Progress Bar Code. Midified from Stack Overflow,
##  "Python to print out status bar and percentage"

## Provide the interation counter (count=int)
## and the action being performed (action=string)
def progress_bar(count,total,action):
    sys.stdout.write('\r')
    sys.stdout.write(action)
    sys.stdout.write("[%-20s] %d%%  %d/%d" % ('='*int((count*20/total)),\
                                              count*100/total,\
                                              count,total))
    sys.stdout.flush()
    return


#############################################################
## Print Commands Function

def print_commands():
    print("\nCOMMAND LIST - Divided Light Curve:")
    print("    - Type '?' to re-print this list of commands. ")
    print("    - Type 'd' to delete the point nearest the cursor. ")
    print("    - Type 'a' to add back a deleted point. ")
    print("    - Type 'A' to add back ALL deleted points.")
    print("    - Type 'g' to activate/deactivate garbage rectangle. ")
    print("    - Type 'r' to activate/deactivate reverse garbage rectangle. ")
    print("    - Type 'z' to activate/deactivate zoom rectangle. ")
    print("    - Type 'Z' to restore zoom to original. ")
    print("    - Type 'x' to perform sigma clipping. ")
    print("    - Type 's' to toggle the display of deleted points. ")
    print("    - Type 'f' to choose the degree of polynomial fit.")
    print("    - Type 'c' to choose comparison stars for division. ")
    print("    - Type 'v' to move to previous aperture size. ")
    print("    - Type 'w' to move to next aperture size. ")
    print("    - Type 'Q' to close plots and exit the program. ")
    print("    - Type 'W' to close plots and continue without grid search. ")
    print("    - Type 'G' to close plots and continue with grid search. ")
    print("\nCOMMAND LIST - Aperture Selection:")
    print("    - Type 'd' to delete the point nearest the cursor. ")
    print("    - Type 'A' to add back all deleted points.")
    print("    - Type 'W' to save lightcurve with *USER* Selection.")
    print("    - Type 'G' to save lightcurve with *GRID* Selection.")
    return



#############################################################
# Function which grabs the header values for DATE-OBS, 
# TIME-OBS, and EXPTIME for the given filename and converts
# them into an Astropy Time object with ISOT format & UTC scale
def get_time(fname,tdict):

    hdr = fits.getheader(fname)
    dformat = tdict['dformat']
    tformat = tdict['tformat']

    if (dformat == 0) & (tformat == 0): 
        date_obs = hdr[tdict['date']] # Must be YYYY MM DD, any separator works
        time_obs = hdr[tdict['time']] # Must be hh mm ss, any separator works
        t_exp = hdr[tdict['texp']] # Must be in seconds

        # Convert to ISOT format for Astropy Time
        isot_time = "{}-{}-{}T{}:{}:{}".format(date_obs[0:4],date_obs[5:7],
                                               date_obs[8:],time_obs[0:2],
                                               time_obs[3:5],time_obs[6:])
        time = Time(isot_time,scale='utc',format='isot')
        
    elif (dformat == 1) & (tformat == 1):
        dt_obs = hdr[tdict['date']] # Must be ISO or ISOT format, any separator works
        t_exp = hdr[tdict['texp']] # Must be in seconds
        
        # Convert to ISOT format for Astropy Time
        time = Time(dt_obs,scale='utc')

    elif (dformat == 2) & (tformat == 1):
        jd_obs = hdr[tdict['date']] # Must be in Julian Date format

        # Convert to ISOT format for Astropy Time
        time = Time(jd_obs,scale='utc',format='jd')
        t_exp = hdr[tdict['texp']] # Must be in seconds

    return time,t_exp


#############################################################
# Function which gets the Astropy Earthlocation for an 
# observation based on the telescope code used.
def get_loc(hdr,telcode):
    # Choose appropriate telescope location
    if telcode == 'mcd2':
        loc = EarthLocation.of_site('mcdonald')
    elif telcode == 'coud':
        loc = EarthLocation.of_site('mcdonald')
    elif telcode == 'perk':
        loc = EarthLocation.of_site('lowell')
    elif telcode == 'pjmo':
        loc = EarthLocation.from_geodetic(31.67991667,97.67352778,333.0)
    elif telcode == 'lco1':
        site_info = hdr['SITE'].split(" ")
        if any([x=='Haleakala'] for x in site_info):
            loc = EarthLocation.of_site('haleakala')
        elif any([x=='Spring'] for x in site_info):
            loc = EarthLocation.of_site('sso')
        elif any([x=='SAAO'] for x in site_info):
            loc = EarthLocation.of_site('SAAO')
        elif any([x=='McDonald'] for x in site_info):
            loc = EarthLocation.of_site('mcdonald')
        elif any([x=='Tololo'] for x in site_info):
            loc = EarthLocation.of_site('ctio')
    return loc



###################################################
# Some functions used for calculating a divided light curve

# Function for calculating P2P scatter of a light curve
def pp_scat(ydata):  
    Nv = len(ydata)
    pp_avg = (sum((ydata[0:-1]-ydata[1:])**2)/Nv)**(0.5)
    return pp_avg

# Function to calculate a polynomial fit to a lightcurve
def poly_fit(x,y,mu,indk,indd,order):

    # First replace any infinite values with the mean
    # or else the resulting fit will be all NaNs
    y[np.isinf(y)] = mu

    kmodel = np.zeros(len(x[indk]))
    dmodel = np.zeros(len(x[indd]))
    try:
        p = np.polyfit(x[indk],y[indk],order)
    except:
        return kmodel,dmodel
    for i in range(order+1):
        kmodel += p[i]*(x[indk]**(order-i))
        dmodel += p[i]*(x[indd]**(order-i))
    return kmodel,dmodel

# Function which returns the normalized, divided light curve
def div_lc(time,target,comps,order,indk,indd):
    # Create raw divided light curvre
    div1 = target/comps
    mean_div1 = np.nanmean(div1[~np.isinf(div1)])
    mean_targ = np.nanmean(target)
    dlc_raw = div1/mean_div1*mean_targ
    
    # Generate a polynmial fit
    modelk,modeld = poly_fit(time,dlc_raw,mean_targ,indk,indd,order)

    # Generate arrays to return
    dlc_mz_keep = dlc_raw[indk]/modelk - 1.0  # Mean-Zero'd DLC (Kept)
    dlc_mz_dele = dlc_raw[indd]/modeld - 1.0  # Mean-Zero'd DLC (Deleted)
    dlc_raw_keep = dlc_raw[indk]              # Raw DLC (Kept,for model comparison)

    return dlc_mz_keep, dlc_mz_dele, dlc_raw_keep, modelk

# Function to generate a string of comp star combinations
def gen_compstr(combos,ps):
    combo_str = ''
    for i,c in enumerate(combos):
        if i == 0:
            if ps == 'hsp':
                combo_str += '{:1d}'.format(c-1)
            elif ps == 'mae':
                combo_str += '{:.0f}'.format((c-1)/2)
        else:
            if ps == 'hsp':
                combo_str += '+{:1d}'.format(c-1)
            elif ps == 'mae':
                combo_str += '+{:.0f}'.format((c-1)/2)
    return combo_str

# Lomb Scargle Periodogram Function
def calc_lsp(time,flux):

    # Define frequency limit and resolution
    deltat = time[-1] - time[0]
    deltaf = 1./deltat/20. # Oversample by 10
    medtexp = np.median(time[1:] - time[0:-1])
    fnyq = 0.5/medtexp

    # For easier viewing, limit Nyquist frequency to 10,000 uHz
    if fnyq > 0.01:
        fnyq = 0.01

    # Define the frequency array
    freq_arr = np.arange(deltaf,fnyq,deltaf)

    # Calculate the LSP
    lsp = ls(time,flux).power(freq_arr,normalization='psd')
    norm_lsp = np.sqrt(abs(4.0*(lsp/len(time))))
    return freq_arr,norm_lsp


# Calculate standard deviation within a window
def window_std(xarr,yarr,win,dwin):
    std_values = np.zeros(len(win))
    polyx = []
    polyy = []
    for i,w in enumerate(win):
        xd = xarr[w:w+dwin]
        yd = yarr[w:w+dwin]
        poly_params = np.polyfit(xd,yd,2)
        poly_values = np.polyval(poly_params,xd)
        polyy.append(poly_values)
        std_values[i] = np.std(yd-poly_values)
    return polyy,std_values


########################################################
# Functions for re-configuring the config.dat file

def change_val(param,old_value):
    ## ask the user if they want to change/keep it.
    change_value = input('Change %s? (y/[n]): ' %param.split("=")[0].strip())

    if (change_value == 'Y') | (change_value == 'y'):
        new_value = input('\nNew value for %s: ' %param.split("=")[0].strip())
        print('')
        return new_value
    else:
        return old_value

# Function which updates the parameter values in config.dat
def reconfig():

    config_path = os.path.dirname(os.path.realpath(__file__))
    print('\nCurrent Configuration:')
    print('----------------------')
    old_values = []
    with open(config_path + "/config.dat") as f:
        for line in f.readlines():
            print(line.strip("\n"))
            old_values.append(line.strip("\n"))

    change_check = input("\nDo you want to change the configuration? ([y]/n): ")

    # Let's change it up
    if (change_check == 'y') | (change_check == 'Y') | (change_check == ''):
        queries = ['author            = ',
                   'image_list_name   = ',
                   'pixloc_name       = ',
                   'stardat_location  = ',
                   'default_telescope = ',
                   'default_source    = ',
                   'default_image     = ',
                   'default_object    = ']
        output = []
        for i,q in enumerate(queries):
            new_item = change_val(q,old_values[i].split("=")[-1].strip())
            output.append(q + new_item)

        # Write new values to file
        with open(config_path + "/config.dat", "w") as new_file:
            for line in output:
                new_file.write(line+"\n")

        # Open newly saved config.dat and print results
        print('\nNew Configuration:')
        print('------------------')
        with open(config_path + "/config.dat") as f:
            for line in f.readlines():
                print(line.strip("\n"))

    # No change, exit program
    elif (change_check == 'n') | (change_check == 'N'):
        print("Configuration unchanged.\n")
        sys.exit(1)

    # Invalid response, exit program
    else:
        print('Invalid input\n')
        sys.exit(1)

    print('')
    return




