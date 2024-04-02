import tkinter as tk
from PIL import Image, ImageTk
import webbrowser
import os
from tkinter import ttk
from tkinter import filedialog
import fitz  # PyMuPDF

# Create the main window
root = tk.Tk()
root.title("Jacobian")
root.geometry("350x690")
root.configure(bg='black')

# Function to create the launch screen
def launch_screen():
    clear_widgets(root)

    # Add an image to the launch screen
    try:
        img = Image.open("logo.png")  # Replace "launch_image.png" with your own image path
        img = img.resize((300, 200), Image.LANCZOS)  # Adjust the size of the image to fit the window
        photo_img = ImageTk.PhotoImage(img)

        img_label = tk.Label(root, image=photo_img, bg="black")
        img_label.image = photo_img
        img_label.pack()
        img_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Call the main screen function after 3 seconds
        root.after(3000, main_screen)
    except FileNotFoundError:
        print("Launch image not found")


# Function to switch to the main screen
def open_subject_screen(subject):
    if subject in ["Physics", "Chemistry"]:
        coming_soon_screen(subject)
    elif subject == "Math":
        modules_screen("Math")
    else:
        main_screen(subject)

# Function to create the main screen
def main_screen(subject=None):
    # Clear the previous widgets
    clear_widgets(root)

    # Create labels for subjects
    subject_label = tk.Label(root, text="Subjects", font=("Arial", 25, "bold"), bg="black", fg="white")
    subject_label.pack(pady=20)

    # Add buttons for subjects
    math_button = create_button(root, "math name.png", "Math")
    physics_button = create_button(root, "physics name.png", "Physics")
    chemistry_button = create_button(root, "chemistry name.png", "Chemistry")

# Function to create the coming soon screen
def coming_soon_screen(subject):
    clear_widgets(root)

    coming_soon_label = tk.Label(root, text=f"Modules - {subject}\nComing Soon!", font=("Arial", 20, "bold"), bg="black", fg="white")
    coming_soon_label.pack(pady=20)

    try:
        img = Image.open("waiting.png")
        img = img.resize((250, 250), Image.LANCZOS)  # Adjust the size of the image
        photo_img = ImageTk.PhotoImage(img)

        img_label = tk.Label(root, image=photo_img, bg="black")
        img_label.image = photo_img
        img_label.pack(pady=20)
        img_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    except FileNotFoundError:
        print("Image not found")

    # Add a back button with an icon
    back_img = Image.open("back.png")  # Replace "back_icon.png" with your own icon path
    back_img = back_img.resize((30, 30), Image.LANCZOS)  # Adjust the size of the image
    back_icon = ImageTk.PhotoImage(back_img)

    back_button = tk.Button(root, image=back_icon, command=lambda: [clear_widgets(root), main_screen()], borderwidth=0)
    back_button.image = back_icon
    back_button.pack(pady=20)
    back_button.place(relx=0.8, rely=0.9, anchor=tk.CENTER)


# Function to create the modules screen
def modules_screen(subject):
    clear_widgets(root)

    module_label = tk.Label(root, text=f"Modules - {subject}", font=("Arial", 20, "bold"), bg="black", fg="white")
    module_label.pack(pady=20)

    # Add buttons for different modules
    trigonometry_button = create_button_mod(root, "trigo.png", "Trigonometry")
    logarithm_button = create_button_mod(root, "log.png", "Logarithm")
    differentiation_button = create_button_mod(root, "diff1.png", "Differentiation")
    integration_button = create_button_mod(root, "integ2.png", "Integration")

    # Add a back button with an icon
    back_img = Image.open("back.png")  # Replace "back_icon.png" with your own icon path
    back_img = back_img.resize((30, 30), Image.LANCZOS)  # Adjust the size of the image
    back_icon = ImageTk.PhotoImage(back_img)

    back_button = tk.Button(root, image=back_icon, command=lambda: [clear_widgets(root), main_screen()], borderwidth=0)
    back_button.image = back_icon
    back_button.pack(pady=20)
    back_button.place(relx=0.85, rely=0.95, anchor=tk.CENTER)

def clear_widgets(parent):
    for widget in parent.winfo_children():
        widget.destroy()

# Function to create a subject button with an image
def create_button(parent, image_path, subject):
    img = Image.open(image_path)
    img = img.resize((300, 150), Image.LANCZOS)  # Adjust the size of the image
    photo_img = ImageTk.PhotoImage(img)

    button = tk.Button(parent, image=photo_img, command=lambda p=subject: open_subject_screen(p), borderwidth=0)
    button.image = photo_img
    button.pack(pady=20)
    return button

# Function to create a subject button with an image
def create_button_mod(parent, image_path, subject):
    img = Image.open(image_path)
    img = img.resize((300, 100), Image.LANCZOS)  # Adjust the size of the image
    photo_img = ImageTk.PhotoImage(img)

    # Define the command for the trigonometry button
    if subject == "Trigonometry":
        trigonometry_command = lambda: display_pdf("Trigonometry.pdf")  # Assuming the PDF is in the same directory as your script
        button = tk.Button(parent, image=photo_img, command=trigonometry_command, borderwidth=0)
    elif subject == "Logarithm":
        logarithm_command = lambda: display_pdf("Logarithm.pdf")
        button = tk.Button(parent, image=photo_img, command=logarithm_command, borderwidth=0)
    elif subject == "Differentiation":
        differentiation_command = lambda: display_pdf("Differentiation.pdf")
        button = tk.Button(parent, image=photo_img, command=differentiation_command, borderwidth=0)
    elif subject == "Integration":
        differentiation_command = lambda: display_pdf("Integration.pdf")
        button = tk.Button(parent, image=photo_img, command=differentiation_command, borderwidth=0)
    else:
        button = tk.Button(parent, image=photo_img, command=lambda p=subject: open_subject_screen(p), borderwidth=0)

    button.image = photo_img
    button.pack(pady=20)
    return button

# Function to create a subject button with an image
def display_pdf(pdf_filename):
    # Create a Tkinter window to display the PDF
    window = tk.Toplevel()
    window.title(pdf_filename)  # Set the title of the window to the PDF filename
    window.geometry("350x690")  # Set the geometry to the desired size

    # Create a Canvas and Scrollbar
    canvas = tk.Canvas(window)
    scrollbar = tk.Scrollbar(window, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Load the PDF file and get the number of pages
    doc = fitz.open(pdf_filename)
    num_pages = doc.page_count

    # Iterate through each page and display the images
    for i in range(num_pages):
        page = doc.load_page(i)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        photo_img = ImageTk.PhotoImage(img)

        label = tk.Label(scrollable_frame, image=photo_img)
        label.image = photo_img  # To keep a reference
        label.pack()

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Center-align the window
    window.update_idletasks()  # Update the window to ensure correct alignment
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_coordinate = int((screen_width - window_width) / 2)
    y_coordinate = int((screen_height - window_height) / 2)
    window.geometry(f"550x690+{x_coordinate}+{y_coordinate}")  # Adjust the geometry accordingly

    window.mainloop()

# Call the launch screen function
launch_screen()
root.mainloop()

