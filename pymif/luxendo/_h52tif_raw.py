import os, tqdm, h5py, glob
import numpy as np
from skimage.io import imsave

def h52tif_raw(exp_folder, downscale=1):

    folder = os.path.join(exp_folder, 'raw')
    print(folder)

    # find all subfolders: all images
    list_subfolders_with_paths = [f.path for f in os.scandir(folder) if f.is_dir()]
    list_subfolders_with_paths.sort()
    print('Found ',len(list_subfolders_with_paths), 'images.')

    for path in tqdm.tqdm(list_subfolders_with_paths):
        # find the only image within the subfolder
        fname = glob.glob(os.path.join(path,'*.h5'))[0]
        f = h5py.File(fname, 'r')
        dset = np.array(f['Data']).astype(np.uint16)

        # extract channel name and angle
        ch = int(fname[fname.index('channel')+8])
        if 'left' in fname:
            obj='left'
        elif 'right' in fname:
            obj='right'

        # extract tile if any
        tilepos = 'x00y00'
        if ('-x' in fname) and ('-y' in fname):
            tilepos = fname[fname.index('-x')+1:fname.index('-x')+8]

        # if it's the right camera, flip it horizontally
        if obj == 'right':
            dset = dset[:,:,::-1]

        dset = dset[:,::downscale,::downscale]
        # print(dset.shape)

        # create name of new file
        new_name = os.path.join(folder,'ch-%d_%s_obj-%s_bin-%d%d1.tif'%(ch,tilepos,obj,downscale,downscale))

        # save image as tif file
        imsave(new_name, dset.astype(np.uint16), check_contrast=False)
