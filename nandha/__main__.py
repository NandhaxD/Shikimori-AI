from nandha import shiki

import pyrogram
import asyncio



async def client():
      await shiki.start()
      await pyrogram.idle()
      return await shiki.send_message(
          chat_id='me', text='Hello, Shiki Restarted!')


if __name__ == '__main__':
    asyncio.run(client())
      
