from pyrogram import Client, filters 
 from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup 
 import youtube_dl 
 from youtube_search import YoutubeSearch 
 import requests 
 import os 
 from config import Config 
  
 bot = Client( 
     'YouTubeSongDownloader', 
     bot_token=Config.BOT_TOKEN, 
     api_id=Config.API_ID, 
     api_hash=Config.API_HASH 
 ) 
  
 ## Extra Fns ------------------------------- 
  
 # Convert hh:mm:ss to seconds 
 def time_to_seconds(time): 
     stringt = str(time) 
     return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':')))) 
  
  
 ## Commands -------------------------------- 
 @bot.on_message(filters.command(['start'])) 
 def start(client, message): 
     start_text = '''👋 Welcome @{username}, 
  
 I am a YouTube Song Downloader Bot [🎶](https://telegra.ph/file/34e13355f6753772d4e3f.mp4). 
  
 Send /s Song Name to download a song. 
  
 Eg. /s Faded 
  
 𝐅𝐨𝐥𝐥𝐨𝐰 👉 @Thealphabotz 
  
 𝐒𝐮𝐩𝐩𝐨𝐫𝐭 👉 https://t.me/+n5UitRf-oDpmNzM1''' 
  
     bot.send_message( 
         chat_id=message.chat.id, 
         text=start_text.format(username=message.from_user.username), 
         reply_markup=InlineKeyboardMarkup( 
             [ 
                 [ 
                     InlineKeyboardButton('Updates 👬', url='https://t.me/Thealphabotz'), 
                     InlineKeyboardButton('Support 🤗', url='https://t.me/https://t.me/+n5UitRf-oDpmNzM1') 
                 ] 
             ] 
         ), 
         disable_web_page_preview=True 
     ) 
  
 @bot.on_message(filters.command(['s'])) 
 def download_song(client, message): 
     query = ' '.join(message.command[1:]) 
     print(query) 
     m = message.reply('🔎 Searching the song...') 
     ydl_opts = {"format": "bestaudio[ext=m4a]"} 
     try: 
         results = [] 
         count = 0 
         while len(results) == 0 and count < 6: 
             if count > 0: 
                 time.sleep(1) 
             results = YoutubeSearch(query, max_results=1).to_dict() 
             count += 1 
         try: 
             link = f"https://youtube.com{results[0]['url_suffix']}" 
             title = results[0]["title"] 
             thumbnail = results[0]["thumbnails"][0] 
             duration = results[0]["duration"] 
             views = results[0]["views"] 
             thumb_name = f'thumb{message.message_id}.jpg' 
             thumb = requests.get(thumbnail, allow_redirects=True) 
             open(thumb_name, 'wb').write(thumb.content) 
  
         except Exception as e: 
             print(e) 
             m.edit('Something went wrong. Try searching a little differently.') 
             return 
     except Exception as e: 
         m.edit("Something went wrong. Try another keyword or make sure your input is correct.") 
         print(str(e)) 
         return 
     m.edit("🔎 Finding a song for you... [🚀](https://telegra.ph/file/60b0489093120e762861f.mp4)") 
     try: 
         with youtube_dl.YoutubeDL(ydl_opts) as ydl: 
             info_dict = ydl.extract_info(link, download=False) 
             audio_file = ydl.prepare_filename(info_dict) 
             ydl.process_info(info_dict) 
         rep = f'🎧 Title: [{title[:35]}]({link})\n⏳ Duration: {duration}\n🎬 Source: [Youtube](https://youtu.be/3pN0W4KzzNY)\n👁‍🗨 Views: {views}\n\n💌 A Bot By: @adarsh2626' 
     except Exception as e: 
         m.edit("Download failed. Try searching with different keywords.") 
         print(str(e)) 
         return 
     m.edit(rep, disable_web_page_preview=True) 
  
  
 bot.run()