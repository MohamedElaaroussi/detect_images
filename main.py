

# import sys
# import cv2
# import numpy as np

# if len(sys.argv) == 2:
#     filename = sys.argv[1]
# else:
#     print('Usage: python main.py <filename.png>', file=sys.stderr)
#     sys.exit(1)

# img_src = cv2.imread('./%s' % filename, cv2.IMREAD_COLOR)

# # 余白を取り除いたときに2つの画像が最も一致するような適切な余白（padding）の幅を見つける

# img_diffs = []
# for padding in range(10, 50):
#     # 画像の余白を削除
#     img = img_src[:, padding:-padding]

#     # 画像を左右で分割する
#     height, width, channels = img.shape[:3]
#     img1 = img[:, :width//2]
#     img2 = img[:, width//2:]

#     # 2つの画像の差分を算出
#     img_diff = cv2.absdiff(img2, img1)
#     img_diff_sum = np.sum(img_diff)

#     img_diffs.append((img_diff, img_diff_sum))

# # 差分が最も少ないものを選ぶ
# img_diff, _ = min(img_diffs, key=lambda x: x[1])


# tmp = filename.split('.')
# filename = '.'.join([tmp[0] + '-diff', *tmp[1:]])
# cv2.imwrite('./%s' % filename, img_diff)

















# import cv2
# import numpy as np
# import tkinter as tk
# from tkinter import filedialog, ttk

# def compare_images(image1, image2):
#     """
#     Compares two images and returns a new image with the differences highlighted.
    
#     Args:
#         image1 (str): Path to the first image.
#         image2 (str): Path to the second image.
    
#     Returns:
#         numpy.ndarray: The image with the differences highlighted.
#     """
#     # Charger les images
#     img1 = cv2.imread(image1)
#     img2 = cv2.imread(image2)
    
#     # Redimensionner les images pour qu'elles aient la même taille
#     height = max(img1.shape[0], img2.shape[0])
#     width = max(img1.shape[1], img2.shape[1])
#     img1 = cv2.resize(img1, (width, height))
#     img2 = cv2.resize(img2, (width, height))
    
#     # Calculer la différence entre les deux images
#     diff = cv2.absdiff(img1, img2)
    
#     # Convertir l'image diff en niveaux de gris
#     diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    
#     # Trouver les contours des objets différents
#     contours, _ = cv2.findContours(diff, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
#     # Créer une nouvelle image avec les différences soulignées
#     diff_img = cv2.addWeighted(img1, 0.5, img2, 0.5, 0)
#     for cnt in contours:
#         x, y, w, h = cv2.boundingRect(cnt)
        
#         # Réduire la taille de la zone détectée
#         x = max(0, x - 5)
#         y = max(0, y - 5)
#         w = min(width - x, w + 10)
#         h = min(height - y, h + 10)
        
#         cv2.rectangle(diff_img, (x, y), (x+w, y+h), (0, 0, 255), 4)
    
#     diff_img = cv2.cvtColor(diff_img, cv2.COLOR_BGR2RGB)
    
#     return diff_img

# class ImageComparisonGUI:
#     def __init__(self, master):
#         self.master = master
#         master.title("Image Comparison")

#         # Créer les widgets
#         self.label1 = tk.Label(master, text="Image 1")
#         self.label1.grid(row=0, column=0)

#         self.button1 = tk.Button(master, text="Choisir Image 1", command=self.select_image1)
#         self.button1.grid(row=1, column=0)

#         self.label2 = tk.Label(master, text="Image 2")
#         self.label2.grid(row=0, column=1)

#         self.button2 = tk.Button(master, text="Choisir Image 2", command=self.select_image2)
#         self.button2.grid(row=1, column=1)

#         self.button_compare = tk.Button(master, text="Comparer les images", command=self.compare_images)
#         self.button_compare.grid(row=2, column=0, columnspan=2)

#         self.progress_bar = ttk.Progressbar(master, mode='indeterminate')

#         self.image1_path = None
#         self.image2_path = None

#     def select_image1(self):
#         self.image1_path = filedialog.askopenfilename()

#     def select_image2(self):
#         self.image2_path = filedialog.askopenfilename()

#     def compare_images(self):
#         if self.image1_path and self.image2_path:
#             self.progress_bar.grid(row=3, column=0, columnspan=2, pady=10)
#             self.progress_bar.start()

#             difference_image = compare_images(self.image1_path, self.image2_path)

#             self.progress_bar.stop()
#             self.progress_bar.grid_forget()

#             # Afficher la différence
#             cv2.imshow('Différence', difference_image)
#             cv2.waitKey(0)
#             cv2.destroyAllWindows()
#         else:
#             tk.messagebox.showerror("Erreur", "Veuillez sélectionner les deux images.")

# root = tk.Tk()
# app = ImageComparisonGUI(root)
# root.mainloop()




















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