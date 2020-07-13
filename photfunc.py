import os
import sys
import numpy as np
from copy import deepcopy
from scipy.signal import find_peaks
from astropy.io import fits
from astropy.time import Time
from astropy.coordinates import EarthLocation
from astropy.timeseries import LombScargle as ls
import lmfit as lmf
from lmfit import Model


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
    print("    - Type '?' to re-print this list of commands. ")
    print("    - Type 'd' to delete the point nearest the cursor. ")
    print("    - Type 'A' to add back all deleted points.")
    print("    - Type 'Q' to close plots and exit the program. ")
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
        t_exp = float(hdr[tdict['texp']]) # Must be in seconds

        # Convert to ISOT format for Astropy Time
        isot_time = "{}-{}-{}T{}:{}:{}".format(date_obs[0:4],date_obs[5:7],
                                               date_obs[8:],time_obs[0:2],
                                               time_obs[3:5],time_obs[6:])
        time = Time(isot_time,scale='utc',format='isot')
        
    elif (dformat == 1) & (tformat == 1):
        dt_obs = hdr[tdict['date']] # Must be ISO or ISOT format, any separator works
        t_exp = float(hdr[tdict['texp']]) # Must be in seconds
        
        # Convert to ISOT format for Astropy Time
        time = Time(dt_obs,scale='utc')

    elif (dformat == 2) & (tformat == 1):
        jd_obs = hdr[tdict['date']] # Must be in Julian Date format

        # Convert to ISOT format for Astropy Time
        time = Time(jd_obs,scale='utc',format='jd')
        t_exp = float(hdr[tdict['texp']]) # Must be in seconds

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
    pp_avg = (sum((ydata[0:-1]-ydata[1:])**2)/(Nv-1))**(0.5)
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
    if fnyq > 0.012:
        fnyq = 0.012

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
    change_value = input('Change {:<18s} (y/[n]): '.format(param.split("=")[0].strip()+"?"))

    if (change_value == 'Y') | (change_value == 'y'):
        new_value = input('New value for %s: ' %param.split("=")[0].strip())
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
    print('')


    # Let's change it up
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

    print('')
    return






############################################################
## Define Functions for FITLC's pre-whitening sequence

# Sinusoidal Function
def sine(x,freq,amp,phase):
    return amp*np.sin(2.0*np.pi*(freq*x + phase))

# A simple constant offset
def offset(x,offset):
    return offset

# Function used to generate a multi-term sinusoidal function
def make_sine_func(nterms):
    if nterms < 1:
        print('Cannot generate function with Zero terms.')
        sys.exit(1)

    for i in range(nterms):
        prefix = "s{}_".format(i+1)
        if i == 0:
            m = Model(offset) + Model(sine, prefix=prefix)
        else:
            m += Model(sine, prefix=prefix)
    return m


# The main pre-whitening function
def prewhiten(time,flux,Npw=1,fmin=500,fmax=100000):

    # Get time sampling and duration
    texp = np.median(time[1:] - time[:-1])
    delt = time[-1] - time[0]

    # Calculate the raw Periodogram
    farr,lsp_raw = calc_lsp(time,flux)
    raw_threshold = 4.0*np.nanmean(lsp_raw[(farr>0.0005) & (farr<0.012)])

    # Define the peak search limits (in frequency units)
    fmin = float(fmin)*1e-6 # Exclude peaks below 500 microhertz (default)
    fmax = float(fmax)*1e-6 # Exclude peaks above 100000 microhertz (default)

    flux_fit = np.copy(flux)  # Make a copy of flux which will be pre-whitened
    old_names = []
    for i in range(Npw):

        # Calculate Lomb-Scargle Periodogram (LSP)
        farr,lsp = calc_lsp(time,flux_fit)
        threshold = 4.0*np.nanmean(lsp[(farr>0.0005) & (farr<0.012)])

        # Find the highest peak
        peaks,props = find_peaks(lsp,height=threshold)
        if len(peaks) > 0:
            choose_peaks = [p for p,f in zip(peaks,farr[peaks]) 
                            if (f > fmin) & (f < fmax)]
            choose_heights = [h for h,f in zip(props['peak_heights'],farr[peaks]) 
                              if (f > fmin) & (f < fmax)]
            if len(choose_peaks) == 0:
                if i == 0:
                    peaks_found = False
                    break
                else:
                    break
            max_height = max(choose_heights)
            max_idx = np.where(choose_heights == max_height)[0][0]
            max_freq = farr[choose_peaks][max_idx]
        else:
            if i == 0:
                peaks_found = False
                break
            else:
                break

        # Generate the model and parameters
        peaks_found = True
        mod = make_sine_func(i+1)
        par = mod.make_params()

        # Set initial guesses and limits for parameters for
        # a linear lieast squares fit (i.e. fix the frequencies)
        # This will provide a better intial guess for the phases.
        for name,_ in par.items():
            if name in old_names:
                par[name].value = par_old[name].value
                if 'freq' in name:
                    par[name].vary = False
            else:
                if 'off' in name:
                    par[name].value = 0.0
                if 'freq' in name:
                    par[name].value = max_freq
                    par[name].vary = False
                if 'amp' in name:
                    par[name].value = max_height
                if 'pha' in name:
                    par[name].value = 0.0

        # Perform the linear LSQ fit
        result = mod.fit(flux, params=par, x=time)

        # Now unfix the frequencies
        new_par = result.params
        for name,_ in new_par.items():
            if 'freq' in name:
                new_par[name].vary = True

        # Perform the non-linear LSQ fit
        result = mod.fit(flux, params=new_par, x=time)

        # Save the new parameters and parameter names for next iteration
        par_old = deepcopy(result.params)
        old_names = [x for x,_ in par_old.items()]

        # Pre-Whiten the Light Curve
        flux_fit = np.copy(flux) - result.best_fit


    # Return fit result or None
    if peaks_found:
        # Calculate LSP one more time to get the fully pre-whitened LSP
        _,lsp = calc_lsp(time,flux_fit)
        return result,lsp
    else:
        return None,None





