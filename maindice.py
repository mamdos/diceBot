import logging
import random
import re

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

logger = logging.getLogger(__name__)

# some text variables
start_text = """
Hiiiiii 
I am DiceBot; 
A <b>COMPLETELY REAL</b> Random Dice Genarator.

send /help for more info.
"""

def start(update, context):
    update.message.reply_text(start_text, 
        parse_mode=ParseMode.HTML)

def help(update, context):
    name = update.effective_user.first_name
    update.message.reply_text(f"""
Welcome {name} 
---------------------------------------
if you want to generate random dice, just send a message with this formation:

    <i>3d10</i>

<b>first number is the amount of dices (how many dices you want) and the second one is each dice range,
for example in here we have 3 dices with a range of 1 to 10 numbers.</b>


<b><i>Update V2.1:</i></b>
In the latest update you can add modifiers
e.x:

    <i>6d10+7</i> AND <i>5d6-3</i>


In first example, That command generates the dices as always, but at the end adds 7 to the result.
In second one, The command generates the dices as always, but at the end reduces 3 from the result.
---------------------------------------
That's it for now, i hope you enjoy the bot.


if you are a developer you can reach to source code through this link:
https://github.com/mamdos/dicebot

    """,
        parse_mode=ParseMode.HTML)

def dice(numbers):
    random_numbers = list()
    for i in range(int(numbers[0])):
        number = random.randint(1, int(numbers[1]))
        random_numbers.append(number)
    return random_numbers

def dice_send(update, context):
    text = update.message.text
    words = re.split('\+|d|\s|-', text)
    fault = False

    for i in range(len(words)):
        try:
            words.remove('')
        except:
            break
    
    regexcp = re.compile(r'^\d+$')
    count = 0
    for num in words :
        if regexcp.search(num):
            count += 1


    if count == len(words):
        username = update.effective_user.username
        random_numbers = dice(words)
        send_string = ''
        sum_rand = 0
        counter = 0


        for this_number in random_numbers:
            sum_rand += this_number
            if counter == 0:
                send_string += f"({this_number} + "
            elif counter != (len(random_numbers)-1) and counter != 0:
                send_string += f"{str(this_number)} + "
            else:
                send_string += f"{str(this_number)})"
            counter += 1
        
        if len(words) == 3:
            modifier = int(words[2])
            if text.find('-') != -1 and text.find('+') == -1:
                modified = sum_rand - modifier
                send_string += f" - {modifier} = {modified}"
            elif text.find('+') != -1 and text.find('-') == -1:
                modified = sum_rand + modifier
                send_string += f" + {modifier} = {modified}"
            else:
                fault = True

        else:
            send_string += f" = {str(sum_rand)}"

        if fault == False:
            update.message.reply_text(send_string)
        else:
            update.message.reply_text("Please enter arguments correctly")



def main():
    updater = Updater(token= TOKEN) 
    dispatcher = updater.dispatcher
    
    start_command = CommandHandler('start', start)
    help_command = CommandHandler('help', help)
    dice_handler = MessageHandler(Filters.regex('^\d+[\sd]+\d+[\s\+-]+\d+$')
                        & (~Filters.command), dice_send)
    dispatcher.add_handler(start_command)
    dispatcher.add_handler(help_command)
    dispatcher.add_handler(dice_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
