import data_creation
import json
from project import Media, Topic




users = data_creation.create_users()
names = [x.username for x in users]
pws = [x.password for x in users]
media = data_creation.create_topics()
list = data_creation.create_lists()



def create_account():
    while True:
        username = input("Enter your username:\n")
        if username not in names:
            break
        else:
            print("That username is taken!")

    password = input("Enter your password:\n")

    f = open("users.txt", "a")
    f.write(username+", "+password+"\n")
    f.close()
    list[username] = {"progress": {}, "ratings": {}}

    print("\nAccount Created!\n")

    return username


def login():
    username = ""

    while username not in names:
        username = input("Enter your username:\n")

    print("")
    password = pws[names.index(username)].strip()  # gets rid of whitespace

    pw = ""
    while pw != password:
        pw = input("Enter password:\n")

    print("\nLogged in successfully!\n")

    return username


def print_topics():
    print("")
    index = 0
    for x in media:
        total_users = 0
        total_rating = 0
        for user in names:
            if list[user]["progress"].get(x.name, -1) == 0:
                total_users += 1
                total_rating += list[user]["ratings"][x.name]
        if total_users == 0:
            if Media(x.media) == Media.tv_show:
                print(str(index)+": "+x.name
                    + " ("+str(x.num_subdivisions)+" episodes, no ratings yet)")
            elif Media(x.media) == Media.book:
                print(str(index)+": "+x.name
                    + " ("+str(x.num_subdivisions)+" chapters, no ratings yet)")
            else:
                print(str(index)+": "+x.name
                    + " ("+str(x.num_subdivisions)+" tracks, no ratings yet)")
        else:
            if Media(x.media) == Media.tv_show:
                print(str(index)+": "+x.name
                    + " ("+str(x.num_subdivisions)+" episodes, average of "+str(total_rating/total_users)+" stars)")
            elif Media(x.media) == Media.book:
                print(str(index)+": "+x.name
                    + " ("+str(x.num_subdivisions)+" chapters, average of "+str(total_rating/total_users)+" stars)")
            else:
                print(str(index)+": "+x.name
                    + " ("+str(x.num_subdivisions)+" tracks, average of "+str(total_rating/total_users)+" stars)")
        index += 1
    print("")


def print_list(username):
    print("")
    index = 0
    for m in media:
        status = list[username]["progress"].get(m.name, -1)
        if status > 0:
            if Media(m.media) == Media.tv_show:
                print(str(index)+": "+m.name
                    + ": In Progress ("+str(status)+"/"+str(m.num_subdivisions)+" episodes)")
            elif Media(m.media) == Media.book:
                print(str(index)+": "+m.name
                    + ": In Progress ("+str(status)+"/"+str(m.num_subdivisions)+" chapters)")
            else:
                print(str(index)+": "+m.name
                    + ": In Progress ("+str(status)+"/"+str(m.num_subdivisions)+" tracks)")
        elif status == 0:
            if Media(m.media) == Media.tv_show:
                print(str(index)+": "+m.name
                    + ": Complete ("+str(m.num_subdivisions)+"/"+str(m.num_subdivisions)+" episodes, rated "+str(list[username]["ratings"][m.name])+" stars)")
            elif Media(m.media) == Media.book:
                print(str(index)+": "+m.name
                    + ": Complete ("+str(m.num_subdivisions)+"/"+str(m.num_subdivisions)+" chapters, rated "+str(list[username]["ratings"][m.name])+" stars)")
            else:
                print(str(index)+": "+m.name
                    + ": Complete ("+str(m.num_subdivisions)+"/"+str(m.num_subdivisions)+" tracks), rated "+str(list[username]["ratings"][m.name])+" stars)")
        else:
            if Media(m.media) == Media.tv_show:
                print(str(index)+": "+m.name
                    + ": Not Started (0/"+str(m.num_subdivisions)+" episodes)")
            elif Media(m.media) == Media.book:
                print(str(index)+": "+m.name
                    + ": Not Started (0/"+str(m.num_subdivisions)+" chapters)")
            else:
                print(str(index)+": "+m.name
                    + ": Not Started (0/"+str(m.num_subdivisions)+" tracks)")
        index += 1
    print("")


