from osgeo import gdal
import numpy as np
from PIL import Image

# Open the GeoTIFF file
src = gdal.Open("pan.tif")

# Get the RGB bands (bands 1, 2, and 3)
gray_band = src.GetRasterBand(1).ReadAsArray()

# Stack the bands into a 3D array
gray_band = (gray_band / 8).astype(np.uint8)

# Create an Image object from the RGB array
image = Image.fromarray(gray_band, 'L')

# Save the image to disk
image.save("gray.png")
