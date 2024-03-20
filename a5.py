# Ana Gao
# gaomy@uci.edu
# 26384258

import tkinter as tk
from tkinter import simpledialog
from tkinter import ttk, filedialog
from typing import Text
from ds_messenger import DirectMessenger
from ds_messenger import DirectMessage
from Profile import Profile, DsuProfileError, DsuFileError
from pathlib import Path


class Body(tk.Frame):
    def __init__(self, root, recipient_selected_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._contacts = [str]
        self._select_callback = recipient_selected_callback
        self._draw()

    def node_select(self, event: tk.Event):
        index = int(self.posts_tree.selection()[0])
        entry = self._contacts[index]
        if self._select_callback is not None:
            self._select_callback(entry)
            # print(f"Mouse entered window at position x = {event.x}, y = {event.y}")

    def insert_contact(self, contact: str):
        self._contacts.append(contact)
        id = len(self._contacts) - 1
        self._insert_contact_tree(id, contact)

    def _insert_contact_tree(self, id, contact: str):
        if len(contact) > 25:
            entry = contact[:24] + "..."
        id = self.posts_tree.insert('', id, id, text=contact)

    def insert_user_message(self, message:str):
        self.entry_editor.configure(state='normal')
        self.entry_editor.insert(tk.END, message + '\n', 'entry-right')
        self.entry_editor.configure(state='disabled')

    def insert_contact_message(self, message:str):
        self.entry_editor.configure(state='normal')
        self.entry_editor.insert(1.0, message + '\n', 'entry-left')
        self.entry_editor.configure(state='disabled')

    def get_text_entry(self) -> str:
        return self.message_editor.get('1.0', 'end').rstrip()

    def set_text_entry(self, text:str):
        self.message_editor.delete(1.0, tk.END)
        self.message_editor.insert(1.0, text)

    def _draw(self):
        posts_frame = tk.Frame(master=self, width=250)
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
        self.entry_editor.tag_configure('entry-right', justify='right')
        self.entry_editor.tag_configure('entry-left', justify='left')
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                               expand=True, padx=0, pady=0)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame,
                                              command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT,
                                    expand=False, padx=0, pady=0)


class Footer(tk.Frame):
    def __init__(self, root, send_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback
        self._draw()

    def send_click(self):
        if self._send_callback is not None:
            self._send_callback()

    def _draw(self):
        save_button = tk.Button(master=self, text="Send", width=20,
                                command=self.send_click)
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.footer_label = tk.Label(master=self, text="Ready.")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)


