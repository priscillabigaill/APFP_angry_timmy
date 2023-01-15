import nextcord
from nextcord.ext import commands
import akinator as ak
import asyncio # interaction.send
import random

# server ids which contains the bot
guilds = []

# global variables -> to keep track of players' info
player_names = [None,None]
player_ids = [None,None]
player_avatar_urls = [None,None]
player_scores = [0,0]
who_is_playing = None
number_attempts = 0

# calls the bot and enables all intents
bot = commands.Bot(intents=nextcord.Intents.all())

# when bot is ready to be used -> prints bot is online 
@bot.event 
async def on_ready():
    print('Bot Is Online!')

#--------- main menu ---------------------------------------------------------------------------------#

# if the /menu command is called, the menu function is used
@bot.slash_command(guild_ids = guilds, description="Main menu of Angry Timmy bot")
async def menu(ctx):

    # create an embed containing the menu information
    menu = nextcord.Embed(
        title="Welcome!",
        description="Angry Timmy is angry yet useful. Here are some features you can use the Angry Timmy bot for:",
        color=0xfbdcff
    )
    menu.add_field(name="⛴️💥 Battleship Game", value="Your childhood game Battleship but with a twist!\nUse the `/bship` command to play", inline=False)
    menu.add_field(name="🎱✨ Magic 8ball", value="Ask the magic 8ball yes/no questions and you will find the answer!\nUse the `/m8ball` command to ask", inline=False)
    menu.add_field(name="🧞🔮 Akinator Bot", value="The akinator bot can guess whoever you're thinking about!\nUse the `/akinator` command to play", inline=False)
    menu.set_thumbnail(url="https://i.pinimg.com/originals/00/59/bc/0059bc0ab9864498107b173f6391d59e.jpg")
    menu.set_footer(text="Abigail made this 😎")

    # sends and prints the menu embed
    await ctx.send(embed=menu)


#------- battleship game ------------------------------------------------------------------------------------------------#

# class that manages the start menu
class StartMenu(nextcord.ui.View):
    def __init__(self):
        super().__init__()
    
    # displays a button used to start the battleship game -> starts the game
    @nextcord.ui.button(label="Start Game", style=nextcord.ButtonStyle.blurple) 
    async def menu(self, button: nextcord.ui.Button, interaction: nextcord.Interaction) :
        
        # global variables 
        global player_names # player names
        global player_scores # players' scores
        global who_is_playing # current player (player 1/2)

        # embed containing info about who is playing
        playing = nextcord.Embed(
            title=f"{player_names[who_is_playing-1]}'s turn",
            color=0xf9cff5
        )
        playing.set_author(
            name=player_names[who_is_playing-1],
            icon_url=player_avatar_urls[who_is_playing-1]
        )
        playing.add_field(
            name="💯 Score",
            value=f"{player_names[0]}: ({player_scores[0]})\n{player_names[1]}: ({player_scores[1]})"
        )
        playing.set_footer(text="Abigail made this 😎")
        
        # displays the battleship game (buttons)
        view = Battleship()

        # send and prints the who is playing embed
        await interaction.send(embed=playing, view=view)

