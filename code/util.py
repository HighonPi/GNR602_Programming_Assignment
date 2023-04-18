import numpy as np
from osgeo import gdal

def resize_image(image, target_height, target_width):
    # Get the height, width, and number of bands of the input image
    height, width, num_bands = image.shape

    # Create a 2D array of coordinates for the resized image
    y_coords, x_coords = np.meshgrid(np.arange(target_height), np.arange(target_width), indexing='ij')

    # Calculate the scale factor for the height and width
    scale_factor_y = float(target_height) / float(height)
    scale_factor_x = float(target_width) / float(width)

    # Calculate the corresponding pixel coordinates in the input image
    x_input = x_coords / scale_factor_x
    y_input = y_coords / scale_factor_y

    # Convert the input coordinates to integers
    x_floor = np.floor(x_input).astype(np.int32)
    x_ceil = np.ceil(x_input).astype(np.int32)
    y_floor = np.floor(y_input).astype(np.int32)
    y_ceil = np.ceil(y_input).astype(np.int32)

    # Ensure the pixel coordinates are within the image bounds
    x_floor = np.clip(x_floor, 0, width-1)
    x_ceil = np.clip(x_ceil, 0, width-1)
    y_floor = np.clip(y_floor, 0, height-1)
    y_ceil = np.clip(y_ceil, 0, height-1)

    # Get the pixel values at the four nearest pixel coordinates
    pixel_floor_floor = image[y_floor, x_floor]
    pixel_floor_ceil = image[y_floor, x_ceil]
    pixel_ceil_floor = image[y_ceil, x_floor]
    pixel_ceil_ceil = image[y_ceil, x_ceil]

    # Interpolate the pixel values using bilinear interpolation
    x_frac = x_input - x_floor
    x_frac = np.repeat(x_frac[:, :, np.newaxis], num_bands, axis = 2)

    y_frac = y_input - y_floor
    y_frac = np.repeat(y_frac[:, :, np.newaxis], num_bands, axis = 2)

    pixel_interpolated = pixel_floor_floor * (1 - x_frac) * (1 - y_frac) + \
                         pixel_floor_ceil * x_frac * (1 - y_frac) + \
                         pixel_ceil_floor * (1 - x_frac) * y_frac + \
                         pixel_ceil_ceil * x_frac * y_frac

    # Reshape the pixel values to match the target image shape
    resized_image = pixel_interpolated.reshape(target_height, target_width, num_bands)

    return resized_image

def pca_image(image, n_components=None):
    # Vectorize the image pixels
    pixel_values = np.reshape(image, (image.shape[0] * image.shape[1], image.shape[2]))

    # Compute the covariance matrix of the pixel values
    covariance_matrix = np.cov(pixel_values, rowvar=False)

    # Perform an eigen decomposition of the covariance matrix
    eigenvalues, eigenvectors = np.linalg.eigh(covariance_matrix)

    # Sort the eigenvalues and eigenvectors in descending order
    idx = eigenvalues.argsort()[::-1]
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]

    # Optionally reduce the number of components to keep
    if n_components is not None:
        eigenvectors = eigenvectors[:, :n_components]

    # Project the pixel values onto the principal components
    projected_pixel_values = np.dot(pixel_values, eigenvectors)

    # Reshape the projected pixel values into an image
    projected_image = np.reshape(projected_pixel_values, (image.shape[0], image.shape[1], eigenvectors.shape[1]))

    # Return the projected image and the eigenvectors for inverse PCA
    return projected_image, eigenvectors

def inverse_pca_image(projected_image, eigenvectors):
    # Reshape the projected image into a 2D matrix
    projected_pixel_values = np.reshape(projected_image, (projected_image.shape[0] * projected_image.shape[1], projected_image.shape[2]))

    # Compute the inverse projection of the pixel values
    inverted_pixel_values = np.dot(projected_pixel_values, eigenvectors.T)

    # Reshape the inverted pixel values into an image
    inverted_image = np.reshape(inverted_pixel_values, (projected_image.shape[0], projected_image.shape[1], eigenvectors.shape[0]))

    return inverted_image



def write_geotiff(array, output_path, geotransform, projection, dtype):
    dtype_to_gdal = {
        np.dtype('uint8'): gdal.GDT_Byte,
        np.dtype('uint16'): gdal.GDT_UInt16,
        np.dtype('uint32'): gdal.GDT_UInt32,
        np.dtype('int8'): gdal.GDT_Byte,
        np.dtype('int16'): gdal.GDT_Int16,
        np.dtype('int32'): gdal.GDT_Int32,
        np.dtype('float32'): gdal.GDT_Float32,
        np.dtype('float64'): gdal.GDT_Float64,
    }   

    # Open a new GDAL dataset for writing
    driver = gdal.GetDriverByName('GTiff')
    height, width, num_bands = array.shape
    dataset = driver.Create(output_path, width, height, num_bands, dtype_to_gdal[dtype])

    # Set the geotransform and projection of the dataset
    dataset.SetGeoTransform(geotransform)
    dataset.SetProjection(projection)

    # Write the array data to the dataset
    for band in range(num_bands):
        dataset.GetRasterBand(band + 1).WriteArray(array[:, :, band])

    # Flush the dataset to disk
    dataset.FlushCache()
