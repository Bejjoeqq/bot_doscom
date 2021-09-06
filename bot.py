from sql import select,insert_event,insert_state,update_present,insert_save,insert_admin
from gmail import send_gmail
import telebot,threading,datetime,time,random,re

#config
config = {
	"local" : {
		"grup_id" : int_testing_grup,
		"token" : str_testing_token,
		"time" : 0,
		"db_credentials" : ["email","password"], #set credentials
		"db_send_email" : "test_members",
		"engine" : "local"
	},
	"deploy" : {
		"grup_id" : -1001206779016, #grup doscom
		"token" : str_token,
		"time" : 7,
		"db_credentials" : ["email","password"], #set credentials
		"db_send_email" : "members",
		"engine" : "deploy"
	}
}
var_global = config["deploy"] #set the main config

bot = telebot.TeleBot(token=var_global["token"],threaded=False)

@bot.message_handler(content_types=["new_chat_members"])
def newMem(message):
	if message.json["new_chat_member"]["username"].lower() == "doscom_bot":
		print(message.chat.id)
		bot.send_message(message.chat.id, "Hai Semuanya...")
	else:
		bot.send_message(message.chat.id, f"Halo Selamat Bergabung {message.json['new_chat_member']['first_name']}")

@bot.message_handler(commands=["start"])
def welcome(message):
	teks = f"Halo ini bot DOSCOM"
	bot.send_message(message.chat.id,teks)

@bot.message_handler(commands=["add"])
def add(message):
	if message.from_user.id == 948159175: #sementara hardcode add belum melalui role
		insert_admin(message.text.split(" ")[1])
		bot.send_message(message.chat.id,"Sukses")

#soon (delete an storages or an events via role)
@bot.message_handler(commands=["delete"])
def delete(message):
	pass

@bot.message_handler(commands=["save"])
def save(message):
	if message.chat.id == var_global["grup_id"] or message.chat.id == 948159175:
		if message.text.lower().strip()!="/save":
			msg = message.text.replace("/save","").strip()
			url = re.search("(?P<url>https?://[^\s]+)", msg).group("url")
			msg = msg.replace(url,"")
			title = msg.split("\n")[0]
			msg = msg.replace(title,"").strip()

			insert_save(title,msg,url)

			bot.send_message(message.chat.id,"Disimpan")
		else:
			teks = f"""# /save
## judul
## deskripsi dan url

# example
/save 
Link Google
Halaman utama google bisa di
buka melalui https://www.google.com/
Terima kasih
"""
			bot.send_message(message.chat.id,teks,disable_web_page_preview=True)

@bot.message_handler(commands=["get"])
def get(message):
	if message.text.lower().strip()!="/get":
		command = message.text.lower().strip().split(" ")
		if command[1] == "event":
			result = select(q=f"SELECT sum(present),sum(not_present) FROM events_members WHERE event_id={command[2]}")[0]
			teks = f"""Prediksi event #{command[2]}
Hadir : {result[0]}
Tidak Hadir : {result[1]}
"""
			bot.send_message(message.chat.id,teks)
		elif command[1] == "save":
			ids = 0
			if len(command)>2:
				ids = command[2]
			result = select(q=f"select title,description,url from storages where id='{ids}'")
			if result:
				teks = f"{result[0][0].title()}\n\n{result[0][1]}\n{result[0][2]}"
				bot.send_message(message.chat.id,teks,disable_web_page_preview=True)
			else:
				result = select(q="select title from storages")
				teks = ""
				for y,x in enumerate(result):
					teks += f"#{y+1}. {x[0].title()}\n"
				bot.send_message(message.chat.id,teks)
		elif command[1] == "time":
			bot.send_message(message.chat.id,str(datetime.datetime.now() + datetime.timedelta(hours=var_global["time"])))
	else:
		teks = f"""# /get event id
# /get save
# /get save id

# example
/get event 3

/get save

/get save 3
"""
		bot.send_message(message.chat.id,teks)