# class that represents the buttons
class BattleshipButtons(nextcord.ui.Button):
    def __init__(self, x: int, y: int):
        super().__init__(style=nextcord.ButtonStyle.secondary, label="\u200b", row=x)
        self.x = x # x-coordinate of the buttons
        self.y = y # y-coordinate of the buttons

    # function that is executed when its asociated button is pressed
    async def callback(self, interaction: nextcord.Interaction):
        assert self.view is not None # makes sure that self.view is available to use
        view = self.view # stores self.view into the variable view -> needed to display battleship buttons

        # global variables
        global who_is_playing # whos turn it is
        global player_ids # list of player ids
        global player_scores # list of player scores
        global player_names # list of player names
        global player_avatar_urls # list of player avatars
        global number_attempts # used to keep track of number of attempts

        # the loop runs/continues only if the user who clicked is the one whose turn it is
        if player_ids[who_is_playing-1] == interaction.user.id:
            
            # adds the number of attempts count by 1
            number_attempts+=1
            
            # if the location of the button clicked is 0 in the matrix -> miss
            if(not view.battleship_locs[self.x][self.y]):
                self.style = nextcord.ButtonStyle.grey
                self.label = "💣"
                self.disabled = True
                
            else:
                # if the location of the button clicked is 1 in the matrix -> hit
                self.style = nextcord.ButtonStyle.danger
                self.label = "💥"
                self.disabled = True

                # adds the player's score by 1
                player_scores[who_is_playing-1]+=1

             # switch players 
            if who_is_playing == 1:
                who_is_playing = 2
            else:
                who_is_playing = 1
                
            # embed containing which player's turn it is and their scores
            embed = nextcord.Embed(
                title=f"{player_names[who_is_playing-1]}'s turn",
                color=0xf9cff5
            )
            embed.set_author(
                name=player_names[who_is_playing-1],
                icon_url=player_avatar_urls[who_is_playing-1]
            )
            embed.add_field(
                name="💯 Score",
                value=f"{player_names[0]}: ({player_scores[0]})\n{player_names[1]}: ({player_scores[1]})"
            )
            embed.set_footer(text="Abigail made this 😎")

            content = None
        else:
            # embed printed if its not the user's turn
            embed = nextcord.Embed(
                title=f"{player_names[who_is_playing-1]}'s turn",
                color=0xf9cff5
            )
            embed.set_author(
                name=player_names[who_is_playing-1],
                icon_url=player_avatar_urls[who_is_playing-1]
            )
            embed.add_field(
                name="💯 Score",
                value=f"{player_names[0]}: ({player_scores[0]})\n{player_names[1]}: ({player_scores[1]})"
            )
            embed.set_footer(text="Abigail made this 😎")

            content = "Oops it's not your turn 😅"

        # if the number of attempts is still below 25 (the number of buttons)
        if number_attempts == 25:
                
            # embed generated if player 1 wins
            if player_scores[0]>player_scores[1]:
                who_wins = 1
                embed = nextcord.Embed(
                    title=f"{player_names[who_wins-1]} wins",
                    color=0xf9cff5
                )
                embed.add_field(
                    name="💯 Final Score", # final scores
                    value=f"<@{player_ids[0]}> ({player_scores[0]})\n<@{player_ids[1]}> ({player_scores[1]})"
                )
                embed.set_footer(text="Abigail made this 😎")

            
            # embed generated if player 2 wins
            elif player_scores[1]>player_scores[0]:
                who_wins = 2
                embed = nextcord.Embed(
                    title=f"{player_names[who_wins-1]} wins",
                    color=0xf9cff5
                )
                embed.set_author(
                    name=player_names[who_is_playing-1],
                    icon_url=player_avatar_urls[who_is_playing-1]
                )
                embed.add_field(
                    name="💯 Final Score", # final scores
                    value=f"<@{player_ids[0]}> ({player_scores[0]})\n<@{player_ids[1]}> ({player_scores[1]})"
                )
                embed.set_footer(text="Abigail made this 😎")
            else:
                # embed generated if the score is a tie
                embed = nextcord.Embed(
                    title="it's a tie",
                    color=0xf9cff5
                )
                embed.add_field(
                    name="💯 Final Score", # final scores
                    value=f"<@{player_ids[0]}> ({player_scores[0]})\n<@{player_ids[1]}> ({player_scores[1]})"
                )
                embed.set_footer(text="Abigail made this 😎")

            # restarts the scores and number of attempts back to 0
            player_scores = [0,0] 
            number_attempts = 0

            # disables all the buttons
            view.stop() 

        # prints the wanted embed
        await interaction.response.edit_message(content=content, embed=embed,view=view)

# class that manages the battleship game
class Battleship(nextcord.ui.View):
    def __init__(self):
        super().__init__()

        while True:
            # generates a random binary matrix to be used as a reference for the buttons 
            self.battleship_locs = [[random.randint(0, 1) for _ in range(5)] for _ in range(5)]
            count = sum(sum(row) for row in self.battleship_locs)
            if 10 <= count <= 15:
                break

        # prints the matrix into the terminal -> cheat code 
        print(self.battleship_locs)

        # making the grid of buttons
        for x in range(5):
            for y in range(5):
                self.add_item(BattleshipButtons(x, y))


