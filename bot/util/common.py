import os

def id_by_username(username):
    # get absolute path of the database
    path = os.path.dirname(os.path.abspath(__file__))
    path = path[:path.index("/util")]

    with open(path + '/Nika.log', 'r') as file:
        for line in file:
            if "CAPTCHA sent" in line:
                if username == line.split("- name:")[1].split("-")[0].strip():
                    user_id = int(line.split("CAPTCHA sent. id:")[1].split("-")[0])
                    break
            elif "NEW USER" in line:
                if username == line.split("- name:")[1].split("-")[0].strip():
                    user_id = int(line.split("NEW USER. id:")[1].split("-")[0])
                    break
            if "LOST USER" in line:
                if username == line.split("- name:")[1].split("-")[0].strip():
                    user_id = int(line.split("LOST USER. id:")[1].split("-")[0])
                    break
        else:
            user_id = None
        
    return user_id