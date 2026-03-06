from database import connect_db

def register_user(name, age, gender, occupation, username, password):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO users(name, age, gender, occupation, username, password)
    VALUES (%s, %s, %s, %s, %s, %s)
    """, (name, age, gender, occupation, username, password))

    conn.commit()
    conn.close()


def login_user(username, password):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM users WHERE username=%s AND password=%s
    """, (username, password))

    user = cursor.fetchone()

    conn.close()
    return user
