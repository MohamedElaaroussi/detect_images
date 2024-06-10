import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np

def select_image1():
    global image1
    image1_path = filedialog.askopenfilename(title="Select Image 1", filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")])
    if image1_path:
        image1 = cv2.imread(image1_path)
        print("Selected image1:", image1_path)
        print("Image 1 shape:", image1.shape)

def select_image2():
    global image2
    image2_path = filedialog.askopenfilename(title="Select Image 2", filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")])
    if image2_path:
        image2 = cv2.imread(image2_path)
        print("Selected image2:", image2_path)
        print("Image 2 shape:", image2.shape)

def generate_difference():
    global image1, image2
    if image1 is None or image2 is None:
        return

    # Calculate the absolute difference between the two images
    diff = cv2.absdiff(image1, image2)

    # Display the difference image
    cv2.imwrite("diffOverImage1.png", diff)
    print("Difference image saved as 'diffOverImage1.png'.")

root = tk.Tk()
root.title("Saizeriya Spot the Difference")

image1 = None
image2 = None

select_image1_button = tk.Button(root, text="Select Image 1", command=select_image1)
select_image1_button.pack(pady=10)

select_image2_button = tk.Button(root, text="Select Image 2", command=select_image2)
select_image2_button.pack(pady=10)

generate_difference_button = tk.Button(root, text="Generate Difference", command=generate_difference)
generate_difference_button.pack(pady=10)

root.mainloop()