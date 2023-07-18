import matplotlib.pyplot as plt
import numpy as np
import scipy

import tools.mymath


def load_img(fname):
    return (plt.imread(fname) * 255).astype(int)


def generate_clut(features,
                  fname_col,
                  clut_shape):

    nfeatures = len(features)
    
    # reference colors
    img_col = load_img(fname_col)

    # initialize color LUT => clut_shape + 4 color channels
    clut = 255 * np.ones(clut_shape + (4,), dtype=int)

    # prepare grids and data
    lspace = ()
    for i in range(nfeatures):
        lspace += (np.linspace(features[i].min(), features[i].max(), clut_shape[i]),)   
    Xg = np.meshgrid(*lspace, indexing='ij')
    Xitp = ()
    for i in range(nfeatures):
        Xitp += (Xg[i].ravel(),)

    X = ()
    for i in range(nfeatures):
        X += (features[i].ravel(),)
    X = list(zip(*X))
    
    for k in range(3):
        v = img_col[..., k].ravel()
        fitp = scipy.interpolate.NearestNDInterpolator(X, v)
        tk = fitp(*Xitp).reshape(clut_shape)
        tk = scipy.ndimage.gaussian_filter(tk, sigma=1)
        clut[..., k] = tk
        
    return clut


def apply_clut(features, clut):
    img_out = 255 * np.ones((features[0].shape[0], features[0].shape[1], 4), dtype=int)
    nfeatures = len(features)
    clut_shape = clut.shape[:-1]
    
    lspace = ()
    for i in range(nfeatures):
        lspace += (np.linspace(features[i].min(), features[i].max(), clut_shape[i]),)   
    Xg = np.meshgrid(*lspace, indexing='ij')
    X = ()
    for i in range(nfeatures):
        X += (Xg[i].ravel(),)

    Xitp = ()
    for i in range(nfeatures):
        Xitp += (features[i].ravel(),)
    Xitp = list(zip(*Xitp))

    for k in range(3):
        v = clut[..., k].ravel()
        fitp = scipy.interpolate.NearestNDInterpolator(X, v)
        img_out[..., k] = fitp(Xitp).reshape(features[0].shape)

    return img_out