# slash command that calls the bship function
@bot.slash_command(guild_ids = guilds, description="Battleship game with a twist")
async def bship(interaction: nextcord.Interaction, player1: nextcord.Member, player2: nextcord.Member):

    # global variables
    global player_names
    global player_ids
    global player_avatar_urls
    global who_is_playing

    if(player1.name): 
        player_names[0] = player1.name
        player_ids[0] = player1.id
        player_avatar_urls[0] = player1.avatar

    if(player2.name): 
        player_names[1] = player2.name
        player_ids[1] = player2.id
        player_avatar_urls[1] = player2.avatar

    # decide who's playing first
    who_is_playing = random.randint(1,2) 

    # embed containing the info of the game
    embed = nextcord.Embed(
        title="Battleship Game 💥⛴️",
        description="Destroy the most ships to win. good luck :)",
        color=0xf9cff5
    )

    embed.add_field(name="⁉️ How the game works?", value="Each player take turns guessing where the ships are. The player who bombs more ships will be the winner.")
    embed.add_field(name="👥 Players", value=f"player 1: {player_names[0]} (<@{player_ids[0]}>) \n player 2: {player_names[1]} (<@{player_ids[1]}>)", inline=False)
    embed.set_footer(text="Abigail made this 😎")
    
    # calls the StartMenu class
    view = StartMenu()

    # prints the start menu embed and start game button
    await interaction.send(embed=embed, view=view)

#------- magic 8ball ---------------------------------------------------------------------------------------------#

# list containing all possible answers 
list_of_ans = ["It is certain", "Definitely not", "Reply hazy", "try again", "As I see it, yes", "Dont count on it", "It is decidedly so", "Ask again later",
    "My reply is no", "Without a doubt", "Of course", "Better not tell you now", "My sources say no", "Yes definitely", "Cannot predict now",
    "Outlook not so good", "You may rely on it", "Concentrate and ask again", "Very doubtful", "Most likely",
    "Outlook good", "Yes", "Signs point to yes"]

# a slash command using the m8ball function
@bot.slash_command(guild_ids = guilds, description="Magic 8ball that answers your yes/no questions")
async def m8ball(interaction: nextcord.Interaction, question: str): #accepts a parameter -> the question

    # randomly choose an answer out of the list_of_ans list
    selected_ans = random.choice(list_of_ans)

    # makes the answer embed
    embed = nextcord.Embed(
        title=f"'{question}'",
        description=f"`{selected_ans}`",
        color=0xf9cff5
    )
    embed.set_thumbnail(url="https://i.pinimg.com/originals/75/d3/df/75d3df783cfe8380440051924f2ad200.jpg")
    embed.set_footer(text="Abigail made this 😎")

    # sends and prints the answer embed
    await interaction.send(embed=embed)

#------- akinator bot ---------------------------------------------------------------------------------------------#

