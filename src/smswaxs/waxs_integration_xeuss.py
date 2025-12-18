"""
This script will integrate 2D SAXS data collected on the Xenocs
Xeuss SWAXS instrument and subtract background data if necessary.
"""
import argparse as ap
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from mpl_toolkits.axes_grid1 import make_axes_locatable
import pyFAI
from pyFAI.integrator.azimuthal import AzimuthalIntegrator
import fabio
import numpy as np

# pylint: disable=C0103, unused-variable


def cli():
    """Integrate 2D saxs data"""
    parser = ap.ArgumentParser(
        description="Perform data reduction on data from Xeuss 2.0C")

    parser.add_argument("sample", help="sample file (.edf)")

    parser.add_argument("mask", help="mask file (.edf)")
    parser.add_argument("--poni", help="PONI configuration file (.poni)")
    parser.add_argument("--background", help="background file (.edf)")
    parser.add_argument(
        "--opencl", help="Use OpenCL (requires pyopencl)", action="store_true")
    parser.add_argument(
        "--bkg_factor", help="background correction factor", type=float, default=float(1))
    parser.add_argument(
        "--lac", help="Convert to absolute units using the calculated thickness - LAC in cm^-1",
        type=float, default=float(0))
    parser.add_argument(
        "--thickness", help="thickness /cm used for trans. cor. (otherwise, trans. int. used)",
        type=float, default=float(0))
    parser.add_argument(
        "--xmin", help="Minimum value of radial unit (q)", type=float)
    parser.add_argument(
        "--xmax", help="Max value of radial unit (q)", type=float, default=3.8)
    parser.add_argument(
        "--raw2D", help="Display the 2D image in the lab frame", action="store_true")
    parser.add_argument(
        "--noabs", help="No absorption correction", action="store_true")
    parser.add_argument(
        "--unit", help="Radial unit for integration, q or 2th", type=str, default="q")
    args = parser.parse_args()

    if args.unit.lower() == "q":
        UNIT = "q_A^-1"

    elif args.unit.lower() == "2th":
        UNIT = "2th_deg"
    else:
        raise ValueError("Unit must be 'q' or '2th'")
    if args.xmin:
        radran = (args.xmin, args.xmax)
    else:
        radran = (None)
    file = fabio.open(args.sample)
    mask = fabio.open(args.mask)
    if args.noabs is False:
        def abscor(tth, intensity, trans):
            """Absorption correction for WAXS according to the Bragg corrections section of the
            XSACT user manual (2020)"""
            if np.allclose(trans, 1, atol=5e-3):
                return intensity
            else:
                fabs = (np.log(trans)*((1/np.cos(np.radians(tth)))-1)) / \
                    (np.exp(np.log(trans)*((1/np.cos(np.radians(tth)))-1))-1)
                cor_int = intensity/fabs
                return cor_int
    else:
        def abscor(_, intensity, __):
            return intensity

    if args.opencl:
        intmeth = 'opencl'
    else:
        intmeth = 'csr'
    if not args.poni:
        geo = {
            "detector": pyFAI.detectors.Detector(float(file.header['PSize_2']), 
                                                 float(file.header['PSize_1'])),
            "dist": float(file.header['SampleDistance']),
            "poni1": float(file.header['PSize_2'])*float(file.header['Center_2']),
            "poni2": float(file.header['PSize_1'])*float(file.header['Center_1']),
            "rot1": 0,
            "rot2": 0,
            "rot3": 0,
            "wavelength": float(file.header['WaveLength'])
        }

        # poni = pyFAI.azimuthalIntegrator.AzimuthalIntegrator(**geo)

        poni = AzimuthalIntegrator(**geo)
    else:
        poni = pyFAI.load(args.poni)
    try:
        transmission_sample = float(file.header['Transmission'])
    except KeyError:
        if np.allclose(args.lac, 0):
            args.noabs = True
        else:
            if np.allclose(args.thickness, 0) is False:
                transmission_sample = np.exp(-args.lac*args.thickness)
            else:
                args.noabs = True

    norm_sample = (float(file.header['Intensity1']) *
                   float(file.header['ExposureTime']) *
                   (
        (
            float(file.header['PSize_1']) /
            float(file.header['SampleDistance']))
    )**2
    )/1e-15

    data_1D = poni.integrate1d(file.data,
                               1000, filename=args.sample[:-4]+'_1D.dat', correctSolidAngle=True,
                               method=intmeth, radial_range=radran, azimuth_range=(None),
                               unit=UNIT, mask=mask.data, normalization_factor=norm_sample,
                               metadata=None, error_model="poisson")

    data_1D_corr = [data_1D[0], data_1D[1], data_1D[2]]
    if args.unit.lower() == "2th":
        data_1D_corr[1] = abscor(data_1D[0], data_1D[1], transmission_sample)
    else:
        data_1D_corr[1] = abscor(2*np.degrees(np.arcsin(((float(file.header['WaveLength'])/1e-10)
                                 * data_1D[0])/(4*np.pi))), data_1D[1], transmission_sample)
    data_2D = file.data/transmission_sample

    if args.background is not None:
        bkg = fabio.open(args.background)
        if np.allclose(float(bkg.header['Transmission']), 1, atol=5e-3):
            transmission_bkg = 1
        else:
            transmission_bkg = float(bkg.header['Transmission'])

        norm_bkg = (float(bkg.header['Intensity1']) *
                    float(bkg.header['ExposureTime']) *
                    (
                        (
                            float(bkg.header['PSize_1']) /
                            float(bkg.header['SampleDistance']))
        )**2
        )/1e-15
        bkg_1D = poni.integrate1d(bkg.data,
                                  1000, filename=args.sample[:-4]+'_bkg1D.dat',
                                  correctSolidAngle=True, method=intmeth,
                                  radial_range=radran, azimuth_range=(None),
                                  unit=UNIT, mask=mask.data, normalization_factor=norm_bkg,
                                  metadata=None, error_model="poisson")

        bkg_1D_corr = [bkg_1D[0], bkg_1D[1], bkg_1D[2]]
        if args.unit.lower() == "2th":
            bkg_1D_corr[1] = abscor(bkg_1D[0], bkg_1D[1], transmission_bkg)
        else:
            bkg_1D_corr[1] = abscor(
                2*np.degrees(np.arcsin(((float(file.header['WaveLength'])/1e-10)*bkg_1D[0])/
                                       (4*np.pi))), bkg_1D[1], transmission_bkg)
        bkg_2D = bkg.data/transmission_bkg * args.bkg_factor
        data_I = data_1D_corr[1]-bkg_1D_corr[1]
        data_2I = data_2D - bkg_2D
        data_sig = abs(data_1D_corr[2])+abs(bkg_1D_corr[2])
    else:
        data_I = data_1D_corr[1]
        data_2I = data_2D
        data_sig = data_1D_corr[2]

    data_2I2 = poni.integrate2d(data_2I, 3000, 3600, unit=UNIT)

    I2, q2, chi2 = data_2I2

    if np.min(I2) < 0:
        I2min = 1e-3
    else:
        I2min = np.min(I2)
    I2max = np.max(I2)

    fig, axs = plt.subplot_mosaic(
        [['(a)', '(b)']], figsize=(7, 4), constrained_layout=True)
    if args.raw2D is False:
        fig1 = axs['(a)'].imshow(I2, origin="lower",
                                 extent=[q2.min(), q2.max(), chi2.min(), chi2.max()],
                                 norm=LogNorm(vmin=I2min, vmax=I2max), cmap=plt.get_cmap('cividis'),
                                 aspect="auto")
        if args.unit.lower() == "q":
            axs['(a)'].set_xlabel(r'q /$\AA^{-1}$', fontsize=8)
        else:
            axs['(a)'].set_xlabel(r'2$\theta$ /$^{\circ}$', fontsize=8)
        axs['(a)'].set_ylabel(r'$\phi/^{\circ}$', fontsize=8)
    else:
        fig1 = axs['(a)'].imshow(data_2I, norm=LogNorm(
            vmin=I2min, vmax=I2max), cmap=plt.get_cmap('cividis'), aspect="auto")
        axs['(a)'].set_xlabel('X /px', fontsize=8)
        axs['(a)'].set_ylabel('Z /px', fontsize=8)
    divider = make_axes_locatable(axs['(a)'])
    cax = divider.append_axes("top", size="5%", pad=0.05)

    cbar = plt.colorbar(fig1, cax=cax, orientation="horizontal")
    cbar.ax.tick_params(labelsize=8)
    cax.xaxis.set_ticks_position("top")

    axs['(a)'].tick_params(labelsize=8)

    fig2 = axs['(b)'].plot(data_1D[0], data_I, linewidth=0.5)

    # axs['(b)'].set_xscale('log')
    # axs['(b)'].set_yscale('log')
    if args.unit.lower() == "q":
        axs['(b)'].set_xlabel(r'q /$\AA^{-1}$', fontsize=8)
    else:
        axs['(b)'].set_xlabel(r'2$\theta$ /$^{\circ}$', fontsize=8)
    axs['(b)'].set_ylabel('I(q) /Arb.', fontsize=8)
    axs['(b)'].get_xaxis().set_major_formatter(ticker.ScalarFormatter())
    # axs['(b)'].get_yaxis().set_major_formatter(ticker.ScalarFormatter())
    # axs['(b)'].ticklabel_format(style='sci', axis='both',
    #                             scilimits=(0, 0), useMathText=True)
    # axs['(b)'].set_xticks([0.01, 0.1, 1])
    # axs['(b)'].get_xaxis().set_major_formatter(ticker.ScalarFormatter())
    axs['(b)'].tick_params(labelsize=8)
    # plt.show()
    plt.savefig(args.sample[:-4]+".png", bbox_inches="tight",dpi=600)

    data_out = np.column_stack((data_1D[0], data_I, data_sig))
    if args.unit.lower() == "q":
        header_str = "q(A^-1)\tI(Arb.)\tSigma(Arb.)"
        np.savetxt(args.sample[:-4]+"_subtracted.dat",
                   data_out, delimiter='\t', fmt='%s', header=header_str)
    elif args.unit.lower() == "2th":
        np.savetxt(args.sample[:-4]+".xye",
                   data_out, delimiter='\t', fmt='%s')


if __name__ == "__main__":
    cli()
