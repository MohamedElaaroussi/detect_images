




import cv2
import numpy as np
import json
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

# Create the main window
root = tk.Tk()
root.title("Spot the Difference")

# Create the image selection widgets
image1_label = tk.Label(root, text="Image 1:")
image1_label.pack()

image1_button = tk.Button(root, text="Select Image 1", command=lambda: select_image("image1"))
image1_button.pack()

image2_label = tk.Label(root, text="Image 2:")
image2_label.pack()

image2_button = tk.Button(root, text="Select Image 2", command=lambda: select_image("image2"))
image2_button.pack()

# Global variables to store the selected images
image1 = None
image2 = None

def select_image(image_name):
    global image1, image2
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.gif")])
    if file_path:
        if image_name == "image1":
            image1 = cv2.imread(file_path)
        else:
            image2 = cv2.imread(file_path)
        print(f"Selected {image_name}: {file_path}")

def generate_difference():
    global image1, image2

    # Check if the images were loaded successfully
    if image1 is None:
        print("Error: Image 1 not selected.")
        return
    if image2 is None:
        print("Error: Image 2 not selected.")
        return

    # Check the dimensions of the two images
    print(f"Image 1 shape: {image1.shape}")
    print(f"Image 2 shape: {image2.shape}")

    # If the images have different dimensions, resize image1 to match image2
    if image1.shape != image2.shape:
        image1 = cv2.resize(image1, (image2.shape[1], image2.shape[0]))
        print("Resized image1 to match image2 dimensions.")

    # Compute the difference between the two images
    difference = cv2.subtract(image1, image2)

    # Convert the difference to grayscale and apply Otsu's thresholding
    Conv_hsv_Gray = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(Conv_hsv_Gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

    # Color the differences in red
    difference[mask != 255] = [0, 0, 255]
    image1[mask != 255] = [0, 0, 255]
    image2[mask != 255] = [0, 0, 255]

    # Save the modified images
    cv2.imwrite('diffOverImage1.png', image1)
    cv2.imwrite('diffOverImage2.png', image2)

    # Open a file dialog to select the download location
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")], initialfile="difference.json")

    if file_path:
        json_data = {'red_objects': []}
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            json_data['red_objects'].append(f"Object at ({x}, {y}) with size ({w}, {h})")

        with open(file_path, 'w') as f:
            json.dump(json_data, f)
        print(f"JSON file downloaded to: {file_path}")

        # Open a file dialog to select the image download location
        image_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")], initialfile="difference.png")
        if image_path:
            cv2.imwrite(image_path, difference)
            print(f"Image file downloaded to: {image_path}")

# Create the "Generate Difference" button
generate_button = tk.Button(root, text="Generate Difference", command=generate_difference)
generate_button.pack()

# Run the main event loop
root.mainloop()