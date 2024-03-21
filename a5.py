# Ana Gao
# gaomy@uci.edu
# 26384258


"""
Distributed Social Messenger Application
This script implements a GUI application for a distributed social messenger.
"""

from pathlib import Path
import tkinter as tk
from tkinter import simpledialog
from tkinter import ttk
from ds_messenger import DirectMessenger
from Profile import Profile, DsuProfileError, DsuFileError


class Body(tk.Frame):
    """
    Represents the main body of the application GUI.
    """

    def __init__(self, root, recipient_selected_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._contacts = [str]
        self._select_callback = recipient_selected_callback
        self._draw()

    def node_select(self, event: tk.Event):
        """
        Callback function for selecting a contact node.
        """
        index = int(self.posts_tree.selection()[0])
        entry = self._contacts[index]
        if self._select_callback is not None:
            self._select_callback(entry)
            print(f"x = {event.x}, y = {event.y}")

    def insert_contact(self, contact: str):
        """
        Insert a new contact into the contact list.
        """
        self._contacts.append(contact)
        _id = len(self._contacts) - 1
        self._insert_contact_tree(_id, contact)

    def _insert_contact_tree(self, _id, contact: str):
        """
        Insert a contact into the Treeview widget.
        """
        if len(contact) > 25:
            contact = contact[:24] + "..."
        _id = self.posts_tree.insert('', _id, _id, text=contact)

    def insert_user_message(self, message: str):
        """
        Insert a user message into the entry editor.
        """
        self.entry_editor.configure(state='normal')
        self.entry_editor.insert(tk.END, message + '\n', 'entry-right')
        self.entry_editor.configure(state='disabled')
        self.entry_editor.see(tk.END)

    def insert_contact_message(self, message: str):
        """
        Insert a contact message into the entry editor.
        """
        self.entry_editor.configure(state='normal')
        self.entry_editor.insert(tk.END, message + '\n', 'entry-left')
        self.entry_editor.configure(state='disabled')
        self.entry_editor.see(tk.END)

    def get_text_entry(self) -> str:
        """
        Get the text from the message editor.
        """
        return self.message_editor.get('1.0', 'end').rstrip()

    def set_text_entry(self, text: str):
        """
        Set the text of the message editor.
        """
        self.message_editor.delete(1.0, tk.END)
        self.message_editor.insert(1.0, text)

    def _draw(self):
        """
        Draw the main body components.
        """
        posts_frame = tk.Frame(master=self, width=250, bg='pink')
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)

        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP,
                             expand=True, padx=5, pady=5)

        entry_frame = tk.Frame(master=self, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        editor_frame = tk.Frame(master=entry_frame, bg="red")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        scroll_frame = tk.Frame(master=entry_frame, bg="blue", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        message_frame = tk.Frame(master=self, bg="yellow")
        message_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=False)

        self.message_editor = tk.Text(message_frame, width=0, height=5)
        self.message_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                                 expand=True, padx=0, pady=0)

        self.entry_editor = tk.Text(editor_frame, width=0, height=5)
        self.entry_editor.tag_configure('entry-right',
                                        justify='right',
                                        background='pink', )
        self.entry_editor.tag_configure('entry-left',
                                        justify='left', background='#F5F5F5',
                                        foreground='pink')
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                               expand=True, padx=0, pady=0)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame,
                                              command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT,
                                    expand=False, padx=0, pady=0)


class Footer(tk.Frame):
    """
    Represents the footer of the application GUI.
    """

    def __init__(self, root, send_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback
        self._draw()

    def send_click(self):
        """
        Callback function for the send button click event.
        """
        if self._send_callback is not None:
            self._send_callback()

    def _draw(self):
        """
        Draw the footer components.
        """
        save_button = tk.Button(master=self, text="Send", width=20,
                                command=self.send_click)
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.footer_label = tk.Label(master=self, text="Ready.")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)


