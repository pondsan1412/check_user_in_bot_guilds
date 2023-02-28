import discord
from discord.ext import commands,tasks
import os
from dotenv import load_dotenv
import requests
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!",intents=intents)

@bot.event #เมื่อมีเหตการ บอทออนไลน์ บอทจะ ปริ้น logged in as บลาๆ
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
   
@bot.command()
async def voice_users(ctx):
    # ดึง guilds ทั้งหมดที่ bot เชื่อมต่ออยู่
    guilds = bot.guilds
    
    # สร้าง dict สำหรับเก็บจำนวนผู้ใช้ที่เชื่อมต่อในแต่ละ voice channel และชื่อผู้ใช้ในแต่ละ voice channel
    voice_users_dict = {}
    voice_users_names = {}
    
    # วน loop เช็ค voice state ของผู้ใช้ทั้งหมดใน guild
    for guild in guilds:
        for member in guild.members:
            voice_state = member.voice
            
            # ถ้าเชื่อมต่ออยู่ใน voice channel
            if voice_state and voice_state.channel:
                channel_name = voice_state.channel.mention
                
                # เพิ่มจำนวนผู้ใช้ใน voice channel นั้นๆ
                if channel_name not in voice_users_dict:
                    voice_users_dict[channel_name] = 1
                    voice_users_names[channel_name] = [member.mention]
                else:
                    voice_users_dict[channel_name] += 1
                    voice_users_names[channel_name].append(member.mention)
    
    # สร้างข้อความที่จะส่งกลับ
    message = f"ผู้ใช้ที่เชื่อมต่อใน voice channel ทั้งหมด ที่บอทอาศัยอยู่:\n"
    for channel_name, user_count in voice_users_dict.items():
        message += f"{channel_name}: {user_count} คน ({', '.join(voice_users_names[channel_name])})\n"
    
    # ส่งข้อความกลับไปยัง channel ที่ใช้งานอยู่
    await ctx.send(message)



    
load_dotenv()
token = os.getenv("TOKEN2") #ตรงส่วนนี้ต้องกำหนดตัวแปรข้างใน env
bot.run(token) #ตัวแปร token จะเก็บค่า str ของ token เอาไว้ใน ไฟล์ env

