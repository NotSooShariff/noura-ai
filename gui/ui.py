import customtkinter as ctk

def create_ui():
    # Function to be called when the button is clicked
    def on_button_click():
        if button.cget("text") == "🔴":
            button.configure(text="⬜")
            label.configure(text="Tap to stop recording")
        else:
            button.configure(text="🔴")
            label.configure(text="Click to start speaking")
        print("Mic button clicked!")

    # Create the main window
    app = ctk.CTk()
    app.geometry("300x300")
    app.title("Mic Button UI")

    # Add a label above the button
    label = ctk.CTkLabel(
        app, 
        text="Click to start speaking", 
        font=("Arial", 14)
    )
    label.pack(pady=20)

    # Define the button with the initial icon as a red circle
    button = ctk.CTkButton(
        app, 
        text="🔴", 
        width=150, 
        height=150, 
        corner_radius=75,  # Making the button circular
        font=("Arial", 80),
        command=on_button_click
    )

    # Center the button in the window
    button.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

    # Run the application
    app.mainloop()

create_ui()
