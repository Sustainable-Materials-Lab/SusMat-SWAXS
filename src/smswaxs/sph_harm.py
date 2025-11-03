# -*- coding: utf-8 -*-
"""
Plot spherical harmonics functions from TOPAS coefficients.

This module visualizes spherical harmonics functions using coefficients
obtained from TOPAS academic output files.
"""

import click
import matplotlib.pyplot as plt
from scipy.special import factorial
from sympy.functions.special.polynomials import assoc_legendre
import numpy as np
from matplotlib import cm, colors

# pylint: disable=C0103


def Nlm(l, m):
    """Calculate normalization factor for spherical harmonics."""
    N = np.sqrt(((2*l+1)/(4*np.pi))*(factorial((l-m))/factorial((l+m))))
    return N


def spherical_harmonic(l, m, theta, phi=None):
    """
    Calculate real spherical harmonic Y_lm.
    
    Args:
        l: degree of the harmonic
        m: order of the harmonic (0 for m=0, positive for cos, negative for sin)
        theta: polar angle(s)
        phi: azimuthal angle(s), required if m != 0
    
    Returns:
        Real spherical harmonic values
    """
    if m == 0:
        return Nlm(l, 0) * assoc_legendre(l, 0, np.cos(theta))
    else:
        abs_m = abs(m)
        legendre_part = assoc_legendre(l, abs_m, np.cos(theta))
        norm = np.sqrt(2) * Nlm(l, abs_m)
        if m > 0:  # cosine term (p for plus)
            return norm * np.cos(abs_m * phi) * legendre_part
        else:  # sine term (m for minus)
            return norm * np.sin(abs_m * phi) * legendre_part


# Define the coefficient structure: (l, m) pairs
# m=0 for Y_l0, m>0 for cos terms (p), m<0 for sin terms (m)
COEFFICIENT_STRUCTURE = [
    (0, 0),   # c00
    (2, 0),   # c20
    (2, 2),   # c22p
    (2, -2),  # c22m
    (4, 0),   # c40
    (4, 2),   # c42p
    (4, -2),  # c42m
    (4, 4),   # c44p
    (4, -4),  # c44m
    (6, 0),   # c60
    (6, 2),   # c62p
    (6, -2),  # c62m
    (6, 4),   # c64p
    (6, -4),  # c64m
    (6, 6),   # c66p
    (6, -6),  # c66m
    (8, 0),   # c80
    (8, 2),   # c82p
    (8, -2),  # c82m
    (8, 4),   # c84p
    (8, -4),  # c84m
    (8, 6),   # c86p
    (8, -6),  # c86m
    (8, 8),   # c88p
    (8, -8),  # c88m
]

@click.command()
@click.argument('coefficients', nargs=-1, type=float, required=True)
@click.option('--output', '-o', default='sph_harm.svg',
              help='Output filename for the plot (default: sph_harm.svg)')
@click.option('--resolution', '-r', default=200,
              help='Angular resolution for the plot (default: 200)')
def cli(coefficients, output, resolution):
    """
    Plot spherical harmonics functions from TOPAS coefficients.
    
    Takes 1 to 25 coefficients and generates a 3D visualization of the spherical
    harmonics function. Coefficients should be provided in order:
    c00, c20, c22p, c22m, c40, c42p, c42m, c44p, c44m, c60, c62p, c62m, c64p, c64m,
    c66p, c66m, c80, c82p, c82m, c84p, c84m, c86p, c86m, c88p, c88m
    
    If fewer than 25 coefficients are provided, the remaining ones are assumed to be zero.
    This allows for 2nd order (5 coeffs), 4th order (9 coeffs), 6th order (16 coeffs), etc.
    
    Use '--' before coefficients if any are negative to prevent them being interpreted as options.
    
    Examples:
        # 2nd order (5 coefficients)
        sm-spharm -- 1 -0.54889 0.48504 0.74711 0.79916
        
        # 8th order (25 coefficients)
        sm-spharm -- 1 -0.54889 0.48504 0.74711 0.79916 -0.33178 0.16323 0.45369 \
                     -0.29782 -0.29214 -0.43949 0.01524 0.09042 0.85340 0.40316 \
                     -0.01881 1.47673 -0.55751 -0.68970 0.02621 -0.06565 -0.56472 \
                     1.00981 -0.12339 -0.25831
    """
    # Validate number of coefficients
    if len(coefficients) > 25:
        raise click.BadParameter(
            f'Too many coefficients: got {len(coefficients)}, maximum is 25'
        )
    
    # Pad coefficients with zeros if fewer than 25 provided
    coefficients = list(coefficients) + [0.0] * (25 - len(coefficients))
    
    # Create angular grid
    phi, theta = np.mgrid[0:2*np.pi:complex(0, resolution), 0:np.pi:complex(0, resolution//2)]
    
    # Calculate radial function R by summing all harmonics
    R = np.zeros_like(theta, dtype=float)
    
    for (l_val, m_val), coeff in zip(COEFFICIENT_STRUCTURE, coefficients):
        if m_val == 0:
            # For m=0, only theta is needed
            y_lm_func = np.frompyfunc(lambda t, lv=l_val, mv=m_val: spherical_harmonic(lv, mv, t), 1, 1)
            y_values = y_lm_func(theta).astype(float)
        else:
            # For m!=0, both theta and phi are needed
            y_lm_func = np.frompyfunc(lambda t, p, lv=l_val, mv=m_val: spherical_harmonic(lv, mv, t, p), 2, 1)
            y_values = y_lm_func(theta, phi).astype(float)
        
        R += coeff * y_values

    # Convert to Cartesian coordinates
    x = R*np.sin(theta)*np.cos(phi)
    y = R*np.sin(theta)*np.sin(phi)
    z = R*np.cos(theta)

    # Create 3D plot
    # pylint: disable=E1101
    _, ax = plt.subplots(subplot_kw=dict(projection='3d'), figsize=(14, 10))
    norm = colors.Normalize()
    ax.plot_surface(x, y, z, rstride=1, cstride=1, facecolors=cm.jet(norm(R)))
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Spherical Harmonics Visualization')

    # Save the plot
    plt.savefig(output, bbox_inches='tight')
    click.echo(f'Plot saved to {output}')


if __name__ == "__main__":
    # pylint: disable=E1120
    cli()
