import discord
from hihiiro.core.bot import DBot
import os
TOKEN=os.environ["BOT_TOKEN"]
INTENTS = discord.Intents.all()
#INTENTS.members = True

# データベースに接続
import psycopg2
conn = psycopg2.connect(host='my_postgres',
                        port='5432',
                        dbname='pokemon',
                        user=os.environ["POSTGRES_USER"],
                        password=os.environ["POSTGRES_PASSWORD"],
                        )

cur=conn.cursor()
cur.execute("select * from status")
res=cur.fetchone()
print(res)
cur.close()
conn.close()

DBot(INTENTS).run(TOKEN)
