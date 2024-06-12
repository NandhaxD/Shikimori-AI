from nandha import shiki

import pyrogram
import asyncio


async def keep_online():
    while True:
        await shiki.invoke(pyrogram.raw.functions.account.UpdateStatus(offline=False))
        await asyncio.sleep(7)

async def client():
      await shiki.start()
      await keep_online()
      await pyrogram.idle()
      
      return await shiki.send_message(
          chat_id='me', text='Hello, Shiki Restarted!')


if __name__ == '__main__':
    shiki.loop.run_until_complete(client())
      
