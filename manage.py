from database import MongoDB

db = MongoDB()
print("TorrentWaver Users Management.")
while True:
    print("\nSelect from below options")
    print("1: Add user\n2: Delete user\n3: List users\n4: Exit")
    in_put = input("Enter choice: ")
    if in_put == "1":
        username = input("Enter username: ")
        password = input("Enter password: ")
        db.new_login(username, password)
        print("User added")
    elif in_put == "2":
        username = input("Enter username: ")
        password = input("Enter password: ")
        db.delete_login(username, password)
        print("User added")
    elif in_put == "3":
        print("This list in username:password format\n")
        all_users = db.get_all_logins()
        i = 1
        for user in all_users:
            print(f"{i} = {user['uname']}:{user['pass']}")
            i += 1
    elif in_put == "4":
        exit()
    else:
        print("enter valid choice!")