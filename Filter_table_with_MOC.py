from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
from IPython import embed
from astropy.table import Column, Table
from mocpy import MOC
from astropy.wcs import WCS
from astropy.coordinates import Angle, SkyCoord
import astropy.units as u

# Read in your catalogue of objects
path='path-to-catalogue/catalogue.fits'
hdul = fits.open(path)
gals_head=hdul[1].header
col=hdul[1].columns.names

# Read in the MOC  file
euclid_moc = MOC.from_fits("your_moc.fits")


#Filtering the table with the MOC
indexes = euclid_moc.contains(gals["RA"] * u.deg, gals["DEC"] * u.deg)
filtered_gals = gals[indexes] # This only contains objects now that are within the MOC


###############
# Plotting the MOC & galaxies
# Generate an abritrary WCS object
wcs = WCS(naxis=2)
wcs.wcs.ctype = ["RA---AIT", "DEC--AIT"]
wcs.wcs.crval = [110.0, 0.0]
wcs.wcs.cdelt = np.array([-0.675, 0.675])
wcs.wcs.crpix = [240.5, 120.5]

ra, dec = (gals["RA"]* u.deg, gals["DEC"]* u.deg)
# MPL figure with WCS projection
fig = plt.figure(figsize=(15, 7))
ax = plt.subplot(projection=wcs)

euclid_moc.fill(ax=ax, wcs=wcs, alpha=0.9)
sc=ax.scatter(ra, dec, c='red', s=0.03, transform=ax.get_transform("world"), marker='.', vmin=-23, vmax=-2.5)
ax.grid(True)

# Plot the MOC in the current figure

plt.xlabel("ra")
plt.ylabel("dec")
plt.title("Moc with galaxies")
plt.grid(color="black", linestyle="dotted")
plt.savefig('Galaxies_MOC_fullsky.pdf')