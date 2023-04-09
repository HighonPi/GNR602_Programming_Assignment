from osgeo import gdal
import numpy as np
from PIL import Image

# Open the GeoTIFF file
src = gdal.Open("ms.tif")

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
image.save("rgb_image.png")
