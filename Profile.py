# Profile.py

# Ana Gao
# 26384258
# gaomy@uci.edu


import json
import time
from pathlib import Path


"""
DsuFileError is a custom exception handler that you should catch
in your own code. It is raised when attempting to load or save
Profile objects to file the system.

"""


class DsuFileError(Exception):
    pass


"""


DsuProfileError is a custom exception handler that you should
catch in your own code. It is raised when attempting to
deserialize a dsu file to a Profile object.

"""


class DsuProfileError(Exception):
    pass


class Post(dict):
    """

    The Post class is responsible for working with individual
    user posts. It currently supports two features:
    A timestamp property that is set upon instantiation and
    when the entry object is set and an entry property
    that stores the post message.

    """

    def __init__(self, entry: str = None, timestamp: float = 0):
        self._timestamp = timestamp
        self.set_entry(entry)

        dict.__init__(self, entry=self._entry, timestamp=self._timestamp)

    def set_entry(self, entry):
        self._entry = entry
        dict.__setitem__(self, 'entry', entry)

        # If timestamp has not been set, generate a new from time module
        if self._timestamp == 0:
            self._timestamp = time.time()

    def get_entry(self):
        return self._entry

    def set_time(self, time: float):
        self._timestamp = time
        dict.__setitem__(self, 'timestamp', time)

    def get_time(self):
        return self._timestamp

    """

    The property method is used to support get and set capability
    for entry and time values. When the value for entry is changed,
    or set, the timestamp field is updated to the current time.

    """

    entry = property(get_entry, set_entry)
    timestamp = property(get_time, set_time)


class Profile:
    """
    The Profile class exposes the properties required to join an
    ICS 32 DSU server. You will need to use this class to manage
    the information provided by each new user created within your
    program for a2. Pay close attention to the properties and
    functions in this class as you will need to make use of each
    of them in your program.

    When creating your program you will need to collect user input
    for the properties exposed by this class. A Profile class
    should ensure that a username and password are set, but contains
    no conventions to do so. You should make sure that your code
    verifies that required properties are set.

    """

    def __init__(self, dsuserver=None, username=None,
                 password=None, friends: list = None,
                 msg_all: list = None, msg_new: list = None):
        self.dsuserver = dsuserver  # REQUIRED
        self.username = username  # REQUIRED
        self.password = password  # REQUIRED
        self.bio = ''             # OPTIONAL
        self._posts = []          # OPTIONAL

        self.friends = friends if friends is not None else []
        self.messages_all = msg_all if msg_all is not None else []
        self.messages_new = msg_new if msg_new is not None else []

    def add_message(self, message, recipient):
        """
        Add a new message to the profile's messages.
        """

        for msg_dict in self.messages_new:
            if recipient in msg_dict:
                msg_dict[recipient].append({"message": message.message,
                                            "timestamp": message.timestamp})
                break
        else:
            msg = message.message
            msg_time = message.timestamp
            self.messages_new.append({recipient: [{"message": msg,
                                                   "timestamp": msg_time}]})

    def push_socMessage(self, rec, message):
        """
        Push a new message to the profile's all messages.
        """

        for msg_dict in self.messages_all:
            if rec in msg_dict:
                msg_dict[rec].append({"message": message,
                                      "timestamp": time.time()})
                break
        else:
            self.messages_all.append({rec: [{"message": message,
                                             "timestamp": time.time()}]})

    def pop_newMessage(self):
        """
        Pop the newest message from new messages.
        """

        rec, msg = self.messages_new.pop(-1)
        self.messages_all.append((rec, msg))
        return (rec, msg)

    def get_messages_new(self):
        """
        Get all new messages.
        """

        return self.messages_new

    def get_messages_all(self):
        """
        Get all messages.
        """
        return self.messages_all

    def add_friends(self, username):
        """
        Add a friend to a contact list if the friend is not in it.
        """

        if username not in self.friends:
            self.friends.append(username)
        else:
            self.friends = self.friends

    def get_friends(self):
        """
        Get friends list.
        """

        return self.friends

    def get_all_message_time(self, message: str):
        """
        Retrieve the timestamp of a message.
        """

        for message_dict in self.messages_all:
            for msg_recipient, message_list in message_dict.items():
                if message in message_list:
                    for msg in message_list:
                        if msg == message:
                            return msg['timestamp']
        return 0

    def get_new_message_time(self, message: str):
        """
        Retrieve the timestamp of a message.
        """

        for message_dict in self.messages_new:
            for msg_recipient, message_list in message_dict.items():
                if message in message_list:
                    for msg in message_list:
                        if msg == message:
                            return msg['timestamp']
        return 0

    """

    add_post accepts a Post object as parameter and appends
    it to the posts list. Posts are stored in a list object
    in the order they are added. So if multiple Posts objects
    are created, but added to the Profile in a different order,
    it is possible for the list to not be sorted by the
    Post.timestamp property. So take caution as to how you
    implement your add_post code.

    """

    def add_post(self, post: Post) -> None:
        self._posts.append(post)

    """

    del_post removes a Post at a given index and
    returns True if successful and False if
    an invalid index was supplied.

    To determine which post to delete you must implement
    your own search operation on the posts returned
    from the get_posts function to find the correct index.

    """

    def del_post(self, index: int) -> bool:
        try:
            del self._posts[index]
            return True
        except IndexError:
            return False

    """

    get_posts returns the list object containing all
    posts that have been added to the Profile object

    """

    def get_posts(self) -> list[Post]:
        return self._posts

    """

    save_profile accepts an existing dsu file to save the
    current instance of Profile to the file system.

    Example usage:

    profile = Profile()
    profile.save_profile('/path/to/file.dsu')

    Raises DsuFileError

    """

    def save_profile(self, path: str) -> None:
        p = Path(path)

        if p.exists() and p.suffix == '.dsu':
            try:
                f = open(p, 'w')
                json.dump(self.__dict__, f, indent=4)
                f.close()
            except Exception as ex:
                raise DsuFileError(
                    "Error while attempting to process the DSU file.", ex)
        else:
            Path(path).touch()
            self.save_profile(path)
            # raise DsuFileError("Invalid DSU file path or type")

    """

    load_profile will populate the current instance of
    Profile with data stored in a DSU file.

    Example usage:

    profile = Profile()
    profile.load_profile('/path/to/file.dsu')

    Raises DsuProfileError, DsuFileError

    """

    def load_profile(self, path: str) -> None:
        p = Path(path)

        if p.exists() and p.suffix == '.dsu':
            try:
                f = open(p, 'r')
                obj = json.load(f)
                self.username = obj['username']
                self.password = obj['password']
                self.dsuserver = obj['dsuserver']
                self.bio = obj['bio']
                self.friends = obj['friends']
                self.messages_all = obj['messages_all']
                self.messages_new = obj['messages_new']
                posts = obj['_posts']
                for post_obj in posts:
                    post = Post(post_obj['entry'], post_obj['timestamp'])
                    self._posts.append(post)
                f.close()
            except Exception as ex:
                raise DsuProfileError(ex)
        else:
            raise DsuFileError()
