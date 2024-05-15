
from nandha import shiki
import subprocess

@shiki.on_message(filters.me & filters.command('logs'))
async def logs(_, message)
  logs = subprocess.getoutput('tail logs.txt')
  return await message.reply(
    text=logs)
                        

                          