# a slash command using the akinator function
@bot.slash_command(guild_ids = guilds, description="Akinator bot that guesses anyone you're thinking of")
async def akinator(Interaction: nextcord.Interaction):
    
    # constant
    AKINATOR_YES = "✅" 
    AKINATOR_NO = "❌" 
    AKINATOR_PROBABLY = "🤷🏻" 
    AKINATOR_IDK = "❔"
    AKINATOR_BACK = "⬅️" 
    
    # intro embed
    intro = nextcord.Embed(title="Welcome! 🔮", description="Hi " + Interaction.user.mention + "! I am Akinator 🧞✨",
                            color=0xf9cff5)
    intro.add_field(name="How to play", value="Think of a person (real or fictional) and I will try to guess who it is", inline=False)
    intro.set_thumbnail(url="https://www.designbolts.com/wp-content/uploads/2019/04/aladdin-Lamp_2019-Movie.jpg")
    intro.set_footer(text="Abigail made this 😎")

    # bye embed (outro)
    bye = nextcord.Embed(title="Byebye 👋🏻", description="Use the command `/menu` to see what else you can do with Angry Timmy bot!", color=0xf9cff5)
    bye.set_thumbnail(url="https://www.designbolts.com/wp-content/uploads/2019/04/aladdin-Lamp_2019-Movie.jpg")
    bye.set_footer(text="Abigail made this 😎")

    # send intro embed (print)
    await Interaction.send(embed=intro)

    # check if the person clicking on the reaction button is the same person who initiated the game
    def check(reaction, user):
        return user == Interaction.user 
        
    # convert reaction into sring readable by akinator
    def reaction_to_str(str_reaction):
        if str_reaction == AKINATOR_YES:
            return 'y'
        elif str_reaction == AKINATOR_NO:
            return 'n'
        elif str_reaction == AKINATOR_PROBABLY:
            return 'p'
        elif str_reaction == AKINATOR_IDK:
            return 'idk'
        else:
            return 'b'

    try:
        # calls akinator class -> imports the class from akinator library here
        aki = ak.Akinator()

        # initiate the game
        q = aki.start_game()

        # loops while the akinator's confidence level is still below 80 (after 80 it will guess)
        while aki.progression <= 80:

            # question embed
            question = nextcord.Embed(title="Guessing.. 🙇🏻‍♀️", description=q, color=0xf9cff5)
            question.add_field(
                name="How to answer?", 
                value="To answer, click on one of the reaction emojis down below.\n\n✅ : yes\n❌ : no\n🤷🏻 : probably\n❔ : idk\n⬅ : back\n\nWait until all reactions have appeared before selecting your answer.", 
                inline=False)
            question.set_thumbnail(url="https://www.designbolts.com/wp-content/uploads/2019/04/aladdin-Lamp_2019-Movie.jpg")
            question.set_footer(text="Abigail made this 😎")

            # sends the question embed containing the question
            question_sent = await Interaction.send(embed=question)

            # adding reactions into(below) the embed -> so the user only has to click on the existing reaction options
            await question_sent.add_reaction(AKINATOR_YES)
            await question_sent.add_reaction(AKINATOR_NO)
            await question_sent.add_reaction(AKINATOR_PROBABLY)
            await question_sent.add_reaction(AKINATOR_IDK)
            await question_sent.add_reaction(AKINATOR_BACK)

            try:

                # waits for a reaction by the user 
                # function wait_for outputs 2 variables -> reaction, user
                # "reaction, _" makes sure only the reaction is used
                reaction, _ = await bot.wait_for('reaction_add', timeout=30, check=check)
            except asyncio.TimeoutError:
                await Interaction.send("You took too long to respond:(")
                await Interaction.send(embed=bye)
                return # game is stopped if no input for 30 seconds

            # if the back reaction is clicked
            if str(reaction.emoji) == AKINATOR_BACK:
                try:
                    q = aki.back() # calls back function
                except ak.CantGoBackAnyFurther:
                    await Interaction.send(e) # sends error message (cant go back any further)
                    continue
            else:
                try:
                    # calls reaction_to_str funtion and assigns the converted reaction emoji 
                        # into the variable akinator_str
                    akinator_str = reaction_to_str(str(reaction.emoji))
                    # calls answer function from the akinator library and uses akinator_str as a parameter
                    q = aki.answer(akinator_str)
                except ak.InvalidAnswer as e:
                    await Interaction.send(e) # sends error message that the answer is invalid
                    continue
        
        # after confidence level reaches 80 
        # signals akinator to make a guess
        aki.win()

        # creates an embed using the keys from the guesses -> the outputs of the aki.win function 
        answer = nextcord.Embed(title="My guess is..", description=aki.first_guess['name']+"! ✨",
                                color=0xf9cff5)
                                # aki.first_guess['description']
        answer.set_image(url=aki.first_guess['absolute_picture_path'])
        answer.set_footer(text="Did I guess the right person?")
        question_sent = await Interaction.send(embed=answer)
        await question_sent.add_reaction(AKINATOR_YES)
        await question_sent.add_reaction(AKINATOR_NO)

        try:
            # waits for a reaction by the user 
            # function wait_for outputs 2 variables -> reaction, user
            # "reaction, _" makes sure only the reaction is used
            reaction, _ = await bot.wait_for('reaction_add', timeout=30, check=check)
        except asyncio.TimeoutError:
            await Interaction.send("You took too long to respond :(")
            await Interaction.send(embed=bye) # sends bye embed after no response for 30 seconds
            return
        
        # if the guess is correct
        if str(reaction.emoji) == AKINATOR_YES:
            yes = nextcord.Embed(title="Yayy! 😆", color=0xf9cff5)
            await Interaction.send(embed=yes)

        # if the guess is incorrect
        else:
            no = nextcord.Embed(title="OOPSIEE 😅", color=0xf9cff5)
            await Interaction.send(embed=no)
        await Interaction.send(embed=bye)
        
    # if there is an error
    except Exception as e:
        await Interaction.send(e)



#------- running the bot ---------------------------------------------------------------------------------------------#

# calls the run function and uses the discord bot token as a parameter
bot.run("")