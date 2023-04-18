from osgeo import gdal
import numpy as np
import util
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()  # Hide the main window

print("Select the multispectral image")
ms_path = filedialog.askopenfilename()  # Show the file dialog box

if ms_path:
    print("Selected file path:", ms_path)
else:
    print("No multispectral image selected")
    exit(0)

print("Select the panchromatic image")
pan_path = filedialog.askopenfilename()  # Show the file dialog box

if pan_path:
    print("Selected file path:", pan_path)
else:
    print("No panchromatic image selected")
    exit(0)

ms_src = gdal.Open(ms_path)
ms_bands = ms_src.RasterCount
ms_img = ms_src.ReadAsArray()
ms_img = np.transpose(ms_img, (1, 2, 0))

dtype = ms_img.dtype
print(dtype)
max_val = np.iinfo(dtype).max
min_val = np.iinfo(dtype).min

pan_src = gdal.Open(pan_path)
pan_bands = pan_src.RasterCount
pan_img = pan_src.ReadAsArray()

ms_img = util.resize_image(ms_img, pan_img.shape[0], pan_img.shape[1])

pcs, eigs = util.pca_image(ms_img) 

x = pcs
pan_adjusted = (pan_img - pan_img.mean()) * (np.std(x) / pan_img.std()) + x.mean()
x[:,:,0] = pan_adjusted

pan_sharpened = util.inverse_pca_image(x, eigs)

pan_sharpened = np.clip(pan_sharpened, np.iinfo(dtype).min, np.iinfo(dtype).max)
pan_sharpened = pan_sharpened.astype(dtype)

util.write_geotiff(pan_sharpened, "pansharpened.tif", ms_src.GetGeoTransform(), ms_src.GetProjection(), dtype)
print("Wrote the pansharpened image in pansharpened.tif")
