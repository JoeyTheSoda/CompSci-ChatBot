import discord
import random
import asyncio

class MyClient(discord.Client):

  async def on_ready(self): #when the bot turns on

    print("Logged on as", self.user)
    self.amountoftime = 0

    #set bot status to streaming "Shark Tank" and link to gothamchess on twitch
    await client.change_presence(activity=discord.Streaming(name="Shark Tank", url="https://www.twitch.tv/gothamchess"))

    #create a background loop called cuban_quote_task for sending cuban_quotes over random periods of time
    self.background_task = self.loop.create_task(self.cuban_quote_task())
    self.state = "START"


  async def on_message(self, message): # hen a message is recieved  

    #don't respond to ourselves & record messages in console
    if message.author == self.user:
      return
    print(message.author.name, " - ", message.content, "in", message.channel)

    if self.state == "START":
      #decrease the amount of time before sending the next cuban_quote be 5 minutes every time someone messages
      self.amountoftime -= 5


      #add a upvote and downvote emoji to every message
      #await message.add_reaction(":upvote:714585291322818576")
      #await message.add_reaction(":downvote:714585843037110282")


      def is_i(m): #check if messages are from the one who called the command
        return m.author == message.author
      def is_me(m): #check if messages are from the bot
        return m.author == client.user


      #function for changing the amount of money a user has. Takes the members name and the amount you want to change the money by
      def change_money(username, change):
        with open("ChatBot/Member List/" + username + ".txt", "r") as file:
          data = file.readlines()
        data[1] = str(change)
        with open("ChatBot/Member List/" + username + ".txt", "w") as file:
          file.writelines(data)


      #function for accessing items from the profile txts. Takes the members name and the number of the line the item is on. 
      #Line 1 = name; Line 2 = money; Line 3 = tos_role;
      def get_txt(username, item):
        with open("ChatBot/Member List/" + username + ".txt", "r") as file:
          data = file.readlines()
          return(data[item].replace("\n", ""))


      #talk as cuban/run code through console
      if message.content == ".":
        await message.channel.purge(limit=1, check=is_i)
        user_input = input()
        if "_message" in user_input:
          await message.channel.send(user_input.replace("message", ""))
        else:
          exec(user_input)


      #command for setting up profiles for each user. Creates a txt file and writes the default parameters
      if message.content.lower() == "!profile_setup":
        async for member in message.guild.fetch_members(limit=None):
          file = open("ChatBot/Member List/" + member.name + ".txt", "wb")
          user_setup_information = (member.name + "\n1000" + "\nNA")
          file.write(user_setup_information.encode("UTF-8"))
          file.close()


      #roulette command. enter the number/color you bet on and then the amount you bet. ex. !roulette red 500 will bet $500 on red
      if "!roulette" in message.content.lower():
        cash = float(get_txt(message.author.name, 1)) #get how much money the user has
        payout = 0.0
        bet_message = message.content.split()
        bet = bet_message[1] #set bet to the number/color the user bet on
        bet_cash = float(bet_message[2]) #set bet_cash to how much the user bet
        win = True


        #if the user does not have enough money
        if cash < bet_cash: 
          await message.channel.send("You don't have enough money poor man.")
        else:
          #pick a random number between 0 and 36
          number = random.randint(0,36) 
          if number == 0:
            color = "green"
          elif number > 0 and number <= 18:
            color = "red"
          else:
            color = "black"

          if type(bet) is int: #if the user bets on a number
            if bet == number:
              payout = bet_cash * 35
            elif bet != number:
              payout = -bet_cash
              win = False
          else: #if the user bets on a color
            if bet == "green" and bet == color:
              payout = bet_cash * 35
            elif bet != "green" and bet == color:
              payout = bet_cash
            elif bet != color:
              payout = -bet_cash
              win = False
          
          if win:
            await message.channel.send("You won $" + str(payout) + " You now have $" + ".")
          else: 
            await message.channel.send("You lost $" + str(abs(payout)) + " You now have $" + str(payout + cash) + ".")
            
          change_money(message.author.name, cash + payout) #change the user's money


      if message.content.lower() == "tos_start":
        role_list = ["Investigator", "Lookout", "Sheriff", "Spy", "Bodyguard", "Doctor", "Unique", "Vampire Hunter", "Unique", "Vigilante", "Escort", "Unique", "Medium", "Unique", "Transporter", "Disguiser", "Forger", "Framer", "Unique", "Unique", "Mafioso", "Consigliere", "Consort", "Blackmailer", "Vampire", "Serial Killer", "Unique", "Arsonist", "Jester", "Witch", "Amnesiac", "Survivor", "Executioner"]

        unique_role_list = ["Jailor", "Veteran", "Mayor", "Retributionist", "Godfather", "Werewolf"]

        self.mafia_role_list = ["Disguiser", "Forger", "Framer", "Mafioso", "Consigliere", "Consort", "Blackmailer", "Godfather"]

        self.game_role_list = []
        self.mafia_list = []
        self.mafia_name_list = []
        self.playerlist = []
        self.player_list_names = []
        self.day = True
        self.round = 1
        self.setup = True
        for i in range(15):
          random_role = random.choice(role_list)
          if random_role == "Unique":
            random_role = random.choice(unique_role_list)
            unique_role_list.remove(random_role)
          self.game_role_list.append(random_role)
        print(self.game_role_list)
        await message.channel.send("The game will be starting soon. Message 'join' to join the game.")
        self.state = "TOS"


    if self.state == "TOS":
      if self.setup == True:
        if message.content.lower() == "game_start":
          for member in self.player_list: 
            with open("ChatBot/Member List/" + member.name + ".txt", "r") as file:
              data = file.readlines()
            data[2] = self.game_role_list.pop()
            with open("ChatBot/Member List/" + member.name + ".txt", "w") as file:
              file.writelines(data)
            roll_message = open("ChatBot/Roll List/" + data[2]).read()
            dm_channel = await member.create_dm()
            await dm_channel.send(roll_message)
            if data[2] in self.mafia_role_list:
              self.mafia_list.append(member)
              self.mafia_name_list.append(member.name)
            self.setup = False
            self.tos_background_task = self.loop.create.task(self.tos_task())
          for member in self.mafia_list:
            await dm_channel.send(self.mafia_name_list)
        elif message.content.lower() == "join" and len(self.playerlist) < 15:
          if message.author not in self.playerlist:
            self.playerlist.append(message.author)
            self.playerlistnames.append(message.author.name)
          print(self.playerlistnames)
        elif message.content.lower() == "playerlist":
          await message.channel.send(self.playerlistnames)

          
  async def say_cuban_quote(self):
    cuban_quote = random.choice(open("ChatBot/cuban_quote_list.txt").read().splitlines())
    await self.get_channel(803272334638186526).send(cuban_quote)


  async def cuban_quote_task(self):
    while not self.is_closed():
      await self.say_cuban_quote()
      self.amountoftime = random.randint(30,300)
      while self.amountoftime > 0:
        self.amountoftime -= 1
        await asyncio.sleep(60)


  async def tos_task():
    print("HhI")


client = MyClient()
token = ""
client.run(token)