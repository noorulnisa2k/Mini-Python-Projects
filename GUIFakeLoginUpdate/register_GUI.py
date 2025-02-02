import tkinter as tk
from tkinter import messagebox
import random
import time, os

# Function to handle registration
def register_user():
    first_name = entry_first_name.get()
    last_name = entry_last_name.get()
    email = entry_email.get()
    password = entry_password.get()
    
    if not first_name or not last_name or not email or not password:
        messagebox.showerror("Error", "All fields are required!")
        return

    # Simulate registration success with a random ID
    user_id = f"USER{random.randint(1000, 9999)}"
    messagebox.showinfo(
        "Registration Successful",
        f"Welcome, {first_name}! Play Game!"
    )
    
    # Close the registration window after showing the success message
    app.destroy()
    start_game()  # Wait for 2 seconds before running the next script
    # time.sleep(2)
    # app.destroy()

# Function to simulate starting the game
def start_game():
    # print("Game is starting...")  # Replace with your game script
    # You can call your game logic or another Python script here.
    # For example:
    print('another script')
    os.system('python Blackjack.py')

# Create the main application window
app = tk.Tk()
app.title("Register Here")
app.geometry("400x300")

# Add labels and entry fields
# Change the background color of the entire app
app.configure(bg="#f0f8ff")  # Light blue background

# Add labels and entry fields
tk.Label(app, text="First Name:", bg="#f0f8ff", fg="#000080").grid(row=0, column=0, pady=5, padx=10, sticky="e")
entry_first_name = tk.Entry(app, bg="#ffffff", fg="#000000")
entry_first_name.grid(row=0, column=1, pady=5, padx=10)

tk.Label(app, text="Last Name:", bg="#f0f8ff", fg="#000080").grid(row=1, column=0, pady=5, padx=10, sticky="e")
entry_last_name = tk.Entry(app, bg="#ffffff", fg="#000000")
entry_last_name.grid(row=1, column=1, pady=5, padx=10)

tk.Label(app, text="Email:", bg="#f0f8ff", fg="#000080").grid(row=2, column=0, pady=5, padx=10, sticky="e")
entry_email = tk.Entry(app, bg="#ffffff", fg="#000000")
entry_email.grid(row=2, column=1, pady=5, padx=10)

tk.Label(app, text="Password:", bg="#f0f8ff", fg="#000080").grid(row=3, column=0, pady=5, padx=10, sticky="e")
entry_password = tk.Entry(app, show="*", bg="#ffffff", fg="#000000")
entry_password.grid(row=3, column=1, pady=5, padx=10)

# Add Register button with custom colors
btn_register = tk.Button(app, text="Register", command=register_user, bg="#4682b4", fg="#ffffff", activebackground="#5f9ea0", activeforeground="#ffffff")
btn_register.grid(row=4, column=0, columnspan=2, pady=20)


# Run the application
app.mainloop()
