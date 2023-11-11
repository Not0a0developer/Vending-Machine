import tkinter as tk
from tkinter import messagebox
import cv2
from pyzbar.pyzbar import decode
from PIL import Image, ImageTk

# Shop items and their regular prices in KRW
shop_items = {
    "Water": {"price": 1000, "image_path": "water.png"},
    "Soda": {"price": 1500, "image_path": "soda.png"},
    "Chips": {"price": 2000, "image_path": "chips.png"},
    "Chocolate": {"price": 2500, "image_path": "chocolate.png"},
}

# Sale discount (20% off)
sale_discount = 0.2

# Initial balance in KRW
user_balance = 0
qr_code_scanned = False  # To track whether a QR code has been scanned

def scan_qr_code():
    global user_balance, qr_code_scanned
    if qr_code_scanned:
        messagebox.showinfo("QR Code Scanned", "You have already scanned a QR code.")
        return

    cap = cv2.VideoCapture(0)  # Open the default camera (0 or -1)
    while not qr_code_scanned:
        ret, frame = cap.read()  # Read a frame
        decoded_objects = decode(frame)
        for obj in decoded_objects:
            qr_code_text = obj.data.decode('utf-8')
            if qr_code_text == "sale":
                apply_sale_discount()  # Apply the sale discount
                continue
            try:
                qr_code_amount = int(qr_code_text)
                user_balance += qr_code_amount
                messagebox.showinfo("QR Code Scanned", f"Added {qr_code_amount} KRW to your balance.")
                qr_code_scanned = True  # Mark that a QR code has been scanned
            except ValueError:
                messagebox.showerror("Invalid QR Code", "The QR code content is not a valid integer.")
            break  # Stop processing frames after the first QR code is detected
        if user_balance > 0:
            break
        if ret:
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            camera_label.imgtk = imgtk
            camera_label.configure(image=imgtk)
            root.update()
    cap.release()  # Release the camera
    balance_label.config(text=f"Your Balance: {user_balance} KRW")

def apply_sale_discount():
    global sale_discount
    sale_discount = 0.30  # Set the sale discount to 30% (0.30)
    for item_name, item_info in shop_items.items():
        item_info["price"] = item_info["price"] * sale_discount  # Apply the sale discount
    messagebox.showinfo("Sale Applied", "A 30% sale discount has been applied to all items.")
        


def purchase_item(item_name, item_price):
    global user_balance, qr_code_scanned
    if user_balance >= item_price:
        user_balance -= item_price
        messagebox.showinfo("Purchase Successful", f"Purchased {item_name} for {item_price} KRW.")
        qr_code_scanned = False  # Reset the QR code scanned flag
    else:
        messagebox.showerror("Insufficient Balance", "You don't have enough balance to purchase this item.")
    balance_label.config(text=f"Your Balance: {user_balance} KRW")

# Create the main window
root = tk.Tk()
root.title("QR Code Balance Simulation")

# Create widgets
title_label = tk.Label(root, text="QR Code Balance Simulation", font=("Helvetica", 16))
title_label.pack(pady=10)

scan_button = tk.Button(root, text="Scan QR Code", command=scan_qr_code)
scan_button.pack(pady=10)

balance_label = tk.Label(root, text=f"Your Balance: {user_balance} KRW", font=("Helvetica", 12))
balance_label.pack()

item_frame = tk.Frame(root)
item_frame.pack(pady=10)

for item_name, item_info in shop_items.items():
    item_image = Image.open(item_info['image_path'])
    item_image.thumbnail((64, 64), Image.BICUBIC)  # Adjust the image size
    item_icon = ImageTk.PhotoImage(item_image)

    item_label = tk.Label(item_frame, image=item_icon, text=f"{item_name}\n{item_info['price']} KRW", compound=tk.TOP)
    item_label.image = item_icon
    item_label.bind("<Button-1>", lambda event, name=item_name, price=item_info['price']: purchase_item(name, price))
    item_label.grid(row=0, column=list(shop_items.keys()).index(item_name), padx=5)

camera_frame = tk.Frame(root)
camera_frame.pack(pady=10)
camera_label = tk.Label(camera_frame)
camera_label.pack()

exit_button = tk.Button(root, text="Exit", command=root.destroy)
exit_button.pack(pady=10)

# Start the GUI application
root.mainloop()
