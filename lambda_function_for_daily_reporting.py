#apo user id =5222103467 abla userid=6549150812

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



    try:
                       today=(datetime.utcnow()+timedelta(hours=3)).strftime("%d%h%y")
                       val = (today)
                       print(today)

                       # total sales
                       sql_for_total_sales =f"SELECT sum(toplam_fiyat) FROM YOUR TABLE NAME where date_day= %s;"

                       cursor.execute(sql_for_total_sales,val)

                       total_sales=cursor.fetchall()[0][0]


                      #total kar

                       sql_for_kar = "SELECT sum(kar) FROM YOUR TABLE NAME where date_day= %s;"
                       cursor.execute(sql_for_kar,val)
                       total_kar= cursor.fetchall()[0][0]

                       cnx.commit()


                       await client.send_message(my_channel,today + " :" + "  toplam ciro: " + str(total_sales) + "  total kar" +str(total_kar))




    except Exception as e:
            print(e)



def lambda_handler(event, context):
    with client:
        client.loop.run_until_complete(main())