def update_topic(username):
    print("")
    while True:
        try:
            index = int(
                input("Enter the no. of the topic you want to change:\n"))
            if index in range(len(media)):
                break
        except ValueError:
            print("Enter an integer!")

    while True:
        try:
            status = int(input(
                "Enter the status of the topic (-1: Not Started, 0: Complete, any other integer: how many subdivisions you've completed)\n"))
            if status == 0:
                while True:
                    try:
                        rating = int(
                            input("Give it a rating from 1-5 stars:\n"))
                        if rating in range(1, 6):
                            break
                        else:
                            print("1 to 5 stars only please!")
                    except ValueError:
                        print("Enter an integer!")
                list[username]["ratings"][media[index].name] = rating
                break
            elif status > -2 and status < media[index].num_subdivisions:
                break
            else:
                print("Can't have more subdivisions completed than there are!")
        except ValueError:
            print("Enter an integer!")

    list[username]["progress"][media[index].name] = status
    print_list(username)


def update_lists(username):
    out_file = open("lists.json", "w")
    json.dump(list, out_file)
    out_file.close()

    if username == "admin":
        f = open("media.txt", "w")
        for m in media:
            f.write(m.name+", "+str(m.media.value)
                    + ", "+str(m.num_subdivisions)+"\n")
        f.close()


def add_topic():
    name = input("Enter the name of the topic you want to add:\n")
    while True:
        try:
            status = int(input(
                "Enter the type of topic (0: TV show, 1: Book, 2: Music album)\n"))
            if status in [0, 1, 2]:
                break
        except ValueError:
            print("Enter an integer!")
    while True:
        try:
            num_subdivisions = int(input(
                "Enter the number of subdivisions:\n"))
            if num_subdivisions > 0:
                break
        except ValueError:
            print("Enter an integer!")
    media.append(Topic(name, status, num_subdivisions))


def remove_topic():
    while True:
        try:
            index = int(
                input("Enter the no. of the topic you want to remove:\n"))
            if index in range(len(media)):
                break
        except ValueError:
            print("Enter an integer!")
    del media[index]
    return


def edit_topic():
    while True:
        try:
            index = int(
                input("Enter the no. of the topic you want to change:\n"))
            if index in range(len(media)):
                break
        except ValueError:
            print("Enter an integer!")

    name = input("Enter the name of the topic:\n")
    while True:
        try:
            status = int(input(
                "Enter the type of topic (0: TV show, 1: Book, 2: Music album)\n"))
            if status in [0, 1, 2]:
                break
        except ValueError:
            print("Enter an integer!")
    while True:
        try:
            num_subdivisions = int(input(
                "Enter the number of subdivisions:\n"))
            if num_subdivisions > 0:
                break
        except ValueError:
            print("Enter an integer!")
    media[index] = Topic(name, status, num_subdivisions)
    return


def check_topic():
    while True:
        try:
            index = int(
                input("Enter the no. of the topic you want to view:\n"))
            if index in range(len(media)):
                break
        except ValueError:
            print("Enter an integer!")
    num_not_started = 0
    num_in_progress = 0
    num_complete = 0
    for user in names:
        status = list[user]["progress"].get(media[index].name, -1)
        if status == -1:
            num_not_started += 1
        elif status == 0:
            num_complete += 1
        else:
            num_in_progress += 1
    print("Number of users who haven't started "
        + media[index].name+": "+str(num_not_started)+"\n")
    print("Number of users who have "
        + media[index].name+" in progress: "+str(num_in_progress)+"\n")
    print("Number of users who have completed "
        + media[index].name+": "+str(num_complete)+"\n")


while True:
    print("""Welcome to the Progress Tracker System!  Please enter an option:
        1: Login
        2: Create an Account""")
    option = input("option: \n")

    match option:
        case "1":
            username = login()
            break
        case "2":
            username = create_account()
            users = data_creation.create_users()
            names = [x.username for x in users]
            break

while True:
    if username == "admin":
        print("""Welcome to the Progress Tracker System!  Please enter an option:
            1: See Topics
            2: See My List
            3: Change Topic Status
            4: Look at Status of a Topic Across all Users
            5: Add Topic
            6: Remove Topic
            7: Edit Topic
            8: Exit""")

        option = input("option: \n")

        match option:
            case "1": print_topics()
            case "2": print_list(username)
            case "3": update_topic(username)
            case "4": check_topic()
            case "5": add_topic()
            case "6": remove_topic()
            case "7": edit_topic()
            case "8":
                update_lists(username)
                break
            case _: print("Not a valid input.")
    else:
        print("""Welcome to the Progress Tracker System!  Please enter an option:
            1: See Topics
            2: See My List
            3: Change Topic Status
            4: Look at Status of a Topic Across all Users
            5: Exit""")

        option = input("option: \n")

        match option:
            case "1": print_topics()
            case "2": print_list(username)
            case "3": update_topic(username)
            case "4": check_topic()
            case "5":
                update_lists(username)
                break
            case _: print("Not a valid input.")