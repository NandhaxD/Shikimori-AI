

import pyrogram
import config
import pymongo
import logging
import aiohttp


aiohttpsession = aiohttp.ClientSession() # session

FORMAT = f"[{config.name}] %(message)s"
logging.basicConfig(level=logging.INFO, handlers=[logging.FileHandler('logs.txt'),
              logging.StreamHandler()], format=FORMAT)



shiki = pyrogram.Client(
   name=config.name,
   api_id=config.api_id,
   api_hash=config.api_hash,
   session_string=config.session,
   plugins=dict(root='nandha')
)

connect_db = pymongo.MongoClient(config.db_url)
db = connect_db['SHIKI']
