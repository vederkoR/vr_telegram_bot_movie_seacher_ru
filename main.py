# This is my learning for the telegram bot

import telebot
from telebot import types
from movie_parsing import movie_selector

TOKEN = 'token here'
MOVIE_GENRES = ('thriller', 'comedy', 'action', 'sci_fi', 'fantasy', 'drama', 'horror', 'adventure')
MOVIE_SEARCH_MODE = ('recent', 'best', 'random')
bot = telebot.TeleBot(TOKEN)
genre = None
ms_mod = None


@bot.message_handler(commands=['movie'])
def movies(message):
    markup = types.InlineKeyboardMarkup(row_width=4)
    item_1 = types.InlineKeyboardButton('Thriller', callback_data=MOVIE_GENRES[0])
    item_2 = types.InlineKeyboardButton('Comedy', callback_data=MOVIE_GENRES[1])
    item_3 = types.InlineKeyboardButton('Action', callback_data=MOVIE_GENRES[2])
    item_4 = types.InlineKeyboardButton('Sci-Fi', callback_data=MOVIE_GENRES[3])
    item_5 = types.InlineKeyboardButton('Fantasy', callback_data=MOVIE_GENRES[4])
    item_6 = types.InlineKeyboardButton('Drama', callback_data=MOVIE_GENRES[5])
    item_7 = types.InlineKeyboardButton('Horror', callback_data=MOVIE_GENRES[6])
    item_8 = types.InlineKeyboardButton('Adventure', callback_data=MOVIE_GENRES[7])
    markup.add(item_1, item_2, item_3, item_4, item_5, item_6, item_7, item_8)
    bot.send_message(message.chat.id, 'Please, choose a genre:', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.message:
        global genre
        global ms_mod
        if call.data in MOVIE_GENRES:
            if call.data == MOVIE_GENRES[0]:
                genre = 'Thriller'
            elif call.data == MOVIE_GENRES[1]:
                genre = 'Comedy'
            elif call.data == MOVIE_GENRES[2]:
                genre = 'Action'
            elif call.data == MOVIE_GENRES[3]:
                genre = 'Sci-Fi'
            elif call.data == MOVIE_GENRES[4]:
                genre = 'Fantasy'
            elif call.data == MOVIE_GENRES[5]:
                genre = 'Drama'
            elif call.data == MOVIE_GENRES[6]:
                genre = 'Horror'
            elif call.data == MOVIE_GENRES[7]:
                genre = 'Adventure'
            markup = types.InlineKeyboardMarkup(row_width=3)
            item_1 = types.InlineKeyboardButton('Most recent', callback_data=MOVIE_SEARCH_MODE[0])
            item_2 = types.InlineKeyboardButton('All times best', callback_data=MOVIE_SEARCH_MODE[1])
            item_3 = types.InlineKeyboardButton('Random', callback_data=MOVIE_SEARCH_MODE[2])
            markup.add(item_1, item_2, item_3)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text=f'Will look for {genre} genre. \nPlease, choose a search mode',
                                  reply_markup=markup)

        elif call.data in MOVIE_SEARCH_MODE:
            if call.data == MOVIE_SEARCH_MODE[0]:
                ms_mod = 'most recent'
            elif call.data == MOVIE_SEARCH_MODE[1]:
                ms_mod = 'all-times-best'
            elif call.data == MOVIE_SEARCH_MODE[2]:
                ms_mod = 'random'
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text=f'Looking for the {ms_mod} {genre} movies')
            movies_dict = movie_selector(genre=genre, mode=ms_mod)
            for movie, links in movies_dict.items():
                bot.send_message(call.message.chat.id, "---***---")
                bot.send_message(call.message.chat.id, f'Name: {movie}')
                bot.send_message(call.message.chat.id, "Official Trailer:")
                bot.send_message(call.message.chat.id, links[0])
                bot.send_message(call.message.chat.id, "---***---")
                if links[1]:
                    bot.send_message(call.message.chat.id, "Watch here:")
                    bot.send_message(call.message.chat.id, links[1])
                    bot.send_message(call.message.chat.id, "---***---")


@bot.message_handler(content_types=['text'])
def answer(message):
    bot.send_message(message.chat.id, 'Commands available:\n/movie - helps to choose a movie to watch')


bot.polling()
