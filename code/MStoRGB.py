from osgeo import gdal
import numpy as np
from PIL import Image
import sys

if len(sys.argv) != 3:
    print("Run as 'python MStoRGB.py [path of geotiff] [output file name]'")
    exit(0)

# Open the GeoTIFF file
src = gdal.Open(sys.argv[1])

# Get the RGB bands (bands 1, 2, and 3)
red_band = src.GetRasterBand(1).ReadAsArray()
green_band = src.GetRasterBand(2).ReadAsArray()
blue_band = src.GetRasterBand(3).ReadAsArray()

# Stack the bands into a 3D array and convert to 8 bit pixel values
rgb = np.dstack((red_band, green_band, blue_band))
rgb = (rgb / 8).astype(np.uint8)

# Create an Image object from the RGB array
image = Image.fromarray(rgb, 'RGB')

# Save the image to disk
image.save(sys.argv[2])