@bot.message_handler(content_types=["text", "photo"])
def set(message):
	if message.chat.id == var_global["grup_id"] or message.chat.id == 948159175:
		result = select(q=f"select role from admins where username='{message.from_user.username}'") #belum diterapkan hingga role
		if result:
			is_photo = False
			if message.content_type == "photo":
				msg = message.caption
				is_photo = True
			else:
				msg = message.text
			if msg:
				if "/set" == msg.lower().strip()[:4]:
					if msg.lower().strip()!="/set":
						m1 = msg.replace("/set","").strip()
						m2 = m1.split("\n")
						try:
							judul = m2[0]
							formats = ["%H:%M %d/%m/%Y","%H.%M %d/%m/%Y","%H:%M %d-%m-%Y","%H.%M %d-%m-%Y","%H %M %d %m %Y"]
							tanggal = False
							for x in formats:
								tanggal = iserror(datetime.datetime.strptime,m2[1],x)
								if tanggal:
									break
							if not tanggal:
								bot.send_message(message.chat.id,"Format tanggal salah")
							else:
								desc = "-"
								if len(m2)>2:
									desc = "\n".join(m2[2:])

								photos = "-"
								if is_photo:
									file = message.photo[-1]
									photos = file.file_id

								ids = insert_event(judul,tanggal,desc,photos)

								markup = telebot.types.InlineKeyboardMarkup()
								btnYes = telebot.types.InlineKeyboardButton("Yes", callback_data=f'{ids} yes')
								btnNo = telebot.types.InlineKeyboardButton("No", callback_data=f'{ids} no')
								markup.row(btnYes,btnNo)

								if is_photo:
									bot.send_photo(message.chat.id,photos)
									pinned = bot.send_message(message.chat.id, getMessageEvent(judul,tanggal,desc,f"#{ids} - "), reply_markup=markup)
								else:
									pinned = bot.send_message(message.chat.id, getMessageEvent(judul,tanggal,desc,f"#{ids} - "), reply_markup=markup)

								bot.pin_chat_message(message.chat.id,pinned.message_id)
								send_gmail(judul,getMessageEvent(judul,tanggal,desc),var_global["db_credentials"],var_global["db_send_email"])

						except Exception as e:
							bot.send_message(message.chat.id,"Format salah, lihat contoh penggunaan /set.")
					else:
						teks = f"""# /set
## judul
## tanggal(h.m dd/mm/yyyy)
## deskripsi 
## .
## .
## . 
## (opsional)
## kirim dengan foto untuk menambahkan foto (opsional)

# example
/set 
Rapat Pyshare ke 3
23.59 28/12/2021
Jangan lupa rapat ya,
sampai ketemu nanti.
"""
						bot.send_message(message.chat.id,teks)


@bot.callback_query_handler(func=lambda call: call.data.split(" ")[1] == 'yes')
def cb_yes(call):
	ids = call.data.split(" ")[0]
	result = select(q=f"select telegram_id from events_members where event_id={ids} and telegram_id={call.from_user.id}")
	if not result:
		insert_state(call.from_user.id, ids, call.from_user.first_name)

	update_present(ids,call.from_user.id,1,0)
	bot.answer_callback_query(call.id, "Answer is Yes")


@bot.callback_query_handler(func=lambda call: call.data.split(" ")[1] == 'no')
def cb_no(call):
	ids = call.data.split(" ")[0]
	result = select(q=f"select telegram_id from events_members where event_id={ids} and telegram_id={call.from_user.id}")
	if not result:
		insert_state(call.from_user.id, ids, call.from_user.first_name)

	update_present(ids,call.from_user.id,0,1)
	bot.answer_callback_query(call.id, "Answer is No")

def getEvents():
	hasil = select(q="select name,dates,description,photo from events")

def iserror(func, value, method):
    try:
        return func(value, method).strftime("%H.%M %d/%m/%Y")
    except Exception:
        return False

