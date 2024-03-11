# ui.py

# Ana Gao
# gaomy@uci.edu
# 26384258


import a4 as cmd
from pathlib import Path
from Profile import Profile as profile
from ds_client import send
from LastFM import LastFM
from OpenWeather import OpenWeather


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
COMMAND_P = (" -svr \n"
             " -usr \n"
             " -pwd \n"
             " -bio \n"
             " -posts \n"
             " -post [ID]"
             " \n -all \n"
             " -publish \n")
MSG_C_SUCCESS = "New journal successfully created! \n"
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

    print(f"Username: {PROFILE.username}")
    print(f"Password: {PROFILE.password}")
    print(f"Bio: {PROFILE.bio}")


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
    print("What would you like to do next?")
    command = input(INPUT_COMMAND_MENU)

    if len(command) == 0:
        print("ERROR")
        UI_new_commands(journal)

    if command == 'E':
        print("Great! Which option do you want to choose? \n")
        option = input(COMMAND_E)
        option = option.strip().split()

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
                cmd.command_E(journal, list)
                print("Server IP address successfully updated!")

            elif option == '-usr':
                list.append(option)
                username = input(USRNAME_UPD)
                list.append(username)
                cmd.command_E(journal, list)
                print("Username succeffully updated!")

            elif option == '-pwd':
                list.append(option)
                password = input(PSW_UPD)
                list.append(password)
                cmd.command_E(journal, list)
                print("User password succeffully updated!")

            elif option == '-bio':
                list.append(option)
                bio = input(BIO_UPDATE)
                bio = api_translude(bio)
                list.append(bio)
                cmd.command_E(journal, list)
                print("Profile bio succeffully updated!")

            elif option == '-addpost':
                list.append(option)
                post = input(POST_UPD)
                post = api_translude(post)
                list.append(post)
                cmd.command_E(journal, list)
                print("New post successfully added to profile!")

            elif option == '-delpost':
                list.append(option)
                post_ID = input(POST_ID_UPD)
                list.append(post_ID)
                cmd.command_E(journal, list)
                print("Selected post successfully deleted from profile!")

            elif option == '-publish':
                ID = -1
                if cmd.publish_from_file(journal, ID):
                    print("User Profile successful published to the server!")

            else:
                print("ERROR")

        else:
            print("ERROR")

    elif command == 'P':
        print("Great! Which option do you want to choose? \n")
        option = input(COMMAND_P)
        option = option.strip().split(" ")

        if len(option) > 1:
            if not cmd.command_P(journal, list):
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

            if not cmd.command_P(journal, list):
                print("ERROR")

        else:
            print("ERROR")
            # quit()

    elif command == 'Q':
        quit()

    else:
        user_interface(command)
    UI_new_commands(journal)


def user_interface(command: str):
    list = command.split()
    command = list[0]
    if command == "C":
        journal = input(INPUT_C)
        if len(journal.strip().split()) != 1:
            print("Error! Do NOT contain whitespace!")
            user_interface(command)
            # quit()
        try:
            if str(journal).endswith('.dsu'):
                if Path(journal).exists():
                    print(MSG_O_SUCCESS)
                    print("Here is your current profile info: \n")
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
                        print(MSG_O_SUCCESS)
                        print("Here is your current profile info: \n")
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
            if len(journal.strip().split()) != 1:
                print("ERROR")
                user_interface(command)
            journal = cmd.command_O(journal)
        except FileNotFoundError:
            print("Error! No such directory/file found!")
        except NotADirectoryError:
            print("Error! Not a directory!")
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
        quit()

    else:
        print("ERROR")
        ui_main()


def new_commands(journal: str, command):
    command = input("What would you like to do next? \n").split()
    if len(command) == 0:
        print("ERROR")
        new_commands(journal, command)
    if command[0] == "E":
        if not cmd.command_E(journal, command[1:]):
            new_commands(journal, command[1:])
    elif command[0] == "P":
        if not cmd.command_P(journal, command[1:]):
            new_commands(journal, command[1:])
    elif command[0] == "Q":
        quit()
    else:
        _admin_(command)
    new_commands(journal, command)


def _admin_(command):
    try:
        if len(command) == 0:
            print("ERROR")
            command = input("What would you like to do next? \n").split()
            _admin_(command)

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
                journal = cmd.admin_new_file(command, directory)
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

        elif command[0] == 'PO':
            publish_online()

        else:
            print("ERROR")
            command = input("What would you like to do next? \n").split()
            _admin_(command)

        command = input("What would you like to do next? \n").split()
        _admin_(command)

    except Exception:
        print("ERROR")

    else:
        command = input("What would you like to do next? \n").split()
        _admin_(command)


def publish_online():
    port = 3021
    server = str(input("Enter a server IP address: "))  # 168.235.86.101
    username = str(input("Enter your username: "))
    password = str(input("Enter your password: "))
    bio_option = str(input("Would you like to add a bio? (y/n): "))
    if bio_option == 'y':
        bio = str(input("Enter your bio: "))
        bio = api_translude(bio)
    elif bio_option == 'n':
        bio = None
    else:
        print("NO BIO")
        bio = None
    message = str(input("Enter a post message: "))
    result = api_translude(message)

    if send(server, port, username, password, result, bio):
        print("Operation completed successfully!")
    else:
        print("Oops! Operation failed!")

    ui_main()


def api_translude(message) -> str:
    if '@weather' in message:
        apikey_ow = str(input("Enter your API key for OpenWeather: "))
        open_weather = OpenWeather()
        open_weather.set_apikey(apikey_ow)
        open_weather.load_data()
        message = open_weather.transclude(message)

    if '@lastfm' in message:
        apikey_lfm = str(input("Enter your API key for LastFM: "))
        lastfm = LastFM()
        lastfm.set_apikey(apikey_lfm)
        lastfm.load_data()
        message = lastfm.transclude(message)

    return message


def ui_main():
    try:
        user_input = input(f"Welcome! What would you like to do? \
                           \n{INPUT_MAIN_MENU}")
        if len(user_input) == 0:
            print("ERROR")
            ui_main()
        if user_input == "admin":
            command = input("What would you like to do? \n").strip().split()
            _admin_(command)
        else:
            user_interface(user_input)

    except FileNotFoundError:
        print("Error! No such directory/file found!")
        ui_main()

    except NotADirectoryError:
        print("Error! Not a directory!")
        ui_main()
