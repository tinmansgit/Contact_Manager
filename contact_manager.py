# Contact Manager v1.0 20250414.07:37
import os
import json
import tkinter as tk
from tkinter import messagebox, simpledialog, Toplevel, scrolledtext
import contact_manager_logger
from contact_manager_logger import log_error, log_debug

contacts_file = "/bin/Python/Contact_Manager/my_contacts.json"
id_counter = 0
contacts = []

BG_COLOR = "black"
FG_COLOR = "white"
ENTRY_BG = "black"
ENTRY_FG = "white"

def load_contacts():
    global id_counter, contacts
    if not os.path.exists(contacts_file):
        log_debug(f"Contacts file not found. Initializing new contacts list at {contacts_file}.")
        contacts = []
        id_counter = 0
        return contacts
    try:
        with open(contacts_file, 'r') as f:
            contacts = json.load(f)
        log_debug("Contacts loaded successfully from the file.")
    except Exception as e:
        log_error(f"Error loading contacts: {e}")
        contacts = []
        id_counter = 0
        return contacts

    if contacts:
        try:
            id_counter = max(int(contact["id"]) for contact in contacts) + 1
        except Exception as e:
            log_error(f"Error computing id_counter: {e}")
            id_counter = 0
    else:
        id_counter = 0
    log_debug(f"Initial id_counter set to {id_counter}.")
    return contacts

def save_contacts():
    try:
        with open(contacts_file, 'w') as f:
            json.dump(contacts, f, indent=4)
        log_debug("Contacts saved successfully.")
    except Exception as e:
        log_error(f"Error saving contacts: {e}")

class ContactsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Contact Manager")
        try:
            icon = tk.PhotoImage(file="/bin/Python/Contact_Manager/contact_manager_icon.png")
            self.iconphoto(False, icon)
        except Exception as e:
            log_error(f"Failed to load icon: {e}")
        self.configure(bg=BG_COLOR)
        self.geometry("600x400")
        log_debug("ContactsApp initialized and GUI set up.")
        self.create_widgets()
    
    def create_widgets(self):
        header = tk.Label(self, text="Contacts Manager", bg=BG_COLOR, fg=FG_COLOR, font=("Helvetica", 16))
        header.pack(pady=10)
        
        btn_frame = tk.Frame(self, bg=BG_COLOR)
        btn_frame.pack(pady=20)
        
        btn_list = tk.Button(btn_frame, text="List all contacts", command=self.list_contacts, bg=BG_COLOR, fg=FG_COLOR, width=20)
        btn_list.grid(row=0, column=0, padx=5, pady=5)
        
        btn_add = tk.Button(btn_frame, text="Add new contact", command=self.add_contact_window, bg=BG_COLOR, fg=FG_COLOR, width=20)
        btn_add.grid(row=0, column=1, padx=5, pady=5)
        
        btn_edit = tk.Button(btn_frame, text="Edit a contact", command=self.edit_contact_window, bg=BG_COLOR, fg=FG_COLOR, width=20)
        btn_edit.grid(row=1, column=0, padx=5, pady=5)
        
        btn_search = tk.Button(btn_frame, text="Search for a contact", command=self.search_contact_window, bg=BG_COLOR, fg=FG_COLOR, width=20)
        btn_search.grid(row=1, column=1, padx=5, pady=5)
        
        btn_delete = tk.Button(btn_frame, text="Delete a contact", command=self.delete_contact_window, bg=BG_COLOR, fg=FG_COLOR, width=20)
        btn_delete.grid(row=2, column=0, padx=5, pady=5)
        
        btn_exit = tk.Button(btn_frame, text="Exit", command=self.quit, bg=BG_COLOR, fg=FG_COLOR, width=20)
        btn_exit.grid(row=2, column=1, padx=5, pady=5)
    
    def list_contacts(self):
        log_debug("Listing all contacts.")
        win = Toplevel(self)
        win.title("All Contacts")
        win.configure(bg=BG_COLOR)
        win.geometry("500x400")
        header = tk.Label(win, text="Contacts List", bg=BG_COLOR, fg=FG_COLOR, font=("Helvetica", 14))
        header.pack(pady=5)
        
        text_area = scrolledtext.ScrolledText(win, bg=BG_COLOR, fg=FG_COLOR, width=60, height=20)
        text_area.pack(padx=10, pady=10)
        if not contacts:
            message = "No contacts available."
            text_area.insert(tk.END, message)
            log_debug("No contacts available to list.")
        else:
            for contact in contacts:
                contact_info = f"{contact['id']}\t{contact['name']}\t{contact['email']}\t{contact['phone']}\n"
                text_area.insert(tk.END, contact_info)
        text_area.config(state=tk.DISABLED)
    
    def add_contact_window(self):
        log_debug("Opening window to add a new contact.")
        win = Toplevel(self)
        win.title("Add New Contact")
        win.configure(bg=BG_COLOR)
        tk.Label(win, text="Name:", bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=0, padx=10, pady=10)
        name_entry = tk.Entry(win, bg=ENTRY_BG, fg=ENTRY_FG)
        name_entry.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(win, text="Email:", bg=BG_COLOR, fg=FG_COLOR).grid(row=1, column=0, padx=10, pady=10)
        email_entry = tk.Entry(win, bg=ENTRY_BG, fg=ENTRY_FG)
        email_entry.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(win, text="Phone:", bg=BG_COLOR, fg=FG_COLOR).grid(row=2, column=0, padx=10, pady=10)
        phone_entry = tk.Entry(win, bg=ENTRY_BG, fg=ENTRY_FG)
        phone_entry.grid(row=2, column=1, padx=10, pady=10)
        
        def add_contact_action():
            global id_counter
            name = name_entry.get()
            email = email_entry.get()
            phone = phone_entry.get()
            if not name or not email or not phone:
                error_msg = "All fields are required to add a new contact."
                log_error(error_msg)
                messagebox.showerror("Error", error_msg, parent=win)
                return
            new_contact = {"id": str(id_counter), "name": name, "email": email, "phone": phone}
            contacts.append(new_contact)
            log_debug(f"Added new contact: {new_contact}")
            id_counter += 1
            save_contacts()
            messagebox.showinfo("Success", f"Contact added with ID {new_contact['id']}", parent=win)
            win.destroy()
        
        tk.Button(win, text="Add Contact", command=add_contact_action, bg=BG_COLOR, fg=FG_COLOR).grid(row=3, column=0, columnspan=2, pady=10)
    
    def edit_contact_window(self):
        log_debug("Opening window to edit contact.")
        win = Toplevel(self)
        win.title("Edit Contact")
        win.configure(bg=BG_COLOR)
        tk.Label(win, text="Enter Contact ID:", bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=0, padx=10, pady=10)
        id_entry = tk.Entry(win, bg=ENTRY_BG, fg=ENTRY_FG)
        id_entry.grid(row=0, column=1, padx=10, pady=10)
        
        def load_contact_for_edit():
            contact_id = id_entry.get()
            for contact in contacts:
                if contact["id"] == contact_id:
                    name_var.set(contact["name"])
                    email_var.set(contact["email"])
                    phone_var.set(contact["phone"])
                    log_debug(f"Loaded contact {contact_id} for editing.")
                    return
            error_msg = f"Contact with ID {contact_id} not found for editing."
            log_error(error_msg)
            messagebox.showerror("Error", error_msg, parent=win)
        
        tk.Button(win, text="Load Contact", command=load_contact_for_edit, bg=BG_COLOR, fg=FG_COLOR).grid(row=1, column=0, columnspan=2, pady=5)
        
        name_var = tk.StringVar()
        email_var = tk.StringVar()
        phone_var = tk.StringVar()
        
        tk.Label(win, text="Name:", bg=BG_COLOR, fg=FG_COLOR).grid(row=2, column=0, padx=10, pady=5)
        name_entry = tk.Entry(win, textvariable=name_var, bg=ENTRY_BG, fg=ENTRY_FG)
        name_entry.grid(row=2, column=1, padx=10, pady=5)
        
        tk.Label(win, text="Email:", bg=BG_COLOR, fg=FG_COLOR).grid(row=3, column=0, padx=10, pady=5)
        email_entry = tk.Entry(win, textvariable=email_var, bg=ENTRY_BG, fg=ENTRY_FG)
        email_entry.grid(row=3, column=1, padx=10, pady=5)
        
        tk.Label(win, text="Phone:", bg=BG_COLOR, fg=FG_COLOR).grid(row=4, column=0, padx=10, pady=5)
        phone_entry = tk.Entry(win, textvariable=phone_var, bg=ENTRY_BG, fg=ENTRY_FG)
        phone_entry.grid(row=4, column=1, padx=10, pady=5)
        
        def edit_contact_action():
            contact_id = id_entry.get()
            for contact in contacts:
                if contact["id"] == contact_id:
                    new_name = name_entry.get() or contact["name"]
                    new_email = email_entry.get() or contact["email"]
                    new_phone = phone_entry.get() or contact["phone"]
                    old_contact = contact.copy()
                    contact.update({"name": new_name, "email": new_email, "phone": new_phone})
                    log_debug(f"Contact {contact_id} updated from {old_contact} to {contact}.")
                    save_contacts()
                    messagebox.showinfo("Success", f"Contact edited with ID {contact_id}", parent=win)
                    win.destroy()
                    return
            error_msg = f"Contact with ID {contact_id} not found for editing."
            log_error(error_msg)
            messagebox.showerror("Error", error_msg, parent=win)
        
        tk.Button(win, text="Save Changes", command=edit_contact_action, bg=BG_COLOR, fg=FG_COLOR).grid(row=5, column=0, columnspan=2, pady=10)
    
    def search_contact_window(self):
        log_debug("Opening window to search for a contact.")
        win = Toplevel(self)
        win.title("Search Contact")
        win.configure(bg=BG_COLOR)
        tk.Label(win, text="Enter Name to search:", bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=0, padx=10, pady=10)
        search_entry = tk.Entry(win, bg=ENTRY_BG, fg=ENTRY_FG)
        search_entry.grid(row=0, column=1, padx=10, pady=10)
        
        text_area = scrolledtext.ScrolledText(win, bg=BG_COLOR, fg=FG_COLOR, width=50, height=10)
        text_area.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        
        def search_action():
            query = search_entry.get().lower()
            text_area.config(state=tk.NORMAL)
            text_area.delete("1.0", tk.END)
            matches = [contact for contact in contacts if query in contact["name"].lower()]
            if not matches:
                no_results = "No matching contacts found."
                text_area.insert(tk.END, no_results)
                log_debug(f"Search for '{query}' returned no results.")
            else:
                for match in matches:
                    info = f"ID: {match['id']}, Name: {match['name']}, Email: {match['email']}, Phone: {match['phone']}\n"
                    text_area.insert(tk.END, info)
                log_debug(f"Search for '{query}' returned {len(matches)} result(s).")
            text_area.config(state=tk.DISABLED)
        
        tk.Button(win, text="Search", command=search_action, bg=BG_COLOR, fg=FG_COLOR).grid(row=1, column=0, columnspan=2, pady=5)
    
    def delete_contact_window(self):
        log_debug("Opening window to delete a contact.")
        win = Toplevel(self)
        win.title("Delete Contact")
        win.configure(bg=BG_COLOR)
        tk.Label(win, text="Enter Contact ID to delete:", bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=0, padx=10, pady=10)
        id_entry = tk.Entry(win, bg=ENTRY_BG, fg=ENTRY_FG)
        id_entry.grid(row=0, column=1, padx=10, pady=10)
        
        def delete_action():
            contact_id = id_entry.get()
            for i, contact in enumerate(contacts):
                if contact["id"] == contact_id:
                    log_debug(f"Deleting contact: {contact}")
                    del contacts[i]
                    save_contacts()
                    messagebox.showinfo("Success", f"Contact deleted with ID {contact_id}", parent=win)
                    win.destroy()
                    return
            error_msg = f"Contact with ID {contact_id} not found for deletion."
            log_error(error_msg)
            messagebox.showerror("Error", error_msg, parent=win)
        
        tk.Button(win, text="Delete Contact", command=delete_action, bg=BG_COLOR, fg=FG_COLOR).grid(row=1, column=0, columnspan=2, pady=10)

if __name__ == "__main__":
    load_contacts()
    log_debug("Starting ContactsApp...")
    app = ContactsApp()
    try:
        app.mainloop()
    except Exception as e:
        log_error(f"An error occurred in the mainloop: {e}")
