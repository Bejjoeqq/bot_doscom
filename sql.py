import sqlite3

def select(q):
    connection = sqlite3.connect("doscom.db")
    cursor = connection.cursor()

    cursor.execute(q)
    hasil =  cursor.fetchall()

    cursor.close()
    connection.close()

    return hasil

def insert_admin(username):
	connection = sqlite3.connect("doscom.db")
	crud_query = "INSERT INTO admins(username) VALUES(?);"
	cursor = connection.cursor()

	cursor.execute(crud_query,[username])

	connection.commit()
	cursor.close()
	connection.close()

def insert_save(title,description, url):
	connection = sqlite3.connect("doscom.db")
	crud_query = "INSERT INTO storages(title,description,url) VALUES(?,?,?);"
	cursor = connection.cursor()

	cursor.execute(crud_query,[title,description, url])

	connection.commit()
	cursor.close()
	connection.close()

def insert_event(name, dates, description, photo):
	connection = sqlite3.connect("doscom.db")
	crud_query = "INSERT INTO events(name,description,dates,photo) VALUES(?,?,?,?);"
	cursor = connection.cursor()

	cursor.execute(crud_query,[name,description,dates,photo])
	ids = cursor.lastrowid

	connection.commit()
	cursor.close()
	connection.close()

	return ids

def update_present(event_id,telegram_id,present,not_present):
    connection = sqlite3.connect('doscom.db')
    cursor = connection.cursor()

    crud_query = f"Update events_members set present = {present}, not_present = {not_present} WHERE event_id = {event_id} and telegram_id = {telegram_id};"
    cursor.execute(crud_query)

    connection.commit()
    cursor.close()
    connection.close()

def insert_state(telegram_id, event_id, first_name):
	connection = sqlite3.connect('doscom.db')
	crud_query = "INSERT INTO events_members(telegram_id,event_id,first_name) VALUES(?,?,?);"
	cursor = connection.cursor()

	cursor.execute(crud_query,[telegram_id, event_id, first_name])

	connection.commit()
	cursor.close()
	connection.close()

if __name__ == "__main__":
	print('tes')