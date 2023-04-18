# GNR602 Programming Assignment
## Topic
PCA based pan-sharpening algorithm assuming geo-referencing of the datasets is already done

## Detailed writeup on the algorithm
PCA-based pansharpening is a technique for fusing a panchromatic (grayscale) image with a multispectral (RGB) image to create a single high-resolution, full-color image.

The first step in the algorithm is to upscale the multispectral image to the same size as the panchromatic image, but with less color information. This is done to ensure that the upscaled multispectral image has a similar level of detail to the panchromatic image.

Next, both the panchromatic and the upscaled multispectral images are reshaped into a three-dimensional multivariate array, with each pixel represented as a vector in RGB color space.

The next step involves applying PCA to the multivariate array to obtain the principal components and the projections of the data onto the PCA space. The first principal component is typically related to the overall brightness or luminosity of the data, while the remaining principal components capture more subtle variations in color.

To perform the pansharpening, the first projection is replaced with the panchromatic image, which is appropriately scaled to have the same luminosity as the original data. This step ensures that the final pansharpened image has the same level of brightness as the original data. Specifically, the panchromatic image is scaled so that its minimum and maximum values match those of the luminosity values in the multispectral image. Then, the scaled panchromatic image is substituted for the first projection in the PCA space.

The inverted projection is then rescaled and multiplied by the principal components to obtain the final image in RGB space. This is done by first applying the inverse PCA transform to the rescaled projection, which yields a multivariate array in RGB space. The inverse PCA transform involves multiplying the rescaled projection by the transpose of the principal component matrix, which effectively transforms the data back into the original RGB space.

Finally, the data is reshaped into an RGB image and saved to a file.

The resulting image is a pansharpened image that combines the high spatial resolution of the panchromatic image with the spectral information of the multispectral image, resulting in a high-resolution, full-color image.

## Instructions to run the code
1. Run pansharpen.py
2. Choose the multispectral image and then choose the panchromatic image 
3. The pansharpened image will get created in the current directory
