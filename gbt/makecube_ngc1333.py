import astropy.io.fits as pyfits
import itertools
import sys
sys.path.append('/Users/adam/repos/casaradio/branches/python/ginsburg/')
import makecube
import numpy as np
np.seterr(all='ignore')

scanrange=[33,57]
ref1 = 33
ref2 = 57
refscans = [33,57]#,22,32]
sourcename = "n1333ctr"
obsmode = "RALongMap:FSWITCH:FSW12"
mapname = 'NGC1333'
outpath = '/Users/adam/observations/gbt/%smap/' % mapname
tau = 0.015 # pm 0.05 for different freqs, over the night

filename = '/Users/adam/observations/gbt/AGBT13B_031_01/AGBT13B_031_01.raw.acs.fits'
#filepyfits = pyfits.open(filename,memmap=True)
#datapfits = filepyfits[1].data
#dataarr = datapfits.DATA

filepyfits = pyfits.open(filename,memmap=True)
datapfits = filepyfits[2].data
dataarr = datapfits.DATA
if datapfits.DATA[-1,:].sum() == 0:
    import pdb; pdb.set_trace()
    print "READING USING PFITS"
    t0 = time.time()
    import pfits
    datapfits = pfits.FITS(filename).get_hdus()[1].get_data()
    print "Successfully read in %i seconds" % (time.time() - t0)
    dataarr = numpy.reshape(datapfits['DATA'],datapfits['DATA'].shape[::-1])

figure(1)
clf()
for feed in (1,2):
    for sampler in ("A13","A9","C25","C29"):
        OK = (datapfits['FEED'] == feed) * (datapfits['SAMPLER'] == sampler)
        if OK.sum() > 0:
            plot(datapfits['LST'][OK],dataarr[OK,8000:10000].mean(axis=1),',',label='Feed %i Sampler %s' % (feed,sampler))
gca().set_ylim(1,5)
savefig('/Users/adam/observations/gbt/AGBT13B_031_01/AGBT13B_031_01_continuum.png')
close(1)


scanrange=[33,57]
ref1 = 33
ref2 = 57
refscans = [33,57]#,22,32]
sourcename = "n1333ctr"
obsmode = "RALongMap:FSWITCH:FSW12"
mapname = 'NGC1333'
outpath = '/Users/adam/observations/gbt/%smap/' % mapname
tau = 0.015 # pm 0.05 for different freqs, over the night
velo_range = [-100,100]
exclude_velo=[-60,-55,5,10,70,75]

feeds = {'A13':1,'A9':1,'C25':2,'C29':2}
for sampler in ("A13","A9","C25","C29"):
    feed = feeds[sampler]
    off_template,off_template_in = makecube.make_off(datapfits, scanrange=scanrange,
            exclude_velo=exclude_velo, interp_vrange=velo_range,
            interp_polyorder=1, sampler=sampler, return_uninterp=True,
            feednum=feed)
    makecube.calibrate_cube_data(datapfits,
            outpath+'13B_031_%ito%i_%s_F1.fits' %
            (ref1,ref2,sampler),scanrange=scanrange,refscan1=ref1,refscan2=ref2,
            feednum=feed, refscans=refscans, sampler=sampler, filepyfits=filepyfits,
            datapfits=datapfits, tau=tau, dataarr=dataarr, obsmode=obsmode,
            sourcename=sourcename, off_template=off_template)






cubename='NGC1333_H2CO22_cube'
# 15' x 12 ' 
makecube.generate_header(52.256025, 31.257809, coordsys='radec', naxis1=30, naxis2=30, pixsize=20,
        naxis3=2000, cd3=0.1, crval3=7.5, clobber=True, restfreq=14.488479e9)
makecube.make_blank_images(cubename,clobber=True)

files = ['/Users/adam/observations/gbt/NGC1333map/13B_031_33to57_A13_F1.fits',
         '/Users/adam/observations/gbt/NGC1333map/13B_031_33to57_A9_F1.fits',
        '/Users/adam/observations/gbt/NGC1333map/13B_031_33to57_C25_F2.fits',
        '/Users/adam/observations/gbt/NGC1333map/13B_031_33to57_C29_F2.fits',
         #'/Users/adam/observations/gbt/NGC1333map/13B_031_22to32_A13_F1.fits',
         #'/Users/adam/observations/gbt/NGC1333map/13B_031_22to32_A9_F1.fits',
         ]

for fn in files:
    makecube.add_file_to_cube(fn,
        cubename+'.fits',nhits=cubename+'_nhits.fits',wcstype='V',
        velocityrange=[-100,100],excludefitrange=exclude_velo,coordsys='galactic') # removed smoothto kwd
