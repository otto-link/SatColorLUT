import glob
import matplotlib.pyplot as plt
import numpy as np
import os

import tools.clut
import tools.mymath

if __name__ == '__main__':
    print('Applying CLUT...')

    dir_list = glob.glob('data/*')
    cmap_list = [os.path.basename(d) for d in dir_list if os.path.isdir(d)]
    
    for cmap in cmap_list:
        print(cmap)
        
        # raw DEM
        z = tools.clut.load_img('data/test_hmap.png')[:, :, 0]

        # compute features used to colorize
        dz = tools.mymath.gradient_norm(z)
        _, dh = tools.mymath.gaussian_curvature(z)
        dzx, dzy = np.gradient(z)

        # colorize
        clut3 = np.load(cmap + '_3.npy')
        img3 = tools.clut.apply_clut((z, dzx, dzy), clut3)

        # add hillshading
        sh = tools.mymath.hillshade(z, 180, 45, 10 * z.ptp() / z.shape[0])
        for k in range(3):
            img3[:, :, k] = (sh**0.5 * img3[:, :, k]).astype(int)

        # plt.figure()
        # plt.imshow(img3)
        # plt.axis('off')

        plt.imsave(cmap + '.png', img3.astype(np.uint8))
        
    # plt.show()
