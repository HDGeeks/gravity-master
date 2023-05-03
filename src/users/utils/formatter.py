def userFormatter(users):
    allUsers = []

    for user in users:
        singleUser = {}
        singleUser["id"] = user.pk
        singleUser["first_name"] = user.first_name
        singleUser["last_name"] = user.last_name
        singleUser["username"] = user.username
        singleUser["email"] = user.email
        singleUser["role_id"] = user.role.pk
        singleUser["phone"] = user.phone
        singleUser["password"] = "9762" + user.username + "data"

        allUsers.append(singleUser)

    return allUsers
