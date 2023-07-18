import matplotlib.pyplot as plt
import numpy as np
import os

import tools.clut
import tools.mymath

if __name__ == '__main__':
    print('Generating CLUT...')

    clut_res = 64

    for cmap in ['amazon', 'china', 'desert', 'himalaya', 'sahara', 'snow', 'stone', 'swamp']:
        print(cmap)

        # See https://worldview.earthdata.nasa.gov to get data
        fname_dem = os.path.join('data', cmap, 'dem.png')
        fname_col = os.path.join('data', cmap, 'aerial.png')

        # CLUT based on elevation and gradient components
        z = tools.clut.load_img(fname_dem)[:, :, 0]
        dz = tools.mymath.gradient_norm(z)
        dzx, dzy = np.gradient(z)

        clut3 = tools.clut.generate_clut((z, dzx, dzy),
                                         fname_col=fname_col,
                                         clut_shape=(clut_res, clut_res, clut_res))

        np.save(cmap + "_3.npy", clut3)
    
    plt.show()
