import discord
import secrets
from dotenv import load_dotenv
import os
import sys

class MyDMBot(discord.Client):
    def __init__(self, user_id, message, intents=discord.Intents.default()):
        super().__init__(intents=intents)
        self.user_id = user_id
        self.message = message

    async def on_ready(self):
        print(f'We have logged in as {self.user}')
        await self.send_dm()

    async def send_dm(self):
        try:
            user = await self.fetch_user(self.user_id)
            print(user)
            await user.send(self.message)
            print(f"Successfully sent DM to user {self.user_id}")
            return 200
        except discord.HTTPException as e:
            print(f"Failed to send DM to user {self.user_id}: {e}")
            return 403
        finally:
            await self.close()

async def main(user_id, message):
    bot = MyDMBot(user_id, message)
    load_dotenv()
    await bot.start(os.getenv("TOKEN"))

def send_2fa(user_id):
    text = f"Hey, it seems you have started a password reset procedure on *https://rhapsopy.onrender.com* ! \n \n > Here's your security code : **{secrets.token_urlsafe(4)}** \n \n Hope you enjoyed our services ! \n \n *https://rhapsopy.onrender.com*"
    asyncio.run(main(user_id, text))

if __name__ == '__main__':
    import asyncio
    text = f"Hey, it seems you have started a password reset procedure on *https://rhapsopy.onrender.com* ! \n \n > Here's your security code : **{secrets.token_urlsafe(4)}** \n \n Hope you enjoyed our services ! \n \n *https://rhapsopy.onrender.com*"
    #asyncio.run(main(600288196046678036 -> eg, text))
    send_2fa(sys.argv[1])