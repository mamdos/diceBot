import logging
import random

from reqs import TOKEN
from telegram.ext import (
    Updater,
    Filters,
    CommandHandler,
    MessageHandler,
)
from telegram import ParseMode

logging.basicConfig(format='%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s', 
                    level=logging.INFO)


# some text variables
start_text = """
Hiiiiii 
i am dicebot; 
a totaly real random dice genarator bot.

send /help for more info.
"""



def start(update, context):
    update.message.reply_text(start_text, 
        )

def help(update, context):
    name = update.effective_user.first_name
    update.message.reply_text(f"""
Welcome {name} 
---------------------------------------
if you want to generate random dice, just send a message to me with this formation:

    <i>3d10</i>

<b>first number is the amount of dices (how many dices you want) and the second one is each dice range,
for example in here we have 3 dices with a range of 1 to 10 numbers.</b>
---------------------------------------
That's it for now, i hope you enjoy the bot.


if you are a developer you can reach to source code through this link:
www.github.com/mamdos/dicebot

    """,
        parse_mode=ParseMode.HTML)

def dice(text):
    random_numbers = list()
    text = text.split('d')
    for i in range(int(text[0])):
        number = random.randint(1, int(text[1]))
        random_numbers.append(number)
    return random_numbers

def dice_send(update, context):
    text = update.message.text
    random_numbers = dice(text)
    send_string = ''
    sum_rand = 0
    counter = 0
    for this_number in random_numbers:
        sum_rand += this_number
        if counter != (len(random_numbers)-1):
            send_string += f"{str(this_number)} + "
        else:
            send_string += str(this_number)
        counter += 1

    send_string += f"= {str(sum_rand)}"

    update.message.reply_text(send_string)
def main():
    updater = Updater(token= TOKEN) 
    dispatcher = updater.dispatcher
    
    start_command = CommandHandler('start', start)
    help_command = CommandHandler('help', help)
    dice_handler = MessageHandler(Filters.regex('^\d*d\d*$') & (~Filters.command), dice_send)
    dispatcher.add_handler(start_command)
    dispatcher.add_handler(help_command)
    dispatcher.add_handler(dice_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()