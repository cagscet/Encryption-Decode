from tkinter import *
from tkinter import messagebox
from cryptography.fernet import Fernet

# Master key oluşturma veya saklama
key = Fernet.generate_key()  # Gerçek projede bu key bir dosyaya veya güvenli bir yere kaydedilmelidir
cipher = Fernet(key)


def save_note():
    title = tit_entry.get()
    message = sec_entry.get("1.0", END).strip()
    master_scr = ms_scr_inp.get()

    if len(title) == 0 or len(message) == 0 or len(master_scr) == 0:
        messagebox.showerror(title="Error!", message="Please enter all info.")
    else:
        try:
            # Mesajı şifrele
            encrypted_message = cipher.encrypt(message.encode())

            # Verileri şifrelenmiş halde dosyaya kaydediyoruz
            with open("secret_note_encrypted.txt", "a") as file:
                file.write(f"Title: {title}\n")
                file.write(f"Encrypted Message: {encrypted_message.decode()}\n")
                file.write(f"Master Key: {master_scr}\n")
                file.write("-" * 30 + "\n")

            messagebox.showinfo(title="Success!", message="Note saved and encrypted successfully.")
        except Exception as e:
            messagebox.showerror(title="Error!", message=f"Failed to save note: {e}")


def decrypt_note():
    try:
        with open("secret_note_encrypted.txt", "r") as file:
            encrypted_message = file.readlines()[1].split(": ")[1].strip()
            decrypted_message = cipher.decrypt(encrypted_message.encode()).decode()
            messagebox.showinfo(title="Decrypted Message", message=decrypted_message)
    except Exception as e:
        messagebox.showerror(title="Error!", message=f"Failed to decrypt: {e}")


window = Tk()
window.title("Secret Note App")
window.config(padx=30, pady=30)

title_info_label = Label(text="Enter your title", font=("arial", 20))
title_info_label.config(padx=30, pady=15)
title_info_label.pack()

tit_entry = Entry(width=30)
tit_entry.pack()

inp_secret = Label(text="Enter your secret", font=("arial", 20))
inp_secret.config(padx=30, pady=15)
inp_secret.pack()

sec_entry = Text(width=30, height=10)
sec_entry.pack()

ms_label = Label(text="Enter master key", font=("arial", 20))
ms_label.config(padx=30, pady=15)
ms_label.pack()

ms_scr_inp = Entry(width=30)
ms_scr_inp.pack()

# Save & Encrypt butonu
save_button = Button(text="Save & Encrypt", command=save_note)
save_button.config(bg="black", fg="white")
save_button.pack()

# Decrypt butonu
dec_button = Button(text="Decrypt", command=decrypt_note)
dec_button.config(bg="black", fg="white")
dec_button.pack()

window.mainloop()
