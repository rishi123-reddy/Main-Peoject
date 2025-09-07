import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import random
import string
from cryptography.fernet import Fernet
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from config import Config
class SteganographyApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Secure Image Steganography")
        self.root.geometry("1000x700")
        self.root.configure(bg="#1e1e1e")
        
        # Load application images
        self.load_application_images()
        
        # Initialize variables
        self.current_image = None
        self.setup_styles()
        self.create_main_interface()
        
    def load_application_images(self):
        try:
            # Load hide icon
            self.hide_image = Image.open("hide.png")
            self.hide_image = self.hide_image.resize((80, 80), Image.Resampling.LANCZOS)
            self.hide_photo = ImageTk.PhotoImage(self.hide_image)
            
            # Load lock image
            self.lock_image = Image.open("lock_image.png")
            self.lock_image = self.lock_image.resize((450, 450), Image.Resampling.LANCZOS)
            self.lock_photo = ImageTk.PhotoImage(self.lock_image)
        except Exception as e:
            print(f"Error loading images: {e}")
            self.hide_photo = None
            self.lock_photo = None
        
    def setup_styles(self):
        # Configure styles for ttk widgets
        style = ttk.Style()
        style.configure("Custom.TButton",
                       padding=10,
                       font=("Helvetica", 12),
                       background="#007bff",
                       foreground="white")
        
        style.configure("Title.TLabel",
                       font=("Helvetica", 24, "bold"),
                       background="#1e1e1e",
                       foreground="white")
        
        style.configure("Subtitle.TLabel",
                       font=("Helvetica", 12),
                       background="#1e1e1e",
                       foreground="#888888")

    def create_main_interface(self):
        # Main container with two panels
        self.main_container = tk.Frame(self.root, bg="#1e1e1e")
        self.main_container.pack(expand=True, fill="both", padx=20, pady=20)

        # Left panel for image preview
        self.left_panel = tk.Frame(self.main_container, bg="#2d2d2d", width=500)
        self.left_panel.pack(side=tk.LEFT, fill="both", padx=(0, 10))
        
        # Title and logo frame
        title_frame = tk.Frame(self.left_panel, bg="#2d2d2d")
        title_frame.pack(pady=10)
        
        # Add hide icon if available
        if self.hide_photo:
            logo_label = tk.Label(title_frame, 
                                image=self.hide_photo, 
                                bg="#2d2d2d")
            logo_label.pack(side=tk.LEFT, padx=10)
        
        # Title for preview section
        tk.Label(title_frame,
                text="Image Preview",
                font=("Helvetica", 18, "bold"),
                bg="#2d2d2d",
                fg="white").pack(side=tk.LEFT, padx=10)
        
        # Image preview area
        self.preview_frame = tk.Frame(self.left_panel, bg="#2d2d2d")
        self.preview_frame.pack(pady=20)
        
        # Default preview image
        self.display_default_preview()

        # Right panel for controls
        self.right_panel = tk.Frame(self.main_container, bg="#1e1e1e")
        self.right_panel.pack(side=tk.LEFT, fill="both", expand=True)

        # Application title and description
        title_frame = tk.Frame(self.right_panel, bg="#1e1e1e")
        title_frame.pack(pady=(0, 30))
        
        tk.Label(title_frame,
                text="Image Steganography",
                font=("Helvetica", 24, "bold"),
                bg="#1e1e1e",
                fg="white").pack()
        
        tk.Label(title_frame,
                text="Hide Secret Messages in Images",
                font=("Helvetica", 14),
                bg="#1e1e1e",
                fg="#888888").pack(pady=(5, 0))

        # Control buttons
        self.create_control_buttons()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = tk.Label(self.root,
                                 textvariable=self.status_var,
                                 bd=1,
                                 relief=tk.SUNKEN,
                                 anchor=tk.W,
                                 bg="#252525",
                                 fg="#888888",
                                 padx=10,
                                 pady=5)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def create_control_buttons(self):
        buttons_frame = tk.Frame(self.right_panel, bg="#1e1e1e")
        buttons_frame.pack(pady=20)

        button_configs = [
            ("Hide Message", self.encode_image, "#2196F3", "Encrypt and hide a message in an image"),
            ("Extract Message", self.decode_image, "#4CAF50", "Extract hidden message from an image"),
            ("Clear Preview", self.clear_preview, "#f44336", "Clear the current image preview")
        ]

        for text, command, color, tooltip in button_configs:
            btn_frame = tk.Frame(buttons_frame, bg="#1e1e1e")
            btn_frame.pack(pady=10)
            
            btn = tk.Button(btn_frame,
                          text=text,
                          command=command,
                          font=("Helvetica", 12, "bold"),
                          bg=color,
                          fg="white",
                          relief=tk.FLAT,
                          width=25,
                          height=2,
                          cursor="hand2")
            btn.pack()
            
            # Tooltip label
            tk.Label(btn_frame,
                    text=tooltip,
                    font=("Helvetica", 10),
                    bg="#1e1e1e",
                    fg="#888888").pack(pady=(5, 0))
            
            # Hover effects
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=self.adjust_color(b.cget("bg"), 1.1)))
            btn.bind("<Leave>", lambda e, b=btn, c=color: b.configure(bg=c))

    def display_default_preview(self):
        # Create a default preview canvas with lock image
        self.preview_canvas = tk.Canvas(self.preview_frame,
                                      width=450,
                                      height=450,
                                      bg="#2d2d2d",
                                      highlightthickness=1,
                                      highlightbackground="#404040")
        self.preview_canvas.pack()
        
        if self.lock_photo:
            # If we have a lock image, display it
            self.preview_canvas.create_image(225, 225, image=self.lock_photo)
        
        # Draw placeholder text
        self.preview_canvas.create_text(225,
                                      350,
                                      text="No Image Selected",
                                      fill="#ffffff",
                                      font=("Helvetica", 16, "bold"))
        self.preview_canvas.create_text(225,
                                      380,
                                      text="Click 'Hide Message' or 'Extract Message' to begin",
                                      fill="#cccccc",
                                      font=("Helvetica", 12))
    def adjust_color(self, color, factor):
        # Convert color to RGB values and adjust brightness
        r = int(min(255, int(color[1:3], 16) * factor))
        g = int(min(255, int(color[3:5], 16) * factor))
        b = int(min(255, int(color[5:7], 16) * factor))
        return f"#{r:02x}{g:02x}{b:02x}"

    def update_preview(self, image_path):
        try:
            image = Image.open(image_path)
            # Store the current image
            self.current_image = image
            
            # Calculate aspect ratio
            aspect_ratio = image.width / image.height
            
            # Determine new dimensions while maintaining aspect ratio
            if aspect_ratio > 1:
                new_width = 450
                new_height = int(450 / aspect_ratio)
            else:
                new_height = 450
                new_width = int(450 * aspect_ratio)
            
            # Resize image
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            
            # Update canvas
            self.preview_canvas.delete("all")
            self.preview_canvas.create_image(225,
                                          225,
                                          image=photo,
                                          anchor=tk.CENTER)
            self.preview_canvas.image = photo
            
            # Update status
            self.status_var.set(f"Image loaded: {os.path.basename(image_path)}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {str(e)}")
            self.status_var.set("Error loading image")

    def clear_preview(self):
        self.current_image = None
        self.preview_canvas.delete("all")
        self.display_default_preview()
        self.status_var.set("Preview cleared")

    def create_popup(self, title, message, fields=None):
        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.geometry("400x300")
        popup.configure(bg="#1e1e1e")
        popup.transient(self.root)
        popup.grab_set()
        
        # Center popup on screen
        popup.geometry(f"+{self.root.winfo_x() + 250}+{self.root.winfo_y() + 200}")

        # Add hide icon to popup
        if self.hide_photo:
            tk.Label(popup,
                    image=self.hide_photo,
                    bg="#1e1e1e").pack(pady=(10, 0))

        tk.Label(popup,
                text=message,
                bg="#1e1e1e",
                fg="white",
                font=("Helvetica", 12)).pack(pady=20)

        entries = {}
        if fields:
            for field in fields:
                frame = tk.Frame(popup, bg="#1e1e1e")
                frame.pack(pady=5)
                tk.Label(frame,
                        text=f"{field}:",
                        bg="#1e1e1e",
                        fg="white").pack(side=tk.LEFT, padx=5)
                entry = tk.Entry(frame, width=30)
                entry.pack(side=tk.LEFT, padx=5)
                entries[field] = entry

        button_frame = tk.Frame(popup, bg="#1e1e1e")
        button_frame.pack(pady=20)

        def on_submit():
            popup.result = {k: v.get() for k, v in entries.items()} if fields else True
            popup.destroy()

        def on_cancel():
            popup.result = None
            popup.destroy()

        tk.Button(button_frame,
                 text="Submit",
                 command=on_submit,
                 bg="#2196F3",
                 fg="white",
                 font=("Helvetica", 10)).pack(side=tk.LEFT, padx=5)

        tk.Button(button_frame,
                 text="Cancel",
                 command=on_cancel,
                 bg="#f44336",
                 fg="white",
                 font=("Helvetica", 10)).pack(side=tk.LEFT, padx=5)

        popup.wait_window()
        return getattr(popup, 'result', None)

 
    def encode_image(self):
        try:
            # Select image
            img_path = filedialog.askopenfilename(
                title="Select Image",
                filetypes=(("PNG files", "*.png"),
                          ("JPEG files", "*.jpg;*.jpeg"),
                          ("All files", "*.*"))
            )
            
            if not img_path:
                return
    
            self.update_preview(img_path)
            self.status_var.set("Image loaded successfully")
    
            # Get message to hide
            text_input = self.create_popup(
                "Hide Message",
                "Enter the message to hide:",
                ["Message"]
            )
    
            if not text_input or not text_input["Message"]:
                return
    
            # Process image
            image = Image.open(img_path)
            newimg = image.copy()
            
            # Encrypt message
            key = Fernet.generate_key()
            cipher_suite = Fernet(key)
            encrypted_text = cipher_suite.encrypt(text_input["Message"].encode())
            
            # Generate OTP
            otp = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            
            # Encode the encrypted message
            self.encode_enc(newimg, encrypted_text)
            
            # Create default encrypted filename
            original_filename = os.path.splitext(os.path.basename(img_path))[0]
            default_save_name = f"{original_filename}_encrypted.png"
            
            # Save the new image with default name
            save_path = filedialog.asksaveasfilename(
                initialfile=default_save_name,
                defaultextension=".png",
                filetypes=(("PNG files", "*.png"), ("All files", "*.*"))
            )
            
            if save_path:
                newimg.save(save_path)
                self.update_preview(save_path)
                
                # Get email for sending key
                email_input = self.create_popup(
                    "Email Address",
                    "Enter email to receive decryption key:",
                    ["Email"]
                )
                
                if email_input and email_input["Email"]:
                    self.send_email(email_input["Email"], key.decode(), otp)
                    messagebox.showinfo("Success", 
                                      "Image saved and decryption key sent!")
                    self.status_var.set("Operation completed successfully")
                
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status_var.set("Error occurred during encoding")
    

    def decode_image(self):
        try:
            # Select image
            img_path = filedialog.askopenfilename(
                title="Select Image",
                filetypes=(("PNG files", "*.png"),
                          ("All files", "*.*"))
            )
            
            if not img_path:
                return

            self.update_preview(img_path)
            
            # Get decryption key and OTP
            key_input = self.create_popup(
                "Decryption",
                "Enter decryption key and OTP:",
                ["Key", "OTP"]
            )
            
            if not key_input:
                return

            # Decrypt and show message
            image = Image.open(img_path)
            encrypted_text = self.decode_enc(image)
            
            try:
                cipher_suite = Fernet(key_input["Key"].encode())
                decrypted_text = cipher_suite.decrypt(encrypted_text).decode()
                
                result_popup = tk.Toplevel(self.root)
                result_popup.title("Decoded Message")
                result_popup.geometry("400x300")
                result_popup.configure(bg="#1e1e1e")
                
                # Add hide icon to result popup
                if self.hide_photo:
                    tk.Label(result_popup,
                            image=self.hide_photo,
                            bg="#1e1e1e").pack(pady=(10, 0))
                
                text_widget = tk.Text(result_popup, 
                                    wrap=tk.WORD,
                                    width=40,
                                    height=10,
                                    bg="#2d2d2d",
                                    fg="white")
                text_widget.pack(padx=20, pady=20)
                text_widget.insert(tk.END, decrypted_text)
                text_widget.configure(state='disabled')
                
                self.status_var.set("Message decoded successfully")
                
            except Exception as e:
                messagebox.showerror("Error", "Invalid key or corrupted message")
                self.status_var.set("Decoding failed")
                
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status_var.set("Error occurred during decoding")

    def encode_enc(self, image, message):
        width, height = image.size
        pixels = image.load()
        
        # Convert message to binary
        binary_message = ''.join(format(byte, '08b') for byte in message)
        message_length = len(binary_message)
        
        if message_length > width * height * 3:
            raise ValueError("Message too large for image")
        
        # Add terminator to binary message
        binary_message += '1111111111111110'
        
        idx = 0
        for row in range(height):
            for col in range(width):
                if idx < len(binary_message):
                    pixel = list(pixels[col, row])
                    
                    # Modify least significant bits
                    for color_channel in range(3):
                        if idx < len(binary_message):
                            pixel[color_channel] = pixel[color_channel] & ~1 | int(binary_message[idx])
                            idx += 1
                    
                    pixels[col, row] = tuple(pixel)
                else:
                    break

    def decode_enc(self, image):
        width, height = image.size
        pixels = image.load()
        binary_message = []
        
        for row in range(height):
            for col in range(width):
                pixel = pixels[col, row]
                
                for color_channel in range(3):
                    binary_message.append(str(pixel[color_channel] & 1))
                
                if len(binary_message) >= 16:
                    if ''.join(binary_message[-16:]) == '1111111111111110':
                        binary_message = binary_message[:-16]
                        
                        message_bytes = bytearray()
                        for i in range(0, len(binary_message), 8):
                            byte = binary_message[i:i+8]
                            if len(byte) == 8:
                                message_bytes.append(int(''.join(byte), 2))
                        
                        return bytes(message_bytes)
        
        raise ValueError("No hidden message found")

    def send_email(self, recipient_email, key, otp):
        # Email configuration
        sender_email = Config.SENDER_EMAIL
        sender_password = Config.SENDER_PASSWORD
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        
        # Create message
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = recipient_email
        message["Subject"] = "Steganography Decryption Key"
        
        body = f"""
        Hello,
        
        Here is your decryption key and OTP for the steganography image:
        
        Decryption Key: {key}
        OTP: {otp}
        
        Please keep this information secure and do not share it with anyone.
        
        Best regards,
        Image Steganography App
        """
        
        message.attach(MIMEText(body, "plain"))
        
        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
            server.quit()
            
        except Exception as e:
            raise Exception(f"Failed to send email: {str(e)}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = SteganographyApp()
    app.run()
