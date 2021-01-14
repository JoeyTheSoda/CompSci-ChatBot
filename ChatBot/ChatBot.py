import discord

class MyClient(discord.Client):

    async def on_ready(self):

        print("Logged on as", self.user)
        await self.get_channel(713138130374361220).send("!warn @Fake News")

client = MyClient()
client.run("Nzk4OTY0MjE3NDYxMzQyMjcw.X_8raQ.aGRIb2hNX9iRRFoQPDH7FrUA-h4")