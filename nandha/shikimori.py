

from sakura import Client
from nandha import shiki, aiohttpsession
from nandha.database import *
from pyrogram import filters, types, enums, errors


import config
import random
import re
import requests
import os

developers = [5015417782, 5696053228] 


SHIKI_MSG = [
     
     "Hi there i can't reply that question try asking again.",
     "Hello something went wrong idk.",
     "Hey idk why do you ask such thing",
     "Hmm... well idk.",
     "Please idk maybe ask other",
     
]




content= requests.get('https://graph.org/file/bfa6deec0fa5a9f05255d.jpg').content
shiki_photo = 'shiki.jpeg'
with open(shiki_photo, 'wb') as f:
     f.write(content)


Shiki= Client(
    username = config.username,
    password = config.password,
    mongo = config.db_url
)
     

async def shiki_react(message):
     try:
       await message.react(
            random.choice(
                 ['🥰', '❤️', '😁', '🗿']
            )
       )
     except:
          pass
         

async def ask_shiki(chat_id, user_id, name, prompt):
     try:
        response = Shiki.sendMessage(
             user_id, config.char_id, prompt
        )
        reply = response['reply']
        reply = re.sub(r'\bUser\b(?!s)', name, reply, flags=re.IGNORECASE)
     except Exception:
           print(
                   'chat_id: ',chat_id,
                   '\nUser: ', name, 
                   '\nError: ', str(Exception), 
                   '\nPrompt: ', prompt
               )
           reply = random.choice(SHIKI_MSG)
           
     return reply




def admin_only(func):
     async def wrapped(client, message):
         user_id = message.from_user.id
         chat_id = message.chat.id
         if message.chat.type in (enums.ChatType.PRIVATE, enums.ChatType.BOT):
               return await func(client, message)
         else:
            try:
              user = await client.get_chat_member(chat_id, user_id)
            except errors.ChatAdminRequired:
                 return await message.reply_animation(
                      animation='https://graph.org/file/ab7d69f435faf4e8235c8.mp4',
                      text='**Hello, Make me Admin to activate & deactivate assistant 🥺🥰**'
                 )
            if user.privileges or user_id == config.shiki_id or user_id in developers:
                 return await func(client, message)
     return wrapped
              



@shiki.on_message((filters.text | filters.sticker | filters.animation ), group=2)
async def shiki_reply(client, message):

    
    reply = message.reply_to_message
    chat_id = message.chat.id
    user = message.sender_chat if message.sender_chat else message.from_user
    name = message.sender_chat.title if message.sender_chat else message.from_user.first_name
    chatname = message.chat.title if message.chat.title else message.chat.first_name
     
    if (
    (
        (message.from_user and (not message.from_user.is_bot and message.from_user.id != config.shiki_id))
        or message.sender_chat
    )
    and message.text
    and bool(re.search('shiki|shikimori|@shikimoriai', string=message.text, flags=re.IGNORECASE))
    ):
        
        is_shiki = get_chat_mode(chat_id, chatname)
        if not is_shiki:
             return
             
        await shiki.send_chat_action(
               chat_id=chat_id, action=enums.ChatAction.TYPING)
        
        await shiki_react(message)
         
        reply = await ask_shiki(
               chat_id, user.id, name, message.text
        )
            
        return await message.reply_text(
              text=reply, quote=True)        
  
    elif (
    (
       (message.from_user and (not message.from_user.is_bot and message.from_user.id != config.shiki_id)) 
    or message.sender_chat
    )
  and reply 
  and reply.from_user 
  and reply.from_user.id == config.shiki_id
  and message.chat.type != enums.ChatType.PRIVATE
    ):  
        
        is_shiki = get_chat_mode(chat_id, chatname)
        if not is_shiki:
             return
        
        if message.sticker or message.animation:
             if message.sticker:
                  if not message.sticker.file_id in get_all_stickers():
                     add_chat_sticker( 
                       chat_id=chat_id, sticker_id=message.sticker.file_id
                  )
             try:
                 #get_chat_stickers(chat_id) alos exsit
                 stickers = get_all_stickers()
                 return await message.reply_sticker(
                     sticker=random.choice(stickers), quote=True)
             except Exception as e:
                   print(chat_id, name, e)
             return
             
        
        await shiki.send_chat_action(
               chat_id=chat_id, action=enums.ChatAction.TYPING)
         
        await shiki_react(message)
         
        reply = await ask_shiki(
               chat_id, user.id, name, message.text
        )
        
        return await message.reply(
             text=reply, quote=True)
        
    elif (
    (
       (message.from_user and (not message.from_user.is_bot and message.from_user.id != config.shiki_id)) 
    or message.sender_chat
    )
  and message.chat.type == enums.ChatType.PRIVATE
    ):  
        is_shiki = get_chat_mode(chat_id, chatname)
        if not is_shiki:
             return
             
        if message.sticker or message.animation:
             if message.sticker:
                  add_chat_sticker( 
                       chat_id=chat_id, sticker_id=message.sticker.file_id
                  )
             try:
                 stickers = get_all_stickers()
                 return await message.reply_sticker(
                     sticker=random.choice(stickers), quote=True)
             except Exception as e:
                   print(chat_id, name, e)
             return
             
        

        await shiki.send_chat_action(
               chat_id=chat_id, action=enums.ChatAction.TYPING)

        await shiki_react(message)
         
        reply = await ask_shiki(
              chat_id, user.id, name, message.text
        )
        
        return await message.reply(
             text=reply, quote=True)
        
         