class NewContactDialog(tk.simpledialog.Dialog):
    """
    Dialog window for adding a new contact.
    """

    def __init__(self, root, title=None, user=None,
                 pwd=None, server='168.235.86.101'):
        self.server = server
        self.user = user
        self.pwd = pwd
        super().__init__(root, title)

    def body(self, master):
        """
        Create dialog body.
        """
        server_label = tk.Label(master, width=30, text="DS Server Address")
        server_label.pack()
        self.server_entry = tk.Entry(master, width=30)
        self.server_entry.insert(tk.END, self.server)
        self.server_entry.pack()

        username_label = tk.Label(master, width=30, text="Username")
        username_label.pack()
        self.username_entry = tk.Entry(master, width=30)
        self.username_entry.insert(tk.END, self.user)
        self.username_entry.pack()

        password_label = tk.Label(master, width=30, text="Password")
        password_label.pack()
        self.password_entry = tk.Entry(master, width=30, show='*')
        self.password_entry.insert(tk.END, self.pwd)
        self.password_entry.pack()

    def apply(self):
        """
        Apply changes made in the dialog.
        """
        self.user = self.username_entry.get()
        self.pwd = self.password_entry.get()
        self.server = self.server_entry.get()


class MainApp(tk.Frame):
    """
    Represents the main application.
    """

    def __init__(self, root, server='168.235.86.101',
                 profile_file=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self.username = None
        self.password = None
        self.server = server
        self.recipient = None
        self.direct_messenger = None
        self.profile = Profile()
        self.profile_file = profile_file
        self._draw()

    def open_profile(self):
        """
        Open user profile with profile name.
        """
        profile_name = simpledialog.askstring("Open Profile:",
                                              "Enter your profile name.",
                                              parent=self.body)
        if Path(profile_name).is_file() and Path(profile_name).exists:
            self.profile_file = profile_name
            self.load_profile()
            self.save_profile()
            print("Profile opened successfully!")
        else:
            if profile_name is None:
                self.footer.footer_label.configure(
                    text="Cancelled by user.")
            else:
                self.footer.footer_label.configure(
                    text="ERROR! Profile does not exist!")

    def new_profile(self):
        """
        Create a new user profile if it does not exist.
        """
        new_file_name = simpledialog.askstring("New Profile:",
                                               "Enter your profile name.",
                                               parent=self.body)
        username = simpledialog.askstring("Username:",
                                          "Enter your username.",
                                          parent=self.body)
        password = simpledialog.askstring("Password:",
                                          "Enter your password.",
                                          parent=self.body)
        self.username = username
        self.password = password
        self.profile = Profile(self.server, self.username, self.password)
        if Path(new_file_name).exists() and new_file_name.endswith('.dsu'):
            self.profile_file = new_file_name
            self.load_profile()
        else:
            if new_file_name is None:
                self.footer.footer_label.configure(
                    text="Cancelled by user.")
            else:
                new_file_name = new_file_name + '.dsu'
                self.profile_file = new_file_name
        self.save_profile()
        self.load_profile()
        print("Profile created successfully!")

    def close_profile(self):
        """
        diconnect connection to the dsu server.
        """
        self.direct_messenger = DirectMessenger()
        self.direct_messenger.close_connection()

    def load_profile(self):
        """
        Load user profile from the profile file.
        """
        try:
            self.profile = Profile(self.server, self.username, self.password)
            self.profile.load_profile(self.profile_file)
            self.username = self.profile.username
            self.password = self.profile.password
            self.server = self.profile.dsuserver
            self.direct_messenger = DirectMessenger(self.server,
                                                    self.username,
                                                    self.password)
            for item in self.body.posts_tree.get_children():
                self.body.posts_tree.delete(item)
            friends = self.profile.get_friends()
            for friend in friends:
                self.body.insert_contact(friend)
        except (DsuProfileError, DsuFileError) as e:
            print(f"Error loading profile: {e}")

    def save_profile(self):
        """
        Save user profile to the profile file.
        """
        try:
            self.profile.save_profile(self.profile_file)
        except DsuFileError as e:
            print(f"Error saving profile: {e}")

    def select_in_body(self, node):
        """
        Select a contact in the body.
        """
        self.recipient = node
        self.body.entry_editor.configure(state='normal')
        self.body.entry_editor.delete(1.0, tk.END)
        self.body.entry_editor.configure(state='disabled')
        self.display_messages(node)
        self.footer.footer_label.configure(text=f"Selected: {node}")

    def display_messages(self, recipient):
        """
        Display messages for the selected recipient.
        """
        self.body.entry_editor.configure(state='normal')
        self.body.entry_editor.delete(1.0, tk.END)
        self.body.entry_editor.configure(state='disabled')

        all_messages = []

        user_messages = self.profile.get_messages_all()
        for message_dict in user_messages:
            for msg_recipient, message_list in message_dict.items():
                if msg_recipient == recipient:
                    for msg in message_list:
                        all_messages.append(("sent", msg_recipient,
                                             msg['message'], msg['timestamp']))

        contact_messages = self.profile.get_messages_new()
        for msg_dict in contact_messages:
            for rec, msg_list in msg_dict.items():
                if rec == recipient:
                    for _msg in msg_list:
                        all_messages.append(("new", rec, _msg['message'],
                                             _msg['timestamp']))

        # Sort messages based on timestamp
        all_messages.sort(key=lambda x: x[2])
        self.body.entry_editor.configure(state='normal')
        self.body.entry_editor.delete(1.0, tk.END)

        for _type, _, message, _ in all_messages:
            if _type == "sent":
                self.body.entry_editor.insert(tk.END, message +
                                              '\n', 'entry-right')
            elif _type == "new":
                self.body.entry_editor.insert(tk.END, message +
                                              '\n', 'entry-left')

        self.body.entry_editor.configure(state='disabled')
        self.body.entry_editor.see(tk.END)

    def send_message(self):
        """
        Send a message to the selected recipient.
        """
        message = self.body.get_text_entry()
        if self.recipient is None:
            self.footer.footer_label.configure(
                text="ERROR! No recipient selected!")
        else:
            if message == '' or message.isspace():
                self.footer.footer_label.configure(
                    text="ERROR! INVALID MESSAGE!")
            else:
                if self.direct_messenger.send(message, self.recipient):
                    self.footer.footer_label.configure(
                        text="Sent Direct Message.")
                    self.body.insert_user_message(message)
                    self.profile.push_socMessage(self.recipient, message)
                    self.save_profile()
                else:
                    self.footer.footer_label.configure(
                        text="ERROR! Cannot process request.")
        self.body.set_text_entry("")

    def add_contact(self):
        """
        Add a new contact.
        """
        new_contact = simpledialog.askstring("New Contact:",
                                             "Enter new contact name.",
                                             parent=self.body)
        if new_contact:
            self.body.insert_contact(new_contact)
            self.profile.add_friends(new_contact)
            self.save_profile()
            print("New contact added")
        else:
            if new_contact is None:
                self.footer.footer_label.configure(
                    text="Cancelled by user.")
            else:
                self.footer.footer_label.configure(
                    text="ERROR! Contact already exists!")

    def configure_server(self):
        """
        Configure the DS server.
        """
        ud = NewContactDialog(self.root, "Configure Account",
                              self.username, self.password,
                              self.server)
        self.username = ud.user
        self.password = ud.pwd
        self.server = ud.server
        self.direct_messenger = DirectMessenger(dsuserver=self.server,
                                                username=self.username,
                                                password=self.password)

    def check_new(self):
        """
        Check for new messages periodically and add them to the profile.
        """
        if self.direct_messenger is not None:
            messages = self.direct_messenger.retrieve_new()
            for dm in messages:
                self.profile.add_message(dm, dm.recipient)
                if dm.recipient not in self.profile.get_friends():
                    self.body.insert_contact(dm.recipient)
                    self.profile.add_friends(dm.recipient)
                self.save_profile()
            self.root.after(2000, self.check_new)
        else:
            print("Error: DirectMessenger not properly initialized.")

    def _draw(self):
        """
        Draw the main application components.
        """
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)

        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New', command=self.new_profile)
        menu_file.add_command(label='Open...', command=self.open_profile)
        menu_file.add_command(label='Close', command=self.close_profile)

        settings_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=settings_file, label='Settings')
        settings_file.add_command(label='Add Contact',
                                  command=self.add_contact)
        settings_file.add_command(label='Configure DS Server',
                                  command=self.configure_server)

        self.body = Body(self.root,
                         recipient_selected_callback=self.select_in_body)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.footer = Footer(self.root, send_callback=self.send_message)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)


def main():
    """
    Main function to run the application.
    """
    mainapp = tk.Tk()
    mainapp.title("ICS 32 Distributed Social Messenger")
    mainapp.geometry("720x480")
    mainapp.configure(background='pink')
    mainapp.option_add('*tearOff', False)

    app = MainApp(mainapp)
    mainapp.update()
    mainapp.minsize(mainapp.winfo_width(), mainapp.winfo_height())
    _id = mainapp.after(2000, app.check_new)
    print(_id)

    mainapp.mainloop()


if __name__ == "__main__":
    main()
