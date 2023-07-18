import numpy as np
import scipy


def clamp(z, vmin=0, vmax=1):
    return np.minimum(vmax * np.ones(z.shape),
                      np.maximum(vmin * np.ones(z.shape), z))


def gradient_angle(z):
    dx, dy = np.gradient(z, axis=0), np.gradient(z, axis=1)
    return np.arctan2(dy, dx)


def gradient_norm(z):
    dx, dy = np.gradient(z, axis=0), np.gradient(z, axis=1)
    return np.hypot(dx, dy)


def gaussian_curvature(z, sigma=2):
    z = scipy.ndimage.gaussian_filter(z, sigma=sigma)
    
    zx, zy = np.gradient(z)
    zxx, zxy = np.gradient(zx)
    _, zyy = np.gradient(zy)

    # Gaussian curvature = K1 * K2
    k = (zxx * zyy - (zxy**2)) / (1 + (zx**2) + (zy**2))**2
    # mean curvature = (K1 + K2)/2
    h = (zxx * (1 + zy**2) - 2 * zxy * zx * zy + zyy *
         (1 + zx**2)) / 2 / (1 + zx**2 + zy**2)**1.5

    return k, h


def hillshade(z, azimuth, zenith, talus_ref):
    azimuth_rad = np.pi * azimuth / 180
    zenith_rad = np.pi * zenith / 180

    aspect = gradient_angle(z)
    dn = gradient_norm(z) / talus_ref
    slope = np.arctan(dn)

    sh = np.cos(zenith_rad) * np.cos(slope) \
        + np.sin(zenith_rad) * np.sin(slope) * np.cos(azimuth_rad - aspect)
    
    return (sh - sh.min()) / sh.ptp()
