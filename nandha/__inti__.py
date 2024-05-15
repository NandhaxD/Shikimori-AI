

import pyrogram
import config
import pymongo


app = pyrogram.Client(
   name=config.name,
   api_id=config.api_id,
   api_hash=config.api_hash,
   session_string=config.session,
   plugins=dict(root='nandha')
)

connect_db = pymongo.MongoClient(config.db_url)
db = connect_db['SHIKI']
