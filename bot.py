import discord
from discord.ext import commands
import random
from dotenv import load_dotenv
from os import getenv

class DungeonsAndDiceBot(discord.Client):
    async def on_ready(self):
        print(f"Chatbot logged on as {self.user}!")

    async def on_message(self, message):
        print(message.content)
        # Check if the sender is itself
        if message.author == self.user:
            return

        # Check if the message is a command
        elif message.content[0] == "!":
            split_message = message.content[1:].split(" ")
            command = split_message[0]

            if command == 'roll':
                try:
                    # Check if the user specified a number of sides
                    if len(split_message) >= 2 and split_message[1].isdigit():
                        sides = int(split_message[1])
                    # Default to 6 sides if no sides were specified
                    elif len(split_message) == 1:
                        sides = 6
                    # Raise error if invalid side value was given
                    else:
                        raise TypeError("Invalid argument provided")

                    # Check if the user specified a number of dice
                    if len(split_message) >= 3 and split_message[2].isdigit():
                        dice_count = int(split_message[2])
                    # Default to 1 die if no number was specified
                    elif len(split_message) <= 2:
                        dice_count = 1
                    # Raise an error if invalid value was given.
                    else:
                        raise TypeError("Invalid argument provided")

                # Set output string for error
                except TypeError as e:
                    reply = f"Error: {e}\nUsage: !roll [sides] [dice count]"

                # No error occurred, so proceed with processing the dice rolls
                else:
                    reply = f"You rolled a "
                    rolls = []
                    sum_of_rolls = 0
                    for die in range(dice_count):
                        roll = random.randint(1, sides)
                        rolls.append(roll)
                        sum_of_rolls += roll

                    # Append the values of the rolls to the output string.
                    if len(rolls) == 1:
                        reply += f"{roll}!"
                    elif len(rolls) == 2:
                        reply += f"{rolls[0]} and {rolls[1]} (sum {sum_of_rolls})!"
                    else:
                        for i in range(len(rolls)):
                            if i == len(rolls) - 1:
                                reply += f"and {rolls[i]} (sum {sum_of_rolls})!"
                            else:
                                reply += f"{rolls[i]}, "

                # Send the message
                finally:
                    await message.channel.send(reply)

def main():
    load_dotenv()
    bot_token = getenv("TOKEN")
    if not bot_token:
        raise ValueError("Error: Token not provided. This might be due to .env not existing. Try copying the sample env file to .env with your bot's token.")
    intents = discord.Intents.default()
    intents.message_content = True
    bot = DungeonsAndDiceBot(command_prefix="!", intents=intents)
    bot.run(bot_token)

if __name__ == "__main__":
    main()