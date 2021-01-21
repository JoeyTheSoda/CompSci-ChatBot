import discord

class MyClient(discord.Client):

    async def on_ready(self):

        print("Logged on as", self.user)
        await self.get_channel(713138130374361220).send("!warn @Fake News")
       
    async def on_message(self, message):
        
        if message.author == self.user: #don't react to own messages
            return
        
        await message.add_reaction(":thumbsup:")

client = MyClient()
client.run(token)
