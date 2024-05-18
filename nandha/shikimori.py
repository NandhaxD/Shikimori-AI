
from nandha import shiki, aiohttpsession
from nandha.database import set_chat_mode, get_chats, get_chat_mode, add_chat_sticker, get_chat_stickers
from pyrogram import filters, types, enums, errors


import config
import random
import re
import os


developers = [5015417782, 5696053228] 

SHIKI_MSG = [
     
     "Hi there i can't reply that question try asking again.",
     "Hello something went wrong idk.",
     "Hey idk why do you ask such thing",
     "Hmm... well idk.",
     "Please idk maybe ask other",
     
]

async def post_shiki(url: str, *args, **kwargs):
    async with aiohttpsession.post(url, *args, **kwargs) as resp:
        data = await resp.json()
    return data


async def ask_shiki(chat_id, user_id, name, prompt):
     payload = {
          "uid": user_id,
          "char_id": config.char_id,
          "prompt": prompt
     }
     try:
        api = config.chatbot_url
        response = await post_shiki(api, json=payload)
        reply = response['reply']
        reply = re.sub(r'User', name, reply, flags=re.IGNORECASE)
     except Exception:
           print(
                   'chat_id: ',chat_id,
                   '\nUser: ',name, 
                   '\nError: ',Exception, 
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
    name = message.sender_chat.title if message.sender_chat else message.from_user.first_name
    chatname = message.chat.title if message.chat.title else message.chat.first_name
     
    if (
       (
         message.from_user
         and not message.from_user.is_bot or 
         message.sender_chat
       )
       and message.text
       and bool(re.search(pattern='shiki|shikimori|@ShikimoriAI', string=message.text, flags=re.IGNORECASE))
    ):
        
        is_shiki = get_chat_mode(chat_id, chatname)
        if not is_shiki:
             return
             
        await shiki.send_chat_action(
               chat_id=chat_id, action=enums.ChatAction.TYPING)
         
        reply = await ask_shiki(
               chat_id, message.from_user.id, name, message.text
        )
            
        return await message.reply_text(
              text=reply, quote=True)        
  
    elif (
         (
           message.from_user 
           and not message.from_user.is_bot or
           message.sender_chat
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
                  add_chat_sticker( 
                       chat_id=chat_id, sticker_id=message.sticker.file_id
                  )
             try:
                 stickers = get_chat_stickers(chat_id)
                 return await message.reply_sticker(
                     sticker=random.choice(stickers), quote=True)
             except Exception as e:
                   print(chat_id, name, e)
             return
             
        
        await shiki.send_chat_action(
               chat_id=chat_id, action=enums.ChatAction.TYPING)
         
        reply = await ask_shiki(
               chat_id, message.from_user.id, name, message.text
        )
        
        return await message.reply(
             text=reply, quote=True)
        
    elif (
         (
           message.from_user 
           and not message.from_user.is_bot or
           message.sender_chat
         )
         and message.chat.type == enums.ChatType.PRIVATE
     
    ):
        if message.sticker or message.animation:
             if message.sticker:
                  add_chat_sticker( 
                       chat_id=chat_id, sticker_id=message.sticker.file_id
                  )
             try:
                 stickers = get_chat_stickers(chat_id)
                 return await message.reply_sticker(
                     sticker=random.choice(stickers), quote=True)
             except Exception as e:
                   print(chat_id, name, e)
             return
             
        

        await shiki.send_chat_action(
               chat_id=chat_id, action=enums.ChatAction.TYPING)
         
        reply = await ask_shiki(
              chat_id, message.from_user.id, name, message.text
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
 


@shiki.on_message((filters.me|filters.user(developers)) & filters.command('chats', prefixes=['.', '?']))
async def get_shiki_chats(client, message):
       chats = get_chats()[1]

       
       text = '❤️ Shiki Chats: {}\n'
       for i, chat in enumerate(chats):
           chatname, chat_id = next(iter(chat.items()))
           text += f'{i+1}, {chatname} - (`{chat_id}`)\n'
            
       path = 'ShikiChats.txt'
       with open(path, 'wb') as file:
           file.write(text.format(len(chats)))
            
       await message.reply_document(
            document=path, quote=True)
       os.remove(path)
       
                  
      
