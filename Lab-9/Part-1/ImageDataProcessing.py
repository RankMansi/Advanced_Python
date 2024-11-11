from PIL import Image, ImageFilter, ImageOps
import matplotlib.pyplot as plt
import numpy as np

# Part 1: Image Data Processing

# 1. Image Loading and Display
def load_and_display_image(image_path):
    image = Image.open(image_path)
    image.show(title="Original Image")
    return image

# 2. Image Manipulation
def apply_image_manipulations(image):
    # Resize image
    resized_image = image.resize((200, 200))
    resized_image.show(title="Resized Image")
    
    # Convert to grayscale
    grayscale_image = ImageOps.grayscale(image)
    grayscale_image.show(title="Grayscale Image")
    
    # Apply Gaussian Blur
    blurred_image = image.filter(ImageFilter.GaussianBlur(5))
    blurred_image.show(title="Gaussian Blur")
    
    # Edge Detection
    edge_image = image.filter(ImageFilter.FIND_EDGES)
    edge_image.show(title="Edge Detection")
    
    return resized_image, grayscale_image, blurred_image, edge_image

# 3. Histogram Analysis
def plot_histogram(image):
    # Convert image to RGB if it's not already
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Get image data as a numpy array
    image_data = np.array(image)
    
    # Initialize histogram data
    colors = ('r', 'g', 'b')
    hist_data = []

    # Calculate histograms for each color channel (R, G, B)
    for i, color in enumerate(colors):
        hist, _ = np.histogram(image_data[:, :, i].flatten(), bins=256, range=(0, 256))
        hist_data.append(hist)
    
    # 6) Graph: Line Plot for Histogram
    plt.figure(figsize=(10, 5))
    plt.plot(hist_data[0], color='red', label='Red Channel')
    plt.plot(hist_data[1], color='green', label='Green Channel')
    plt.plot(hist_data[2], color='blue', label='Blue Channel')
    plt.title('Color Histogram')
    plt.xlabel('Bins')
    plt.ylabel('# of Pixels')
    plt.legend()
    plt.grid()
    plt.show()

    # 7) Histogram: Bar Plot for Histogram
    plt.figure(figsize=(10, 5))
    bar_width = 5  # Increased bar width for thicker bars
    x = np.arange(256)

    # Plotting the bar graph
    plt.bar(x - bar_width, hist_data[0], width=bar_width, color='red', label='Red Channel', alpha=0.8)
    plt.bar(x, hist_data[1], width=bar_width, color='green', label='Green Channel', alpha=0.8)
    plt.bar(x + bar_width, hist_data[2], width=bar_width, color='blue', label='Blue Channel', alpha=0.8)

    plt.title('Color Histogram (Separate Bars)')
    plt.xlabel('Color Value Ranges')
    plt.ylabel('# of Pixels')
    plt.xticks(x[::20], rotation=45)  # Show every 20th bin for clarity
    plt.legend()
    plt.grid(axis='y')
    plt.ylim(0, max(max(hist_data[0]), max(hist_data[1]), max(hist_data[2])) * 1.1)  # Set y-axis limit for better view
    plt.tight_layout()  # Adjust layout to avoid clipping of tick-labels
    plt.show()

# Main function to run all steps
def main(image_path):
    print("Rank Mansi")
    print("22BCP284")

    # Load and display image
    image = load_and_display_image(image_path)
    
    # Apply manipulations
    resized_image, grayscale_image, blurred_image, edge_image = apply_image_manipulations(image)
    
    # Plot histogram for original image
    plot_histogram(image)

# Provide the path to your image file here
image_path = r'Lab-9\Part-1\kedar.jpg'  # Use raw string to avoid issues with backslashes
main(image_path)