@shiki.on_message(filters.command('shiki', prefixes=['.', '?']))
@admin_only
async def shiki_mode(client, message):
  
      chat_id = message.chat.id
      
      modes = {
          'on': True,
          'off': False
      }
      if len(message.text.split()) == 2 and message.text.split()[1] in list(modes.keys()):
           key = message.text.split()[1]
           mode = modes[key]
           chatname = message.chat.title if message.chat.title else message.chat.first_name + ' Chat'
           
           set_chat_mode(
                chat_id=chat_id, 
                chatname=chatname, 
                mode=mode)
           
           mode = get_chat_mode(chat_id, chatname)
           shiki = 'off'
           for k, v in modes.items():
             if v == mode:
                shiki = k
                
                   
           return await message.reply(
              f'**Shikimori Assistant {shiki.upper()} in {chatname}.**')
      else:
         return await message.reply(
            'Maybe something you did wrong, Example: `.shiki on|off`')
 

@shiki.on_message((filters.me|filters.user(developers)) & filters.command('ss', prefixes=['.', '?']))
async def ScanSticker(shiki, message):
     m = message
     reply = m.reply_to_message
     msg = await m.reply_text(
          "✨ Finding the sticker please wait...."
     )
     if reply and reply.sticker:
           file_id = reply.sticker.file_id
           check = scan_sticker(file_id)
           if check:
               chat_id, file_id = next(iter(check.items()))
               try:       
                  info = await shiki.get_chat(chat_id)
                  name = info.title if info.title else info.mention
               except Exception as e:
                  name = None
               return await msg.edit(
f"""
👀 **Scan results**:
**Chat**: {name}
**Id**: `{chat_id}`

```
To remove sticker from the database use
> .sr chat_id sticker_id
```
"""
)
           else:
               return await msg.edit(
                "🤔 Semms like the sticker not in my database."
           )
     else:
        return await msg.edit("🐼 Reply to s sticker")



@shiki.on_message((filters.me|filters.user(developers)) & filters.command('sr', prefixes=['.', '?']))
async def RemoveSticker(shiki, message):
          m = message
          if m.command == 1:
               return await m.reply_text(
                    "Wrong usage! .sr chat_id file_id"
               )
          else:
             chat_id, sticker_id = m.command[1], m.command[2]
             await remove_sticker(int(chat_id), sticker_id)
             return await m.reply_text(
                  "🎉 Okay! I've removed sticker if sticker in my database."
             )
     

@shiki.on_message((filters.me|filters.user(developers)) & filters.command('chats', prefixes=['.', '?']))
async def get_shiki_chats(client, message):
       chats = get_chats()
       text = '❤️ Shiki Chats: {}\n'
       for i, chat in enumerate(chats[1]):
           name, chat_id, shiki = chat['name'], chat['chat_id'], chat['chat']
           text += f'{i+1}, {name} - (`{chat_id}`): {shiki}\n'
            
       shiki_docs = 'ShikiChats.txt'
       text = text.format(len(chats))
       with open(shiki_docs, 'w') as file:
           file.write(text)
           
       await message.reply_document(
            document=shiki_docs, thumb=shiki_photo, quote=True)
       os.remove(path)
       
                  
      
