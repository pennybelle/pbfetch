def parse():
    file = "/etc/passwd"
    try:
        with open(file) as passwd:
            passwd = passwd.readlines()[::-1]

        for line in passwd:
            if ":1000:1000::/home/" in line:
                user = line.split(":").pop(0)

        return user

    except Exception as e:
        print(e)
        return None
