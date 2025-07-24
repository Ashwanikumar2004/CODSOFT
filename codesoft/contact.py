import tkinter as tk
from tkinter import messagebox, simpledialog

class ContactManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Manager")
        self.contacts = []  # List of dicts with keys: name, phone, email, address
        self.selected_index = None

        self.create_widgets()
        self.refresh_contact_list()

    def create_widgets(self):
        # Frame for contact form
        form_frame = tk.Frame(self.root)
        form_frame.pack(padx=10, pady=10, fill=tk.X)

        # Store Name
        tk.Label(form_frame, text="Store Name:").grid(row=0, column=0, sticky='e')
        self.entry_name = tk.Entry(form_frame)
        self.entry_name.grid(row=0, column=1, sticky='ew')

        # Phone Number
        tk.Label(form_frame, text="Phone Number:").grid(row=1, column=0, sticky='e')
        self.entry_phone = tk.Entry(form_frame)
        self.entry_phone.grid(row=1, column=1, sticky='ew')

        # Email
        tk.Label(form_frame, text="Email:").grid(row=2, column=0, sticky='e')
        self.entry_email = tk.Entry(form_frame)
        self.entry_email.grid(row=2, column=1, sticky='ew')

        # Address
        tk.Label(form_frame, text="Address:").grid(row=3, column=0, sticky='e')
        self.entry_address = tk.Entry(form_frame)
        self.entry_address.grid(row=3, column=1, sticky='ew')

        form_frame.columnconfigure(1, weight=1)

        # Buttons frame
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(padx=10, pady=5, fill=tk.X)

        self.btn_add_update = tk.Button(btn_frame, text="Add Contact", command=self.add_or_update_contact)
        self.btn_add_update.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        self.btn_delete = tk.Button(btn_frame, text="Delete Contact", command=self.delete_contact)
        self.btn_delete.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        # Search frame
        search_frame = tk.Frame(self.root)
        search_frame.pack(padx=10, pady=5, fill=tk.X)

        tk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.entry_search = tk.Entry(search_frame)
        self.entry_search.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.entry_search.bind("<KeyRelease>", lambda e: self.search_contacts())

        # Contact listbox with scrollbar
        list_frame = tk.Frame(self.root)
        list_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox_contacts = tk.Listbox(list_frame, yscrollcommand=scrollbar.set)
        self.listbox_contacts.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.listbox_contacts.bind("<<ListboxSelect>>", self.on_contact_select)

        scrollbar.config(command=self.listbox_contacts.yview)

    def add_or_update_contact(self):
        name = self.entry_name.get().strip()
        phone = self.entry_phone.get().strip()
        email = self.entry_email.get().strip()
        address = self.entry_address.get().strip()

        if not name or not phone:
            messagebox.showwarning("Input Error", "Please enter at least the Store Name and Phone Number.")
            return

        if self.selected_index is None:
            # Add new contact
            self.contacts.append({
                "name": name,
                "phone": phone,
                "email": email,
                "address": address
            })
            messagebox.showinfo("Success", "Contact added successfully.")
        else:
            # Update existing contact
            self.contacts[self.selected_index] = {
                "name": name,
                "phone": phone,
                "email": email,
                "address": address
            }
            messagebox.showinfo("Success", "Contact updated successfully.")
            self.selected_index = None
            self.btn_add_update.config(text="Add Contact")

        self.clear_form()
        self.refresh_contact_list()

    def delete_contact(self):
        if self.selected_index is None:
            messagebox.showwarning("No selection", "Please select a contact to delete.")
            return

        contact = self.contacts[self.selected_index]
        confirm = messagebox.askyesno("Confirm Delete", f"Delete contact '{contact['name']}'?")
        if confirm:
            del self.contacts[self.selected_index]
            self.selected_index = None
            self.btn_add_update.config(text="Add Contact")
            self.clear_form()
            self.refresh_contact_list()

    def search_contacts(self):
        query = self.entry_search.get().strip().lower()
        self.listbox_contacts.delete(0, tk.END)
        for i, contact in enumerate(self.contacts):
            if (query in contact['name'].lower()) or (query in contact['phone']):
                self.listbox_contacts.insert(tk.END, f"{contact['name']} - {contact['phone']}")

    def refresh_contact_list(self):
        self.listbox_contacts.delete(0, tk.END)
        for contact in self.contacts:
            self.listbox_contacts.insert(tk.END, f"{contact['name']} - {contact['phone']}")

    def on_contact_select(self, event):
        if not self.listbox_contacts.curselection():
            return
        idx = self.listbox_contacts.curselection()[0]

        # When searching, the index of the listbox is filtered, so we have to map back
        query = self.entry_search.get().strip().lower()
        if query:
            # Find the actual index in self.contacts
            filtered_contacts = [c for c in self.contacts if (query in c['name'].lower()) or (query in c['phone'])]
            contact = filtered_contacts[idx]
            # Find contact real index in contacts list
            real_index = self.contacts.index(contact)
        else:
            real_index = idx
            contact = self.contacts[real_index]

        self.selected_index = real_index
        self.fill_form(contact)
        self.btn_add_update.config(text="Update Contact")

    def fill_form(self, contact):
        self.entry_name.delete(0, tk.END)
        self.entry_name.insert(0, contact['name'])

        self.entry_phone.delete(0, tk.END)
        self.entry_phone.insert(0, contact['phone'])

        self.entry_email.delete(0, tk.END)
        self.entry_email.insert(0, contact['email'])

        self.entry_address.delete(0, tk.END)
        self.entry_address.insert(0, contact['address'])

    def clear_form(self):
        self.entry_name.delete(0, tk.END)
        self.entry_phone.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_address.delete(0, tk.END)
        self.entry_search.delete(0, tk.END)
        self.selected_index = None
        self.btn_add_update.config(text="Add Contact")


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x500")
    app = ContactManager(root)
    root.mainloop()
