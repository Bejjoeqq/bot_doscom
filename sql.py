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

def setBirth():
	data = """111202013065@mhs.dinus.ac.id|NURUL ISMAWATI|A11.2020.13065|http://mahasiswa.dinus.ac.id/images/foto/A/A11/2020/A11.2020.13065.jpg 23 06 2002
111201911829@mhs.dinus.ac.id|ARDI NUR HANDOYO MUKTI|A11.2019.11829|http://mahasiswa.dinus.ac.id/images/foto/A/A11/2019/A11.2019.11829.jpg 02 02 2001
111202012605@mhs.dinus.ac.id|WAHYU MAULANA PRAWIRO|A11.2020.12605|http://mahasiswa.dinus.ac.id/images/foto/A/A11/2020/A11.2020.12605.jpg 24 05 2002
111201911929@mhs.dinus.ac.id|MOHAMMAD AZWAR SYECHUNA NAZIYULLAH|A11.2019.11929|http://mahasiswa.dinus.ac.id/images/foto/A/A11/2019/A11.2019.11929.jpg 26 09 1997
111202012849@mhs.dinus.ac.id|WISNU MUHAMMAD RAMADHAN|A11.2020.12849|http://mahasiswa.dinus.ac.id/images/foto/A/A11/2020/A11.2020.12849.jpg 07 12 2001
111202013038@mhs.dinus.ac.id|DINITA KUSUMASARI|A11.2020.13038|http://mahasiswa.dinus.ac.id/images/foto/A/A11/2020/A11.2020.13038.jpg 21 02 2002
111201912322@mhs.dinus.ac.id|MAULANA MALIK IBRAHIM|A11.2019.12322|http://mahasiswa.dinus.ac.id/images/foto/A/A11/2019/A11.2019.12322.jpg 17 08 1999
111202013106@mhs.dinus.ac.id|NI MADE KIREI KHARISMA HANDAYANI|A11.2020.13106|http://mahasiswa.dinus.ac.id/images/foto/A/A11/2020/A11.2020.13106.jpg 16 04 2002
111201911943@mhs.dinus.ac.id|ROFI NOOR SALIM|A11.2019.11943|http://mahasiswa.dinus.ac.id/images/foto/A/A11/2019/A11.2019.11943.jpg 22 12 2001
111202013084@mhs.dinus.ac.id|ROSALIA NATAL SILALAHI|A11.2020.13084|http://mahasiswa.dinus.ac.id/images/foto/A/A11/2020/A11.2020.13084.jpg 23 12 2002
111202012812@mhs.dinus.ac.id|MUHAMMAD DAFFA AL FAHREZA|A11.2020.12812|http://mahasiswa.dinus.ac.id/images/foto/A/A11/2020/A11.2020.12812.jpg 03 09 2002
111202013127@mhs.dinus.ac.id|ANA MILATUL KHAULIYA|A11.2020.13127|http://mahasiswa.dinus.ac.id/images/foto/A/A11/2020/A11.2020.13127.jpg 06 03 2002
111202012548@mhs.dinus.ac.id|NEHA WAHYUNINGATI|A11.2020.12548|http://mahasiswa.dinus.ac.id/images/foto/A/A11/2020/A11.2020.12548.jpg 28 01 2002
111202012972@mhs.dinus.ac.id|ENRICO ZADA|A11.2020.12972|http://mahasiswa.dinus.ac.id/images/foto/A/A11/2020/A11.2020.12972.jpg 11 12 2000
111202012549@mhs.dinus.ac.id|BADRUL AKBAR AL MUTHOHHAR|A11.2020.12549|http://mahasiswa.dinus.ac.id/images/foto/A/A11/2020/A11.2020.12549.jpg 05 09 2002
111201911835@mhs.dinus.ac.id|MUHAMMAD MIRZA RAZZAQ|A11.2019.11835|http://mahasiswa.dinus.ac.id/images/foto/A/A11/2019/A11.2019.11835.jpg 16 05 2001
111202012980@mhs.dinus.ac.id|ANGGITA PRAMESWARI DARMAWAN|A11.2020.12980|http://mahasiswa.dinus.ac.id/images/foto/A/A11/2020/A11.2020.12980.jpg 03 10 2002
111202013068@mhs.dinus.ac.id|HAFIIDH AKBAR SYA'BANI|A11.2020.13068|http://mahasiswa.dinus.ac.id/images/foto/A/A11/2020/A11.2020.13068.jpg 30 10 2001
111202013034@mhs.dinus.ac.id|MALIK AZIZ ALI|A11.2020.13034|http://mahasiswa.dinus.ac.id/images/foto/A/A11/2020/A11.2020.13034.jpg 29 10 2002
111202012864@mhs.dinus.ac.id|SALWA SALSABILA|A11.2020.12864|http://mahasiswa.dinus.ac.id/images/foto/A/A11/2020/A11.2020.12864.jpg 29 11 2001
111201912319@mhs.dinus.ac.id|SAMSUN MAARIF|A11.2019.12319|http://mahasiswa.dinus.ac.id/images/foto/A/A11/2019/A11.2019.12319.jpg 12 12 2000
111202013046@mhs.dinus.ac.id|YUNIA SAFITRI|A11.2020.13046|http://mahasiswa.dinus.ac.id/images/foto/A/A11/2020/A11.2020.13046.jpg 03 06 2002
111201912250@mhs.dinus.ac.id|AZWAN NURFADHILLAH|A11.2019.12250|http://mahasiswa.dinus.ac.id/images/foto/A/A11/2019/A11.2019.12250.jpg 13 02 2001
111202012969@mhs.dinus.ac.id|KHALIVIO RAHMYANTO PUTRA|A11.2020.12969|http://mahasiswa.dinus.ac.id/images/foto/A/A11/2020/A11.2020.12969.jpg 26 09 2002
111202013154@mhs.dinus.ac.id|AHMAD ALAIK MAULANI|A11.2020.13154|http://mahasiswa.dinus.ac.id/images/foto/A/A11/2020/A11.2020.13154.jpg 18 01 2001
111201912183@mhs.dinus.ac.id|LILIK WAHYU NUGROHO|A11.2019.12183|http://mahasiswa.dinus.ac.id/images/foto/A/A11/2019/A11.2019.12183.jpg 17 04 2001
111202013039@mhs.dinus.ac.id|DADY BIMA NUR SEJATI|A11.2020.13039|http://mahasiswa.dinus.ac.id/images/foto/A/A11/2020/A11.2020.13039.jpg 20 06 2002
111201911924@mhs.dinus.ac.id|DERY NUGROHO MARJUKI|A11.2019.11924|http://mahasiswa.dinus.ac.id/images/foto/A/A11/2019/A11.2019.11924.jpg 02 12 1999
111201911952@mhs.dinus.ac.id|MUNCHAMINNA|A11.2019.11952|http://mahasiswa.dinus.ac.id/images/foto/A/A11/2019/A11.2019.11952.jpg 26 12 2000
111201912186@mhs.dinus.ac.id|RIFQI MULYA KISWANTO|A11.2019.12186|http://mahasiswa.dinus.ac.id/images/foto/A/A11/2019/A11.2019.12186.jpg 08 07 2000
112201906271@mhs.dinus.ac.id|SYIFA NURAZIZAH|A12.2019.06271|http://mahasiswa.dinus.ac.id/images/foto/A/A12/2019/A12.2019.06271.jpg 03 02 2001
112201906161@mhs.dinus.ac.id|MAITSA DWI ATSIELA|A12.2019.06161|http://mahasiswa.dinus.ac.id/images/foto/A/A12/2019/A12.2019.06161.jpg 16 09 2000
111201911746@mhs.dinus.ac.id|MUHAMMAD RAFFIN DWI AKBAR|A11.2019.11746|http://mahasiswa.dinus.ac.id/images/foto/A/A11/2019/A11.2019.11746.jpg 11 01 2002
111201911910@mhs.dinus.ac.id|DIMAS SETO WICAKSANA|A11.2019.11910|http://mahasiswa.dinus.ac.id/images/foto/A/A11/2019/A11.2019.11910.jpg 23 05 2001
111201912096@mhs.dinus.ac.id|ILHAM PRASETYA|A11.2019.12096|http://mahasiswa.dinus.ac.id/images/foto/A/A11/2019/A11.2019.12096.jpg 31 05 2001
111201912362@mhs.dinus.ac.id|MUHAMMAD IRKHAM HIDAYAT|A11.2019.12362|http://mahasiswa.dinus.ac.id/images/foto/A/A11/2019/A11.2019.12362.jpg 11 10 2001
111201911935@mhs.dinus.ac.id|DEWA SINAR SURYA|A11.2019.11935|http://mahasiswa.dinus.ac.id/images/foto/A/A11/2019/A11.2019.11935.jpg 05 02 2001
111201911817@mhs.dinus.ac.id|IVAN NOVA ARDIANSYAH|A11.2019.11817|http://mahasiswa.dinus.ac.id/images/foto/A/A11/2019/A11.2019.11817.jpg 24 11 2000
111201912173@mhs.dinus.ac.id|DIDIEK TRISATYA|A11.2019.12173|http://mahasiswa.dinus.ac.id/images/foto/A/A11/2019/A11.2019.12173.jpg 01 10 2001
111201912253@mhs.dinus.ac.id|ARIF RIZALDI|A11.2019.12253|http://mahasiswa.dinus.ac.id/images/foto/A/A11/2019/A11.2019.12253.jpg 13 06 2001
111201912287@mhs.dinus.ac.id|MOHAMMAD LUKMAN HAKIM|A11.2019.12287|http://mahasiswa.dinus.ac.id/images/foto/A/A11/2019/A11.2019.12287.jpg 28 01 2000
111201912179@mhs.dinus.ac.id|FRADANAN PUTRA FAJAR YUDA PRATAMA|A11.2019.12179|http://mahasiswa.dinus.ac.id/images/foto/A/A11/2019/A11.2019.12179.jpg 25 06 2001
111201912167@mhs.dinus.ac.id|ALDHIYA ROZAK|A11.2019.12167|http://mahasiswa.dinus.ac.id/images/foto/A/A11/2019/A11.2019.12167.jpg 21 06 2001"""
	# data=""
	hasil = list()
	for x in data.split("\n"):
		d = x.split("|")
		dd = d[3].split(" ")
		hasil.append([d[1].strip(),d[0].strip(),d[2].strip(),dd[0],f"{dd[1]}/{dd[2]}/{dd[3]}"])

	connection = sqlite3.connect("doscom.db")
	crud_query = "INSERT INTO members(name,email,nim,photo,date_of_birth) VALUES(?,?,?,?,?);"
	cursor = connection.cursor()

	for x in hasil:
		cursor.execute(crud_query,x)

	connection.commit()
	cursor.close()
	connection.close()
if __name__ == "__main__":
	setBirth()