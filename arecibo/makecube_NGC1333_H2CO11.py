import sys
sys.path.append('/Users/adam/repos/casaradio/branches/python/ginsburg/')
import makecube

cubename='NGC1333_H2CO11_cube'
makecube.generate_header(52.25625, 31.257809, coordsys='radec', naxis1=60, naxis2=60, pixsize=20,
        naxis3=2000, cd3=0.1, crval3=7.5, clobber=True, restfreq=14.488479e9)
makecube.make_blank_images(cubename,clobber=True)
for ii in xrange(5):
    makecube.add_file_to_cube('/Users/adam/observations/arecibo/20130913/NGC1333_spectra_0913_%i.fits' % ii,
        cubename+'.fits',nhits=cubename+'_nhits.fits',wcstype='V',
        velocityrange=[-50,50],excludefitrange=[4,10], coordsys='radec')

makecube.make_flats(cubename,vrange=[4,10],noisevrange=[-20,0])
