

import configparser
import pymysql


from datetime import  timedelta


import uuid

endpoint = 'YOUR MYSQL ENDPOINT'
username = 'YOUR USER NAME'
port = 3306
password = 'YOUR PASSWORD'
database = "YOUR DATABASE NAME"

cnx = pymysql.connect(user=username, password=password,
                      host=endpoint)

cursor = cnx.cursor()



from telethon.sync import TelegramClient

from datetime import date, datetime
from telethon.sessions import StringSession

from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.types import (
    PeerChannel
)
import json



# some functions to parse json date
class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        if isinstance(o, bytes):
            return list(o)

        return json.JSONEncoder.default(self, o)


# Reading Configs
config = configparser.ConfigParser()
config.read("config.ini")

# Setting configuration values
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']

api_hash = str(api_hash)

phone = config['Telegram']['phone']
username = config['Telegram']['username']

# Create the client and connect


string1 = "YOUR STRING SESSION"
with TelegramClient(StringSession(string1), int(api_id), api_hash) as client:
    string = client.session.save()




async def main():
    #  user_input_channel = input('enter entity(telegram URL or entity id):')
    user_input_channel = "YOUR TELEGRAM CHANNEL INVITE LINK"

    if user_input_channel.isdigit():
        entity = PeerChannel(int(user_input_channel))
    else:
        entity = user_input_channel

    my_channel = await client.get_entity(entity)

    offset_id = 0
    limit = 100
    all_messages = []

    total_count_limit = 0

    while True:

        history = await client(GetHistoryRequest(
            peer=my_channel,
            offset_id=offset_id,
            offset_date=None,
            add_offset=0,
            limit=limit,
            max_id=0,
            min_id=0,
            hash=0
        ))
        if not history.messages:
            break
        messages = history.messages
        for message in messages:
            all_messages.append(message.to_dict())
        offset_id = messages[len(messages) - 1].id
        total_messages = len(all_messages)
        if total_count_limit != 0 and total_messages >= total_count_limit:
            break




    for i in range(len(all_messages)):

      if all_messages.__getitem__(i)["from_id"]["user_id"] =='YOUR USER ID':

        try:
               print((all_messages.__getitem__(i)["date"] + timedelta(hours=3)).strftime("%d%h%y"))

               if (all_messages.__getitem__(i)["date"] + timedelta(hours=3)).strftime("%d%h%y") ==(datetime.utcnow()+timedelta(hours=3)).strftime("%d%h%y"):
                   last_message=all_messages.__getitem__(i)["message"]
                   last_message_splited = last_message.split("-")


                   marka = last_message_splited[0]
                   urun = last_message_splited[1]
                   aciklama = last_message_splited[2]
                   adet = last_message_splited[3]
                   satis_fiyati = last_message_splited[5]
                   alis_fiyati = last_message_splited[4]
                   kart_nakit = last_message_splited[6]
                   toplam_fiyat = int(last_message_splited[3]) * int(last_message_splited[5])
                   kar = int(toplam_fiyat) - (int(alis_fiyati)*int(adet))


                   last_date_day = (all_messages.__getitem__(i)["date"] + timedelta(hours=3)).strftime("%d%h%y")
                   last_date_hour = (all_messages.__getitem__(i)["date"] + timedelta(hours=3)).strftime("%d%h%y %H:%M")
                   tarih = last_date_day
                   tarih_saat = last_date_hour
                   print(str(uuid.uuid4()), marka, urun, aciklama, adet, satis_fiyati, alis_fiyati, toplam_fiyat,
                         kart_nakit, tarih, tarih_saat)
                   try:
                       sql = "INSERT INTO YOUR TABLE NAME (satis_id, marka, urun, aciklama, adet, alis_fiyati,satis_fiyati,toplam_fiyat,kar,date_day,date_day_hour,kart_nakit) VALUES(%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                       val = (
                       str(uuid.uuid4()), marka, urun, aciklama, adet, alis_fiyati, satis_fiyati, toplam_fiyat, kar,
                       tarih, tarih_saat, kart_nakit)
                       cursor.execute(sql, val)

                       cnx.commit()

                       print(cursor.rowcount, "was inserted.")

                   except Exception as e:
                       print(e)

        except Exception as e:
            print(e)
            await client.send_message(my_channel, 'yanlış girdiniz', reply_to=all_messages.__getitem__(i)["id"])






def lambda_handler(event, context):
    with client:
        client.loop.run_until_complete(main())
