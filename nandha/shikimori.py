
from nandha import shiki
from nandha.database import set_chat_mode, get_chats, get_chat_mode
from pyrogram import filters, types, enums

import requests
import config


def admin_only(func):
     async def wrapped(client, message):
         user_id = message.from_user.id
         chat_id = message.chat.id
         if message.chat.type in (enums.ChatType.PRIVATE, enums.ChatType.BOT):
               return await func(client, message)
         else:
            user = await client.get_chat_member(chat_id, user_id)
            if user.privileges:
                 return await func(client, message)



@shiki.on_message(filters.text, group=1)
async def shiki_reply(client, message):

    
    reply = message.reply_to_message
  
    if (
         not message.from_user.is_bot
         and reply 
         and reply.from_user.id == config.shiki_id
    ):
  
        chat_id = message.chat.id
        name = message.from_user.first_name

        prompt = (
          f"{name}: {message.text}"
        )
        api = f'http://apis-awesome-tofu.koyeb.app/api/sakura_ai/continue?chat_id=DdsFW8n&prompt={prompt}'
        response = requests.get(api).json()
        try:
          reply = response['reply']
        except Exception as e:
             print(name, e)
        return await message.reply(
             text=reply, quote=True)
        
        

    

                  


@shiki.on_message(filters.command('shiki', prefixes=['.']))
@admin_only
async def shiki(client, message):
  
      chat_id = message.chat.id

      modes = {
          'on': True,
          'off': False
      }
      if len(message.text.split()) == 2 and message.text.split()[1] in list(modes.keys()):
           key = message.text.split()[1]
           mode = modes[key]
           set_chat_mode(chat_id, mode)
           mode = get_chat_mode(chat_id)
           chatname = message.chat.title if message.chat else message.from_user.first_name + ' Chat'
           return await message.reply(
              f'**Shikimori Assistant {mode} in {chatname}.**')
      else:
         return message.reply(
            'Maybe something you did wrong, Example: `.shiki on|off`')
 
           
           
      



