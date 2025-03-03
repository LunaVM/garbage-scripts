import discord
from discord.ext import commands
import os
import subprocess

# Your bot's token
TOKEN = ',,,'
OWNER_IDS = [492883063542513675, 1257791775523868735]  # List of owner IDs

# Initialize bot
intents = discord.Intents.default()
intents.members = True  # Enable member join event
bot = commands.Bot(command_prefix='!', intents=intents)

# Welcoming new users
@bot.event
async def on_member_join(member):
    await member.guild.system_channel.send(f"Welcome to the server, {member.mention}!")

# Upload file command (owner-only)
@bot.command()
async def uploadfile(ctx, *, file_path: str):
    if ctx.author.id not in OWNER_IDS:
        await ctx.send("You are not authorized to use this command.")
        return
    
    # Safety check to avoid sensitive Windows system files
    if file_path.startswith('C:\\Windows'):
        if not file_path.startswith('C:\\Windows\\Logs'):
            await ctx.send("You are not allowed to access files in C:\\Windows (except for C:\\Windows\\Logs).")
            return

    # Check if the file exists
    if os.path.exists(file_path):
        try:
            await ctx.send(f"Here's the file you requested: {file_path}", file=discord.File(file_path))
        except Exception as e:
            await ctx.send(f"An error occurred while sending the file: {str(e)}")
    else:
        await ctx.send(f"The file {file_path} does not exist.")

# Eval command (owner-only)
@bot.command()
async def eval(ctx, *, code):
    if ctx.author.id not in OWNER_IDS:
        await ctx.send("You are not authorized to use this command.")
        return
    
    try:
        # Execute code and capture the result
        result = subprocess.run(['python', '-c', code], capture_output=True, text=True)
        if result.stdout:
            await ctx.send(f"Output:\n{result.stdout}")
        if result.stderr:
            await ctx.send(f"Error:\n{result.stderr}")
    except Exception as e:
        await ctx.send(f"Error: {str(e)}")

# Localcmd command (owner-only) to run local system commands
@bot.command()
async def localcmd(ctx, *, command: str):
    if ctx.author.id not in OWNER_IDS:
        await ctx.send("You are not authorized to use this command.")
        return

    try:
        # Run the local command and capture the output
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()

        # Send the output or error to the Discord channel
        if stdout:
            await ctx.send(f"Command Output:\n{stdout}")
        if stderr:
            await ctx.send(f"Command Error:\n{stderr}")
    except Exception as e:
        await ctx.send(f"An error occurred while executing the command: {str(e)}")

# Run the bot
bot.run(TOKEN)
