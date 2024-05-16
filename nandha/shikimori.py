
from nandha import shiki
from nandha.database import set_chat_mode, get_chats, get_chat_mode, add_chat_sticker, get_chat_stickers
from pyrogram import filters, types, enums

import requests
import config
import random
import re


developers = [5015417782, 5696053228] 

SHIKI_MSG = [
     
     "Hi there i can't reply that question try asking again.",
     "Hello something went wrong idk.",
     "Hey idk why do you ask such thing",
     "Hmm... well idk.",
     "Please idk maybe ask other",
     "Letz talk about other idk."
     
]



def admin_only(func):
     async def wrapped(client, message):
         user_id = message.from_user.id
         chat_id = message.chat.id
         if message.chat.type in (enums.ChatType.PRIVATE, enums.ChatType.BOT):
               return await func(client, message)
         else:
            user = await client.get_chat_member(chat_id, user_id)
            
            if user.privileges or user_id == config.shiki_id:
                 return await func(client, message)
     return wrapped
              



@shiki.on_message((filters.text | filters.sticker), group=2)
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
       and bool(re.search('@ShikimoriAI', message.text, re.IGNORECASE))
    ):
        
        is_shiki = get_chat_mode(chat_id, chatname)
        if not is_shiki:
             return
        prompt = (
          f"username: {name}\n"
          f"prompt: {message.text}"
        )
         
        api = f'{config.chatbot_url}{prompt}'

        await shiki.send_chat_action(
               chat_id=chat_id, action=enums.ChatAction.TYPING)
        try:
           response = requests.get(api , timeout=15)
           reply = response.json()['reply']
   #    except requests.exceptions.Timeout:         
        except Exception as e:
             print(chat_id, name, e, message.text)
             reply = random.choice(SHIKI_MSG)
 
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
    ):
  
        

        is_shiki = get_chat_mode(chat_id, chatname)
        if not is_shiki:
             return

        if message.sticker:
             add_chat_sticker( chat_id=chat_id, sticker_id=message.sticker.file_id)
             try:
                 stickers = get_chat_stickers(chat_id)
                 return await message.reply_sticker(
                     sticker=random.choice(stickers), quote=True)
             except Exception as e:
                   print(chat_id, name, e)
             return
             
        prompt = (
          f"username: {name}\n"
          f"prompt: {message.text}"
        )
         
        api = f'{config.chatbot_url}{prompt}'

        await shiki.send_chat_action(
               chat_id=chat_id, action=enums.ChatAction.TYPING)
        try:
           response = requests.get(api , timeout=15)
           reply = response.json()['reply']
   #    except requests.exceptions.Timeout:         
        except Exception as e:
             print(chat_id, name, e, message.text)
             reply = random.choice(SHIKI_MSG)
 
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
       text = '**❤️ Shiki Chats**: {}\n'
       for i, chat in enumerate(chats):
           chatname, chat_id = next(iter(chat.items()))
           text += f'{i+1}, {chatname} - (`{chat_id}`)\n'
            
              
       return await message.reply(
            text=text.format(len(chats)), quote=True
       )
                  
      
