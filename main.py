import os
import cv2
import tkinter as tk
from tkinter import filedialog, Label, Button, Frame, messagebox
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.efficientnet import preprocess_input
from PIL import Image, ImageTk

# Auto-detect model path
script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, "model", "brain_tumor_model.keras")
icon_path = os.path.join(script_dir, "brain-cancer.png")

# Load the trained model
if os.path.exists(model_path):
    model = tf.keras.models.load_model(model_path)
else:
    raise FileNotFoundError(f"Model file not found at {model_path}")

# Model classes (match folder names exactly)
class_names = ["glioma", "meningioma", "no tumor", "pituitary"]

# Function to open an image
def open_image():
    file_path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg;*.png;*.jpeg")])
    if file_path:
        result_label.config(text="🔄 Analyzing...", fg="#F8C471")
        root.update_idletasks()
        predict_image(file_path)

# Function to predict and display result
def predict_image(img_path):
    try:
        true_label = os.path.basename(os.path.dirname(img_path)).lower()

        img = cv2.imread(img_path)
        if img is None:
            result_label.config(text="❌ Error: Image not found", fg="red")
            return

        if len(img.shape) == 2 or img.shape[-1] == 1:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        elif img.shape[-1] == 4:
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
        else:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Updated size and preprocessing
        img = cv2.resize(img, (260, 260))  
        img = preprocess_input(img)  
        img_array = np.expand_dims(img, axis=0)

        prediction = model.predict(img_array)
        predicted_class = class_names[np.argmax(prediction)].lower()

        display_image(img_path)
        result_label.config(
            text=f"📌 True Label: {true_label}\n🧠 Predicted Label: {predicted_class}",
            fg="#4CAF50"
        )

    except Exception as e:
        result_label.config(text=f"❌ Error: {str(e)}", fg="red")

# Display selected image
def display_image(img_path):
    img = Image.open(img_path).resize((250, 250))
    img = ImageTk.PhotoImage(img)
    image_label.config(image=img)
    image_label.image = img

# Team info
def show_team():
    messagebox.showinfo("Development Team", "Development by:\n- Bouagal Houssem Eddine")

# Tkinter window
root = tk.Tk()
root.title("Brain Tumor Classification")
root.geometry("450x600")
root.resizable(False, False)
root.configure(bg="#222831")

# Set icon
if os.path.exists(icon_path):
    icon_image = Image.open(icon_path)
    icon_photo = ImageTk.PhotoImage(icon_image)
    root.iconphoto(False, icon_photo)

# Styling
btn_style = {"font": ("Arial", 12, "bold"), "bg": "#00ADB5", "fg": "white", "bd": 0, "relief": "flat", "padx": 10, "pady": 5}
label_style = {"font": ("Arial", 14, "bold"), "fg": "#EEEEEE", "bg": "#222831"}

frame = Frame(root, bg="#222831")
frame.pack(pady=20)

header_label = tk.Label(frame, text="Brain Tumor Detection", font=("Arial", 18, "bold"), bg="#222831", fg="white", pady=10)
header_label.pack(fill=tk.X, pady=10)

btn_load = Button(frame, text="📂 Load Image", command=open_image, **btn_style)
btn_load.pack(pady=10)

image_label = Label(frame, bg="#393E46")
image_label.pack(pady=10)

result_label = Label(frame, text="", **label_style)
result_label.pack(pady=20)

button_frame = Frame(root, bg="#222831")
button_frame.pack(pady=10)
team_button = Button(button_frame, text="Dev by", font=("Arial", 12), bg="#FFC107", fg="black", command=show_team)
team_button.pack()

root.mainloop()