def status_deploy():
	while True:
		try:
			bot.polling()
		except Exception as e:
			file1 = open("logs.txt","a")
			file1.write(str(e)+"\n\n")
			file1.close()
			bot.stop_polling()

def status_local():
	bot.polling()

def getBulan(x):
	bulan = {
		'01' : 'Januari',
		'02' : 'Februari',
		'03' :'Maret',
		'04' : 'April',
		'05' : 'Mei',
		'06' : 'Juni',
		'07' : 'Juli',
		'08' : 'Agustus',
		'09' : 'September',
		'10' : 'Oktober',
		'11' : 'November',
		'12' : 'Desember'
	}
	return bulan[x]

def getMessageEvent(judul,tanggal,description,ids=""):
	jam = tanggal.split(" ")[0]
	tanggal = tanggal.split(" ")[1].split("/")
	pesan = f"""{ids}{judul.title()}

Tanggal : {tanggal[0]} {getBulan(tanggal[1])} {tanggal[2]}
Pukul     : {jam} WIB - Selesai
Meet      : http://g.co/meet/{judul.lower().strip().replace(" ","-")}
(Gunakan akun mahasiswa)

{description}
"""
	return pesan

def list_word(x,y=""):
	words = [
		f"Selamat ulang tahun {x}{y}! Semoga kamu senantiasa diberi kemudahan oleh Tuhan dalam menjalani setiap urusan dan selalu menjadi pribadi yang lebih baik dari sebelumnya. Amin.",
		f"Selamat ulang tahun {x}{y}! Tambah umur berarti harus tambah dewasa juga. Semoga Tuhan memberikanmu kesuksesan dan kelancaran rezeki.",
		f"Selamat bertambah usia {x}{y}! Semoga diberi umur panjang, sehat selalu, dan selalu tetap semangat menjalani hidup karena kesuksesan di masa depan ditentukan oleh setiap usaha hari ini.",
		f"Hei, Selamat ulang tahun {x}{y}, ya! Semoga kuliahnya diberikan kelancaran dan rezekinya diperbanyak oleh Tuhan.",
		f"Happy birthday {x}{y}! Semoga apa yang kamu semogakan tidak hanya menjadi sekadar semoga, tapi secepatnya terwujudkan!"
	]
	return random.choice(words)

def timecheck():
	while True:
		today = datetime.datetime.now() + datetime.timedelta(hours=var_global["time"])
		print(today.hour, today.minute, today.second)
		if today.hour==0 and today.minute==0:
			time.sleep(5)
			result = select(q="select date_of_birth,name,username,photo from members")
			for x in result:
				if today.strftime("%d/%m")=="/".join(x[0].split("/")[:2]):
					print("hbd")
					bot.send_photo(var_global["grup_id"], x[3])
					bot.send_message(var_global["grup_id"],list_word(x[1]))
			time.sleep(5)

		if today.second==0:
			result = select(q="select name,dates,description,photo from events")
			for x in result:
				jam = x[1].split(" ")[0].split(".")
				mins = today - datetime.timedelta(minutes=30)

				if today.strftime("%d/%m/%Y")==x[1].split(" ")[1] and (today.hour==int(jam[0]) and mins.minute==int(jam[1])):
					# print("masuk")
					if x[3]!="-":
						bot.send_photo(var_global["grup_id"], x[3])
						bot.send_message(var_global["grup_id"], getMessageEvent(x[0],x[1],x[2]))
						bot.send_message(var_global["grup_id"], "30 Menit lagi, jangan lupa ya !")
					else:
						bot.send_message(var_global["grup_id"], getMessageEvent(x[0],x[1],x[2]))
						bot.send_message(var_global["grup_id"], "30 Menit lagi, jangan lupa ya !")

		time.sleep(1)

def start():
	if var_global["engine"]=="local":
		status_local()
	else:
		status_deploy()

if __name__ == "__main__":
	t1 = threading.Thread(target=start)
	t2 = threading.Thread(target=timecheck)

	t1.start()
	t2.start()