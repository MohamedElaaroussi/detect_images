
# # サイゼリアの間違い探しを見つけるプログラム

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

# load images
image1 = cv2.imread("testt.jfif")
image2 = cv2.imread("testtt.jfif")

# compute difference
difference = cv2.subtract(image1, image2)

# color the mask red
Conv_hsv_Gray = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold(Conv_hsv_Gray, 0, 255,cv2.THRESH_BINARY_INV |cv2.THRESH_OTSU)
difference[mask != 255] = [0, 0, 255]

# add the red mask to the images to make the differences obvious
image1[mask != 255] = [0, 0, 255]
image2[mask != 255] = [0, 0, 255]

# store images
cv2.imwrite('diffOverImage1.png', image1)
cv2.imwrite('diffOverImage2.png', image1)
cv2.imwrite('diff.png', difference)