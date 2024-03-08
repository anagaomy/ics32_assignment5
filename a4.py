# a4.py

# Ana Gao
# gaomy@uci.edu
# 26384258


import ui as cmd
from pathlib import Path
from Profile import Profile as profile
from ds_client import send


# input/output messages
INPUT_C = "Great! What is the name of the journal you would like to create? \n"
INPUT_O = "Great! What is the name of the journal you would like to open? \n"
INPUT_MAIN_MENU = (" PO  - Publish online \n"
                   " C   - Create a new file \n"
                   " O   - Open an existing file \n"
                   " R   - Read file \n"
                   " D   - Delete file \n"
                   " Q   - Quit \n")
INPUT_COMMAND_MENU = " E - Edit file \n P - Print data in file \n Q - Quit \n"
COMMAND_E = (" -svr [SERVER IP ADDRESS] \n"
             " -usr [USERNAME] \n"
             " -pwd [PASSWORD] \n"
             " -bio [BIO] \n"
             " -addpost [NEW POST] \n"
             " -delpost [ID] \n"
             " -publish \n")
COMMAND_P = (" -usr \n"
             " -pwd \n"
             " -bio \n"
             " -posts \n"
             " -post [ID] \n"
             " -all \n"
             " -publish \n")
MSG_C_SUCCESS = "\nNew journal successfully created! \n"
MSG_O_SUCCESS = "Journal is loading successfully! \n"
USRNAME_INPUT = "Enter your username (please do NOT contain whitespace): \n"
PWD_INPUT = "Enter your password (please do Not contain whitespace): \n"
SVR_UPD = "Great! What is the server IP address? \n"
USRNAME_UPD = "Great! What is the username that you want to update? \n"
PSW_UPD = "Great! What is the password that you want to update? \n"
BIO_UPDATE = "Great! What is the bio that you want to update? \n"
POST_UPD = "Great! What post do you want to add? \n"
POST_ID_UPD = "Great! Which post do you want to delete? \n"


def profile_loading(journal: str):
    PROFILE = profile()
    PROFILE.load_profile(str(journal))
    print(MSG_O_SUCCESS)
    print("Here is your current profile info: \n")
    print(f" Username: {PROFILE.username}")
    print(f" Password: {PROFILE.password}")
    print(f" Bio: {PROFILE.bio}")


def data_collection(journal: str):
    username = input(USRNAME_INPUT)
    cmd.input_error_check(username, journal)

    password = input(PWD_INPUT)
    cmd.input_error_check(password, journal)

    bio = input("Enter your bio: \n")
    cmd.user_bio_error_check(bio, journal)

    PROFILE = profile(username=username, password=password)
    PROFILE.bio = bio
    PROFILE.save_profile(str(journal))
    print("User info successfully saved in the Profile!")


def UI_new_commands(journal):
    print("\nWhat would you like to do next?")
    command = input(INPUT_COMMAND_MENU)
    if command == 'E':
        print("Great! Which option do you want to choose? \n")
        option = input(COMMAND_E)
        option = option.strip().split(" ")

        if len(option) > 1:
            try:
                cmd.command_E(journal, option)
            except Exception:
                print("ERROR")

        elif len(option) == 1:
            list = []
            option = ''.join(option)
            if option == '-svr':
                list.append(option)
                server = str(input(SVR_UPD))
                list.append(server)
            elif option == '-usr':
                list.append(option)
                username = input(USRNAME_UPD)
                list.append(username)
            elif option == '-pwd':
                list.append(option)
                password = input(PSW_UPD)
                list.append(password)
            elif option == '-bio':
                list.append(option)
                bio = input(BIO_UPDATE)
                list.append(bio)
            elif option == '-addpost':
                list.append(option)
                post = input(POST_UPD)
                list.append(post)
            elif option == '-delpost':
                list.append(option)
                post_ID = input(POST_ID_UPD)
                list.append(post_ID)
            elif option == '-publish':
                ID = -1
                cmd.publish_from_file(journal, ID)
            else:
                print("Error! Invalid command!")
                exit()
            try:
                cmd.command_E(journal, list)
            except Exception:
                print("ERROR")
        else:
            print("ERROR")
            exit()

    elif command == 'P':
        print("Great! Which option do you want to choose? \n")
        option = input(COMMAND_P)
        option = option.strip().split(" ")

        if len(option) > 1:
            try:
                cmd.command_P(journal, option)
            except Exception:
                print("ERROR")

        elif len(option) == 1:
            list = []
            option = ''.join(option)
            if option == '-post':
                list.append(option)
                post = input("Great! Which post do you want to print? \n")
                list.append(post)
            elif option == '-publish':
                list.append(option)
                post = input("Great! Which post do you want to publish? \n")
                list.append(post)
            else:
                list.append(option)
                try:
                    cmd.command_P(journal, list)
                except Exception:
                    print("ERROR")
            try:
                cmd.command_P(journal, list)
            except Exception:
                print("ERROR")

        else:
            print("ERROR")
            exit()
    elif command == 'Q':
        exit()
    else:
        user_interface(command)
    UI_new_commands(journal)


