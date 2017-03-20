import numpy as np
import scipy.constants as c

from wk2 import cartesian_to_spherical
from wk4 import angular_wave_func, radial_wave_func


a = c.physical_constants['Bohr radius'][0]

def hydrogen_wave_func(n, l, m, r_max, *n_xyz):
    x, y, z = [np.linspace(-r_max, r_max, n_dim) for n_dim in n_xyz]
    cartesian_mesh   = np.meshgrid(x, y, z)

    r3, theta3, phi3 = np.vectorize(cartesian_to_spherical)(*cartesian_mesh)
    r3              *= a

    ang_func, rad_func = map(np.vectorize, [angular_wave_func, radial_wave_func])
    ang_mag,  rad_mag  = ang_func(m,l,theta3,phi3), rad_func(n,l,r3)

    density = np.absolute(ang_mag*rad_mag)**2
    density = np.round(density)

    return tuple([np.round(arr) for arr in (tuple(cartesian_mesh) + (density,))])
