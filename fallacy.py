import discord
import yt_dlp
import urllib
import re
import asyncio
import ffmpeg

class MyClient(discord.Client):

    def getSong(self, searchTerm):
        searchUrl = "https://www.youtube.com/results?search_query=" + searchTerm
        searchUrl = searchUrl.replace(" ", "-")
        html = urllib.request.urlopen(searchUrl)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        songUrl = "https://www.youtube.com/watch?v="


        ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'LMAO??/songs/'+ searchTerm + ".mp3",

        'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        
            print(songUrl + str(video_ids[0]))
            _ = ydl.extract_info(songUrl + video_ids[0], download=True)
            
    
    async def on_ready(self):
        print("Logged on as {0}!".format(self.user))

    async def on_message(self, message):
        print("Message from {0.author}: {0.content}".format(message))
        if '!p ' in message.content:
            content = message.content.replace("!p ", "")
            print(content)
            user=message.author
            voice_channel=user.voice.channel
            channel=None
            if voice_channel!= None:
                # grab user's voice channel
                channel=voice_channel.name
                await message.channel.send('Alright, playing ' + "'" + content + "'" + ' in ' + channel + " in like 5 secs!")
                vc = await voice_channel.connect()
                self.getSong(content)
                discord.opus.load_opus('/usr/local/homebrew/Cellar/opus/1.3.1/lib/libopus.dylib')
                vc.play(discord.FFmpegPCMAudio(executable="/opt/homebrew/Cellar/ffmpeg/5.1.2_1/bin/ffmpeg", source="LMAO??/songs/" + content + ".mp3"))

                while vc.is_playing():
                    await asyncio.sleep(1)

            else:
                await message.channel.send('Get in a vc bro')
    
  


client = MyClient(intents=discord.Intents.all())

client.run('MTA1OTk0NTQwMjA3MTI1NzExOA.GyP_F3.CKR5apmP_a13L9BtRlj5trRT1Pcn9i-5QVJsKg')