def user_interface(command: str):
    list = command.split()
    command = list[0]
    if command == "C":
        journal = input(INPUT_C)
        if len(journal.strip().split()) != 1:
            print("Do NOT contain whitespace!")
            exit()
        try:
            if str(journal).endswith('.dsu'):
                if Path(journal).exists():
                    profile_loading(str(journal))
                else:
                    journal = Path(journal)
                    journal.touch()
                    print(MSG_C_SUCCESS)
                    data_collection(str(journal))
            else:
                if Path(journal).suffix != '':
                    Path(journal).touch()
                else:
                    journal = Path(str(journal) + '.dsu')
                    if Path(journal).exists():
                        profile_loading(str(journal))
                    else:
                        journal.touch()
                        print(MSG_C_SUCCESS)
                        data_collection(str(journal))
        except Exception:
            print("Error occured when saving user data!")
        else:
            UI_new_commands(journal)

    elif command == "O":
        try:
            journal = input(INPUT_O)
            journal = cmd.command_O(journal)
        except Exception:
            print("Error! DSU file could not be found!")
        else:
            UI_new_commands(journal)

    elif command == "PO":
        publish_online()

    elif command == "L":
        _admin_(list)

    elif command == "D":
        _admin_(list)

    elif command == "R":
        _admin_(list)

    elif command == "Q":
        exit()

    else:
        print("ERROR")


def new_commands(journal, command):
    print("\nWhat would you like to do next?")
    command = input().split()
    if command[0] == "E":
        cmd.command_E(journal, command)
    elif command[0] == "P":
        cmd.command_P(journal, command)
    elif command[0] == "Q":
        exit()
    else:
        _admin_(command)
    new_commands(journal, command)


def _admin_(command):
    try:
        if command[0] == 'Q':
            quit()

        elif command[0] == 'L':
            directory = command[1]
            if len(command) == 2:
                cmd.command_len2(directory)
            elif len(command) == 3:
                cmd.command_len3(command, directory)
            elif len(command) >= 4:
                if command[2] == '-r':
                    cmd.recursion_options(command, directory)
                elif command[2] == '-s':
                    cmd.list_matching_name(command, directory)
                elif command[2] == '-e':
                    cmd.list_extension(command, directory)
            else:
                print("ERROR")

        elif command[0] == 'C':
            if len(command) > 1:
                directory = command[1]
                journal = cmd.new_file(command, directory)
                new_commands(journal, command)
            else:
                print("ERROR")

        elif command[0] == 'O':
            if len(command) > 1:
                directory = command[1]
                journal = cmd.command_O(directory)
                new_commands(journal, command)
            else:
                print("ERROR")

        elif command[0] == 'D':
            if len(command) > 1:
                directory = command[1]
                cmd.delete_file(command)
            else:
                print("ERROR")

        elif command[0] == 'R':
            if len(command) > 1:
                directory = command[1]
                cmd.read_file(command)
            else:
                print("ERROR")

        else:
            print("ERROR")

    except Exception:
        print("ERROR")
    else:
        print("What would you like to do next? ")
        command = input().strip().split()
        _admin_(command)


def publish_online():
    port = 3021
    server = str(input("Enter a server IP address: "))  # 168.235.86.101
    username = str(input("Enter your username: "))
    password = str(input("Enter your password: "))
    bio_option = str(input("Would you like to add a bio? (y/n) "))
    if bio_option == 'y':
        bio = str(input("Enter your bio: "))
    elif bio_option == 'n':
        bio = None
    else:
        print("NO BIO")
        bio = None
    message = str(input("Enter a post message: "))

    if send(server, port, username, password, message, bio):
        print("Operation completed successfully!")
        exit()
    else:
        print("Oops! Operation failed!")
        exit()


def main():
    print("Welcome! What would you like to do? \n")
    print(INPUT_MAIN_MENU)
    user_input = input()
    if user_input == "admin":
        print("You are successfully in ADMIN mode!")
        print("What would you like to do? ")
        command = input().strip().split()
        _admin_(command)
    else:
        user_interface(user_input)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print("Uh oh, there is an error occured!")