class NewContactDialog(tk.simpledialog.Dialog):
    def __init__(self, root, title=None, user=None, pwd=None, server=None):
        self.root = root
        self.server = server
        self.user = user # 'BLACKPINK' 
        self.pwd = pwd # '2016'
        super.__init__(root, title)

    def body(self, frame):
        self.server_label = tk.Label(frame, width=30, text="DS Server Address")
        self.server_label.pack()
        self.server_entry = tk.Entry(frame, width=30)
        self.server_entry.insert(tk.END, self.server)
        self.server_entry.pack()

        self.username_label = tk.Label(frame, width=30, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(frame, width=30)
        self.username_entry.insert(tk.END, self.user)
        self.username_entry.pack()

        self.password_label = tk.Label(frame, width=30, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(frame, width=30, show='*')
        self.password_entry.insert(tk.END, self.pwd)
        self.password_entry.pack()

    def apply(self):
        self.user = self.username_entry.get()
        self.pwd = self.password_entry.get()
        self.server = self.server_entry.get()


class MainApp(tk.Frame):
    def __init__(self, root, username=None, password=None, server=None, profile_file=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self.username = username
        self.password = password
        self.server = server
        self.recipient = None  
        self.node_selected = None
        self.direct_messenger = None
        self._messages_new = None
        self._messages_all = None
        self.profile_file = profile_file

        self._draw()
        self.load_profile()
        self.check_new()

    def load_profile(self):
        if Path(self.profile_file).is_file():
            try:
                self.profile = Profile()
                self.profile.load_profile(self.profile_file)
                self.username = self.profile.username
                self.password = self.profile.password
                self.server = self.profile.dsuserver
                self._messages_all = self.profile._messages_all
                self._messages_new = self.profile._messages_new
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
        else:
            self.profile = Profile(self.server, self.username, self.password)
            friends = self.profile.get_friends()
            for recipient in friends:
                self.body.insert_contact(recipient)

    def save_profile(self):
        try:
            self.profile.save_profile(self.profile_file)
        except DsuFileError as e:
            print(f"Error saving profile: {e}")

    def select_in_body(self, node):
        self.recipient = node
        self.body.entry_editor.configure(state='normal')
        self.body.entry_editor.delete(1.0, tk.END) 
        self.body.entry_editor.configure(state='disabled')
        self.display_messages(node)
        self.footer.footer_label.configure(text=f"Selected: {node}")

    def display_messages(self, recipient):
        self.body.entry_editor.configure(state='normal')
        self.body.entry_editor.delete(1.0, tk.END) 
        self.body.entry_editor.configure(state='disabled')

        all_messages = []

        user_messages = self.profile.get_messages_all()
        for message_dict in user_messages:
            for msg_recipient, message_list in message_dict.items():
                if msg_recipient == recipient:
                    for msg in message_list:
                        all_messages.append(("sent", msg_recipient, msg['message'], msg['timestamp']))

        contact_messages = self.profile.get_messages_new()
        for msg_dict in contact_messages:
            for rec, msg_list in msg_dict.items():
                if rec == recipient:
                    for _msg in msg_list:
                        all_messages.append(("new", rec, _msg['message'], _msg['timestamp']))

        # Sort messages based on timestamp
        all_messages.sort(key=lambda x: x[3], reverse=True)

        for _type, recepient, message, timestamp in all_messages:
            if _type == "sent":
                self.body.insert_user_message(message)
            elif _type == "new":
                self.body.insert_contact_message(message)

    def send_message(self):
        message = self.body.get_text_entry()
        if self.recipient == None:
            self.footer.footer_label.configure(text="ERROR! No recipient selected!")
        else:
            if message == '' or message.isspace():
                self.footer.footer_label.configure(text="ERROR! INVALID MESSAGE!")
            else:
                if self.direct_messenger.send(message, self.recipient):
                    self.footer.footer_label.configure(text="Sent Direct Message.")
                    self.body.insert_user_message(message)
                    self.profile.push_socMessage(self.recipient, message)
                    self.save_profile()
                else:
                    self.footer.footer_label.configure(text="ERROR! Cannot process request.")
        self.body.set_text_entry("")

    def add_contact(self):
        new_contact = simpledialog.askstring("New Contact:",
                                             "Enter new contact name.", 
                                             parent=self.body)
        if new_contact:
            self.body.insert_contact(new_contact)
            self.profile.add_friends(new_contact)
            self.save_profile()
            print("New contact added")
        else:
            if new_contact == None:
                self.footer.footer_label.configure(text="Cancelled by user.")
            else:
                self.footer.footer_label.configure(text="ERROR! Contact already exists!")

    def configure_server(self):
        ud = NewContactDialog(self.root, "Configure Account",
                              self.username, self.password, self.server)
        self.username = ud.user
        self.password = ud.pwd
        self.server = ud.server
        self.direct_messenger = DirectMessage(self.server, 
                                              self.username,
                                              self.password)

    def check_new(self):
        """
        Check for new messages periodically and add them to the profile.
        """
        try:
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
        except Exception as e:
            print("Error:", e)

    def _draw(self):
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)

        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New')
        menu_file.add_command(label='Open...')
        menu_file.add_command(label='Close')

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


if __name__ == "__main__":
    file = input("Which dsu profile do you want to load? \n") # "profile.dsu"
    file = file.replace("'", "")
    file = file.replace('"', '')

    main = tk.Tk()

    main.title("ICS 32 Distributed Social Messenger")

    main.geometry("720x480")
    main.configure(background='pink')

    main.option_add('*tearOff', False)

    app = MainApp(main, profile_file=file) # '168.235.86.101'

    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    id = main.after(2000, app.check_new)
    print(id)
    main.mainloop()
