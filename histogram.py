import cv2
import matplotlib.pyplot as plt

# Load the image
image = cv2.imread('your_image_path.jpg', cv2.IMREAD_GRAYSCALE)

# Calculate the histogram
histogram = cv2.calcHist([image], [0], None, [256], [0, 256])

# Plot the histogram
plt.plot(histogram)
plt.title('Histogram')
plt.xlabel('Pixel Value')
plt.ylabel('Frequency')
plt.savefig('your_image_path_histogram.png')
plt.show()