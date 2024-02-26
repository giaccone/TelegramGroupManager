# function
def isin(conn, user_id, chat_id):
    """Check if a user is in a database

    Parameters
    ----------
    conn : sqlite3.Connection
        open connection to a database
    user_id : int
    chat_id : int

    Returns
    -------
    bool
        True if the used is in the database, False otherwise
    """
    cursor = conn.execute("SELECT * FROM warning_list WHERE user_id=:id AND chat_id=:chat_id",
                          {"id":user_id, "chat_id":chat_id})
    row = cursor.fetchone()
    if row is not None:
        return True
    else:
        return False
    

def add_user(conn, user_id, username, name, chat_id, chat_title):
    """Add a user in a database setting warn count to 1

    Parameters
    ----------
    conn : sqlite3.connection
        open connection to a database
    user_id : int
    username : str
    name : str
        _description_
    chat_id : int
        chat id
    chat_title : int
        chat title

    Returns
    -------
    counter: int
        warning counter
    """
    with conn:
        counter = 1
        cursor = conn.cursor()
        cursor.execute("INSERT INTO warning_list VALUES (:user_id, :username, :name, :chat_id, :chat_title, :counter)",
                       {"user_id":user_id, "username":username, "name":name, "chat_id":chat_id, "chat_title":chat_title, "counter":counter})
        
    return counter


def remove_user(conn, user_id, chat_id):
    """remove user from database

    Parameters
    ----------
    conn : _type_
        _description_
    user_id : _type_
        _description_
    chat_id : _type_
        _description_
    """
    with conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM warning_list WHERE user_id=:id AND chat_id=:chat_id",
                       {"id":user_id, "chat_id":chat_id})


def update_user(conn, user_id, chat_id, update_value):
    """update user info in a database

    Parameters
    ----------
    conn : sqlite3.Connection
        _description_
    user_id : int
        
    chat_id : int
        
    update_value : int
        increment of the counter (set a negative value if you want to decrease the counter)

    Returns
    -------
    counter: int
        warning counter
    """
    with conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM warning_list WHERE user_id=:id AND chat_id=:chat_id",
                       {"id":user_id, "chat_id":chat_id})
        counter = cursor.fetchone()[-1]
        counter = counter + update_value
        if counter == 3:
            remove_user(conn, user_id, chat_id)
        else:
            cursor.execute("UPDATE warning_list SET warn_count=:counter WHERE user_id=:id AND chat_id=:chat_id",
                       {"id":user_id, "chat_id":chat_id, "counter":counter})
        
        return counter

