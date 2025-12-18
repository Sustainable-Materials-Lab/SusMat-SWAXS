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
    parser.add_argument("--empty", help="empty file (.edf)")
    parser.add_argument("--background", help="background file (.edf)")
    parser.add_argument(
        "--opencl", help="Use OpenCL (requires pyopencl)", action="store_true")
    parser.add_argument(
        "--bkg_factor", help="background correction factor", type=float, default=float(1))
    parser.add_argument(
        "--lac", help="Convert to absolute units using the calculated thickness - LAC in cm^-1",type=float, default=float(0))
    parser.add_argument(
        "--thickness", help="thickness in cm used for transmission correction (otherwise, transmitted intensity used)",type=float, default=float(1))
    parser.add_argument(
        "--autobkg", help="Automatic background scaling", action="store_true")
    args = parser.parse_args()


    file = fabio.open(args.sample)
    mask = fabio.open(args.mask)


    if args.opencl:
        intmeth = 'opencl'
    else:
        intmeth = 'csr'
    if not args.poni:
        geo = {
            "detector": pyFAI.detectors.Detector(float(file.header['PSize_2']),float(file.header['PSize_1'])),
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

    if np.allclose(args.lac, 0):
        transmission_sample = args.thickness
    else:
        transmission_sample = -((1/args.lac)*np.log10(float(file.header['Transmission'])))

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
                            method=intmeth, radial_range=(None), azimuth_range=(None),
                            unit="q_A^-1", mask=mask.data, normalization_factor=norm_sample,
                            metadata=None, error_model="poisson")

    data_2D = file.data/transmission_sample

    if args.background is not None:
        bkg = fabio.open(args.background)
        if np.allclose(args.lac, 0):
            transmission_bkg = args.thickness
        elif np.allclose(float(bkg.header['Transmission']), 1, atol=5e-3):
            transmission_bkg = -((1/args.lac)*np.log10(1))
        else:
            transmission_bkg = -((1/args.lac)*np.log10(float(bkg.header['Transmission'])))
        
        norm_bkg = (float(bkg.header['Intensity1']) *
                    float(bkg.header['ExposureTime']) *
                    (
                        (
                            float(bkg.header['PSize_1']) /
                            float(bkg.header['SampleDistance']))
        )**2
        )/1e-15
        bkg_1D = poni.integrate1d(bkg.data,
                                1000, filename=args.sample[:-4]+'_bkg1D.dat', correctSolidAngle=True,
                                method=intmeth, radial_range=(None), azimuth_range=(None),
                                unit="q_A^-1", mask=mask.data, normalization_factor=norm_bkg,
                                metadata=None, error_model="poisson")

        bkg_2D = bkg.data/transmission_bkg

        if args.autobkg is True:
            print("Use automated background scaling with caution!")
            if max(bkg_1D[1][:np.where(bkg_1D[0] > 0.02)[0][0]]) > max(data_1D[1][:np.where(data_1D[0] > 0.02)[0][0]]):
                bkg_1D = [bkg_1D[0], bkg_1D[1], bkg_1D[2]]
                bkg_1D[1] -= max(bkg_1D[1][:np.where(bkg_1D[0] > 0.02)[0][0]]) - \
                    max(data_1D[1][:np.where(data_1D[0] > 0.02)[0][0]])
    else:
        data_I = data_1D[1]
        data_sig = abs(data_1D[2])
    if args.empty is not None:
        empty = fabio.open(args.empty)
        if np.allclose(args.lac, 0):
            transmission_empty = args.thickness
        elif np.allclose(float(bkg.header['Transmission']), 1, atol=5e-3):
            transmission_empty = -((1/args.lac)*np.log10(1))
        else:
            transmission_empty = -((1/args.lac)*np.log10(float(empty.header['Transmission'])))
        norm_empty = (float(empty.header['Intensity1']) *
                    float(empty.header['ExposureTime']) *
                    (
            (
                float(empty.header['PSize_1']) /
                float(empty.header['SampleDistance']))
        )**2
        )/1e-15
        empty_1D = poni.integrate1d(empty.data,
                                    1000, filename=args.sample[:-4]+'_empty1D.dat', correctSolidAngle=True,
                                    method=intmeth, radial_range=(None), azimuth_range=(None),
                                    unit="q_A^-1", mask=mask.data, normalization_factor=norm_empty,
                                    metadata=None, error_model="poisson")

        empty_2D = empty.data/transmission_empty
        empty_1Df = empty_1D[1]

        if args.autobkg is True:
            if max(empty_1D[1][:np.where(empty_1D[0] > 0.02)[0][0]]) > max(data_1D[1][:np.where(data_1D[0] > 0.02)[0][0]]):
                empty_1Df = empty_1D[1] - max(empty_1D[1][:np.where(empty_1D[0] > 0.02)[
                                            0][0]]) - max(data_1D[1][:np.where(data_1D[0] > 0.02)[0][0]])

        if args.background is not None:
            data_I = ((data_1D[1]-empty_1Df) -
                    (bkg_1D[1]-empty_1Df))*transmission_sample
            data_2I = (data_2D-empty_2D)-(bkg_2D-empty_2D)
            data_sig = (abs(data_1D[2])+abs(empty_1D[2]) +
                        abs(bkg_1D[2])+abs(empty_1D[2]))*transmission_sample
        else:
            data_I = (data_1D[1]-empty_1Df)*transmission_sample
            data_2I = data_2D-empty_2D
            data_sig = (abs(data_1D[2])+abs(empty_1D[2]))*transmission_sample
    else:
        if args.background is None:
            data_I = data_1D[1]*transmission_sample
            data_2I = data_2D
            data_sig = abs(data_1D[2])*transmission_sample
        else:
            data_I = (data_1D[1]-bkg_1D[1])*transmission_sample
            data_2I = data_2D - bkg_2D
            data_sig = (abs(data_1D[2])+abs(bkg_1D[2]))*transmission_sample

    data_2I2 = poni.integrate2d(data_2I, 3000, 3600, unit="q_A^-1")

    I2, q2, chi2 = data_2I2

    if np.min(I2) < 0:
        I2min = 1e-3
    else:
        I2min = np.min(I2)
    I2max = np.max(I2)

    fig, axs = plt.subplot_mosaic(
        [['(a)', '(b)']], figsize=(7, 4), constrained_layout=True)

    fig1 = axs['(a)'].imshow(I2, origin="lower", extent=[q2.min(), q2.max(), chi2.min(), chi2.max()],
                            norm=LogNorm(vmin=I2min, vmax=I2max), cmap=plt.get_cmap('cividis'), aspect="auto")
    divider = make_axes_locatable(axs['(a)'])
    cax = divider.append_axes("top", size="5%", pad=0.05)

    cbar = plt.colorbar(fig1, cax=cax, orientation="horizontal")
    cbar.ax.tick_params(labelsize=8)
    cax.xaxis.set_ticks_position("top")

    axs['(a)'].set_xlabel(r'q /$\AA^{-1}$', fontsize=8)
    axs['(a)'].set_ylabel(r'$\phi/^{\circ}$', fontsize=8)
    axs['(a)'].tick_params(labelsize=8)

    fig2 = axs['(b)'].errorbar(data_1D[0], data_I, yerr=data_sig, linestyle='')

    axs['(b)'].set_xscale('log')
    axs['(b)'].set_yscale('log')
    axs['(b)'].set_xlabel(r'q /$\AA^{-1}$', fontsize=8)
    if np.allclose(args.lac,0):
        if np.allclose(args.thickness,1):
            axs['(b)'].set_ylabel('I(q) /Arb.', fontsize=8)

    else:
        axs['(b)'].set_ylabel(r'I(q) /cm$^{-1}$.', fontsize=8)
    axs['(b)'].get_xaxis().set_major_formatter(ticker.ScalarFormatter())
    # axs['(b)'].get_yaxis().set_major_formatter(ticker.ScalarFormatter())
    # axs['(b)'].ticklabel_format(style='sci', axis='both',
    #                             scilimits=(0, 0), useMathText=True)
    #axs['(b)'].set_xticks([0.01, 0.1, 1])
    # axs['(b)'].get_xaxis().set_major_formatter(ticker.ScalarFormatter())
    axs['(b)'].tick_params(labelsize=8)
    # plt.show()
    plt.savefig(args.sample[:-4]+".png", bbox_inches="tight",dpi=600)

    data_out = np.column_stack((data_1D[0], data_I, data_sig))
    np.savetxt(args.sample[:-4]+"_subtracted.dat",
            data_out, delimiter='\t', fmt='%s')

if __name__ == "__main__":
    cli()