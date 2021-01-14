import discord

class MyClient(discord.Client):

    async def on_ready(self):
        
        print("Logged on as", self.user)

client = MyClient()
client.run("Nzk4OTY0MjE3NDYxMzQyMjcw.X_8raQ.aGRIb2hNX9iRRFoQPDH7FrUA-h4")