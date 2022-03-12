from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters

import logging
import wordle
import settings
import pickle
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler

sessions = {}
points = [-5, 100, 80, 50, 35, 10, 5]
qwerty = [chr(x+ord('a')) for x in range(26)];

def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Nuova partita avviata... Invia la prima parola!")
    username = update.message.from_user.id
    nick = update.message.chat.username
    if nick is None:
        return
    global sessions
    sol = wordle.rand_word()
    sol = sol[:-1]
    sessions[username] = [sol, 0, '', nick, qwerty.copy(), [], [], [], 0]; #b, n, y, g
    print("Nuova partita avviata da {}, sol: {}".format(nick, sol));
    
def res_to_str(res):
    s = '';
    for c in res:
        if c == 0:
            s += '\u2B1B';
        if c == 1:
            s += '\U0001f7e8';
        if c == 2:
            s += '\U0001f7e9';
    return s;


def update_leaderboard(id_, user, points):
    with open('leaderboard.pkl', 'rb') as f:
        leaderboard = pickle.load(f)
    if id_ not in leaderboard:
        leaderboard[id_] = [points, user];
    else:
        leaderboard[id_][0] += points;
        leaderboard[id_][1] = user;
    with open('leaderboard.pkl', 'wb') as f:
        pickle.dump(leaderboard, f)

def make_keyboard(white, grey, yellow, green):
    s = '';
    s += "\U0001f7e9: ";
    for c in green:
        s += c + ' ';
    s += '\n';   
    s+= "\U0001f7e8: "; 
    for c in yellow:
        s += c + ' ';
    s += '\n';
    s+= '\u2B1C: ';
    for c in white:
        s+= c + ' ';
    return s;

def game(update: Update, context: CallbackContext):
    username = update.message.from_user.id;
    msg = update.message.text.lower()
    nick = update.message.chat.username
    
    context.bot.delete_message(update.message.chat_id, update.message.message_id)
    
    if nick is None:
        return
    global sessions;
    if username not in sessions:
        context.bot.send_message(chat_id=update.effective_chat.id, text = "Per avviare una nuova partita digita /start");
    else:      
        if wordle.search_word(settings.dictionary,msg) == False:
            context.bot.send_message(chat_id=update.effective_chat.id, text = "Parola non valida")
        else :
            sessions[username][1] += 1
            res = res_to_str(wordle.cmp_words(msg, sessions[username][0], 
                                              sessions[username][4], sessions[username][5], sessions[username][6], sessions[username][7]))
            
            keyboard = make_keyboard(sessions[username][4], sessions[username][5], sessions[username][6], sessions[username][7]);
            
            if sessions[username][8] != 0:
                context.bot.delete_message(update.message.chat_id, sessions[username][8])
            
            txt = ". "+"  ".join(msg.upper()) + "\n" + res;
            context.bot.send_message(chat_id=update.effective_chat.id, text = txt)
            sessions[username][2] += res + '\n';
            
            if sessions[username][0] == msg:
                context.bot.send_message(chat_id=update.effective_chat.id, text = "Complimenti! Digita /start per ricominciare");
                final_txt ="Valhalla Wordle " + str(sessions[username][1]) + "/6" + "\n\n" + sessions[username][2]
                context.bot.send_message(chat_id=update.effective_chat.id, text = final_txt);
                update_leaderboard(username, nick, points[sessions[username][1]]);
                print("{} ha vinto in {} tentativi!".format(nick, sessions[username][1]))
                sessions.pop(username)
            elif sessions[username][1] == 6:
                context.bot.send_message(chat_id=update.effective_chat.id, text = "La parola giusta era {}, digita /start per ricominciare...".format(sessions[username][0]))
                final_txt ="Valhalla Wordle " +  "-/6" + "\n\n" + sessions[username][2]
                context.bot.send_message(chat_id=update.effective_chat.id, text = final_txt);
                update_leaderboard(username, nick, points[0]);
                sessions.pop(username)
                print("{} ha perso!".format(nick))
            else:
                mess = context.bot.send_message(chat_id=update.effective_chat.id, text = keyboard)
                sessions[username][8] = mess.message_id;
               # context.bot.send_message(chat_id=update.effective_chat.id, text = "{}/6".format(sessions[username][1]))

def show_leaderboard(update: Update, context: CallbackContext):
    text = "🏆 LEADERBOARD 🏆\n\n";
    with open('leaderboard.pkl', 'rb') as f:
        leaderboard = pickle.load(f)
        
    sorted_leaderboard = {k: v for k, v in sorted(leaderboard.items(), key=lambda item: item[1], reverse = True)}
    for x,i in zip(sorted_leaderboard, range(len(sorted_leaderboard))):
        if(i>=20):
            break;
        else:
            text += str(i+1) + " 》 " + leaderboard[x][1]+" " + str(leaderboard[x][0]) + "\n";
    context.bot.send_message(chat_id=update.effective_chat.id, text = text);
    
def help_(update: Update, context: CallbackContext):
    text = 'Il gioco è ancora in via di sviluppo, i punteggi sono 100, 80, 50, 35, 10, 5, -5, in base a quanti tentativi sono stati necessari, buona fortuna!';
    context.bot.send_message(chat_id=update.effective_chat.id, text = text);
    
def start_bot():
    global sessions
    sessions = {}
    updater = Updater(token='5237798422:AAFlobvbBvyTv6X5F5W-g8-XKmGWZs6Zet4', use_context=True)
    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                         level=logging.INFO)
    start_handler = CommandHandler('start', start)
    leaderboard_handler = CommandHandler('leaderboard', show_leaderboard)
    help_handler = CommandHandler('help', help_)
    dispatcher.add_handler(leaderboard_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    game_handler = MessageHandler(Filters.text & (~Filters.command), game)
    dispatcher.add_handler(game_handler)
    updater.start_polling()
    updater.idle()