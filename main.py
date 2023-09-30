import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def logged():
	from datetime import datetime
	print('STARTED  \n\n\n\n\n\n\n\n\n\n', datetime.now())
logged()



#yandex -  google +
#page = json.loads(bs(urlopen("https://www.wildberries.ru/webapi/product/50846038/data?subject=3274&kind=0&brand=922411").read().decode("utf-8"), "html.parser").text)
#print(page["value"]["data"]["sitePath"][2]["name"])

#https://www.aliexpress.com/item/3256804708968405.html


from aiogram.filters.text import Text

from aiogram import F, Bot, Dispatcher, Router, types, filters
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.utils.markdown import hlink
import asyncio
import logging
import Levenshtein

import btns
from config_reader import config

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.bot_token.get_secret_value(), parse_mode = 'html')
dp = Dispatcher()
r = Router()


global web_price_id
web_price_id_file = open(BASE_DIR+'/data/web_price_id', 'r')
web_price_id = web_price_id_file.read()
web_price_id_file.close()

global price_id, document_id, video_id
file_ids_file = open(BASE_DIR+'/data/file_ids', 'r')
file_ids = file_ids_file.readlines()
price_id = file_ids[0].replace('\n', '')
document_id = file_ids[1].replace('\n', '')
video_id = file_ids[2].replace('\n', '')
file_ids_file.close()

kb = []
for i in btns.main_btns:
	kb.append([types.KeyboardButton(text=i)])
	keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard = True, input_field_placeholder="Нажмите кнопки ниже...")



async def start(message: types.message):

	us = message.from_user
	user = (us.id, us.first_name, us.last_name, str(us.username))
	
	await message.answer(f'Здравствуйте, {message.chat.first_name} ! \nМы компания "Double front" - предоставляем возможность приобрести новые видеокарты и комплектующие из Китая.\nЯ отвечу на большинство ваших вопросов. Если остануться вопросы, напишите продавцу.', reply_markup = keyboard)
	print('  START    ', message)


async def my_msg(message: types.message):
	print('  MY_MSG    ', message)
	if not message.chat.id in config.elite_ids:
		hl = hlink('продавцу', 't.me/Fenrir322')
		answer = f'{message.chat.first_name}, можете написать напрямую {hl}, а так же задать свой вопрос здесь, вам ответит оператор !'
		await message.answer(answer)

		builder = InlineKeyboardBuilder()
		builder.row(types.InlineKeyboardButton(text="ID: "+str(message.chat.id), url = 'tg://user?id='+str(message.chat.id)))

		if message.from_user.username == None:
			third = ""
		else:third = "@"+message.from_user.username

		user = f"{message.from_user.first_name} {message.from_user.last_name} {third}"
		o_text = f"""{user}

<code>{message.text}</code>"""
		
		await bot.send_message(chat_id = config.elite_ids[1], text = o_text, reply_markup = builder.as_markup())
		await bot.send_message(chat_id = config.elite_ids[2], text = o_text, reply_markup = builder.as_markup())
		print('  MY_MSG_DEF    ', message)
		return
		#await bot.forward_message(chat_id=2041110046, from_chat_id=message.chat.id, message_id=message.message_id)
		#await bot.forward_message(chat_id=1313792747, from_chat_id=message.chat.id, message_id=message.message_id)
	else:
		if message.reply_to_message != None:
		    await bot.send_message(chat_id = int(message.reply_to_message.reply_markup.inline_keyboard[0][0].text[3:]), text = message.text)
		else:await message.answer("Выберите сообщение для ответа")
		
	print('  MY_MSG    ', message)


import re
regex = r"\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b"

p_delete = ["computeruniverse.net", "newegg.com", "r-seven.ru", "amazon.com", "pleer.ru", "kotofoto.ru", "fotosklad.ru"]
t_word = ["videokarty", "materinskie_platy", "protsessory", "operativnaya_pamyat", "ssd_diski", "hdd", "bloki_pitaniya", "kompyuternye_korpusa", "kulery_dlya_protsessorov", "sistemy_vodyanogo_okhlazhdeniya_pk", "ventilyatory_dlya_korpusa", "sistemnye_bloki", 
	"processor", "materinskaa-plata", "videokartyа", "operativnaa-pamat", "blok-pitania", "korpus", "sata", "ssd", "zestkij-disk", "kuler-dla-processora", "sistema-ohlazdenia", "ventilator", "pk", "custompc", "configurator", "conf", "compare", 
	"sistemnyy-blok", "zhestkiy-disk", "-tb", "-gb", "operativnaya-pamyat", "materinskaya-plata", "protsessor", "blok-pitaniya", "ventilyator", "sistema-ohlazhdeniya", "korpus", 
	"videokarta"]

from urllib.parse import urlparse
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
white_list = ['плохо']
sense_words = ['кукан', 'хуеплет', 'eбу', '6ля', '6лядь', '6лять', 'b3ъeб', 'cunt', 'e6aль', 'ebal', 'eblan', 'eбaл', 'eбaть', 'eбyч', 'eбать', 'eбёт', 'eблантий', 'xyёв', 'xyй', 'xyя', 'xуе,xуй', 'xую', 'zaeb', 'zaebal', 'zaebali', 'zaebat', 'архипиздрит', 'ахуел', 'ахуеть', 'бздение', 'бздех', 'бздецы', 'бздит', 'бздицы', 'бздло', 'бзднуть', 'бздун', 'бздунья', 'бздюха', 'бздюшка', 'бздюшко', 'бля', 'блябу', 'блябуду', 'бляд', 'бляди', 'блядина', 'блядище', 'блядки', 'блядовать', 'блядство', 'блядун', 'блядуны', 'блядунья', 'блядь', 'блядюга', 'блять', 'вафлёр', 'взъебка', 'взьебка', 'взьебывать', 'въеб', 'въебался', 'въебенн', 'въебусь', 'въебывать', 'выблядок', 'выблядыш', 'выеб', 'выебать', 'выебен', 'выебнулся', 'выебон', 'выебываться', 'гандон', 'гнид', 'гнида', 'гниды', 'говенка', 'говешка', 'говназия', 'говнецо', 'говнище', 'говноед', 'говнолинк', 'говночист', 'говнюк', 'говнюха', 'говнядина', 'говняк', 'говнять', 'гондон', 'доебываться', 'долбоеб', 'долбоёб', 'дрисня', 'дрист', 'дристануть', 'дристать', 'дристун', 'дристуха', 'е6ал', 'е6ут', 'еб твою мать', 'ёб твою мать', 'ёбaн', 'ебaть', 'ебyч', 'ебал', 'ебало', 'ебальник', 'ебан', 'ебанамать', 'ебанат', 'ебаная', 'ёбаная', 'ебанический', 'ебанный', 'ебанныйврот', 'ебаное', 'ебануть', 'ебануться', 'ёбаную', 'ебаный', 'ебанько', 'ебарь', 'ебат', 'ёбат', 'ебатория', 'ебать', 'ебать-копать', 'ебаться', 'ебашить', 'ебёна', 'ебет', 'ебёт', 'ебец', 'ебик', 'ебин', 'ебись', 'ебическая', 'ебки', 'ебла', 'еблан', 'ебливый', 'еблище', 'ебло', 'еблыст', 'ебля', 'ебнуть', 'ебнуться', 'ебня', 'ебошить', 'ебская', 'ебский', 'ебтвоюмать', 'ебун', 'ебут', 'ебуч', 'ебуче', 'ебучее', 'ебучий', 'ебучим', 'ебущ', 'ебырь', 'елда', 'елдак', 'елдачить', 'заговнять', 'задристать', 'зае6', 'заё6', 'заеб', 'заёб', 'заеба', 'заебал', 'заебанец', 'заебастая', 'заебастый', 'заебать', 'заебаться', 'заебашить', 'заебистое', 'заёбистое', 'заебистые', 'заёбистые', 'заебистый', 'заёбистый', 'заебись', 'заебошить', 'заебываться', 'залуп', 'залупа', 'залупаться', 'залупить', 'залупиться', 'замудохаться', 'запиздячить', 'засерать', 'засерун', 'засеря', 'засирать', 'засрун', 'захуячить', 'заябестая', 'злоеб', 'злоебучая', 'злоебучее', 'злоебучий', 'ибанамат', 'ибонех', 'изъебнуться', 'ипать', 'ипаться', 'ипаццо', 'манда', 'мандавошек', 'мандавошка', 'мандавошки', 'мандей', 'мандень', 'мандеть', 'мандища', 'мандой', 'манду', 'мандюк', 'минетчик', 'минетчица', 'млять', 'мокрощелка', 'мокрощёлка', 'мразь', 'мудak', 'мудaк', 'мудаг', 'мудак', 'муде', 'мудель', 'мудеть', 'мудил', 'мудистый', 'мудня', 'мудоеб', 'мудозвон', 'мудоклюй', 'на хуй', 'набздел', 'набздеть', 'наговнять', 'надристать', 'наебать', 'наебет', 'наебнуть', 'наебнуться', 'наебывать', 'напиздел', 'напиздели', 'напиздело', 'напиздили', 'настопиздить', 'нахуй', 'нахуйник', 'не ебет', 'не ебёт', 'невротебучий', 'невъебенно', 'нехира', 'Нехуй', 'нехуйственно', 'нихуя', 'обдристаться', 'обосранец', 'обосцать', 'обосцаться', 'объебос', 'обьебать обьебос', 'однохуйственно', 'опездал', 'опизде', 'опизденивающе', 'остоебенить', 'остопиздеть', 'отмудохать', 'отпиздить', 'отпиздячить', 'отпороть', 'отъебись', 'охуевательский', 'охуевать', 'охуевающий', 'охуел', 'охуенно', 'охуеньчик', 'охуеть', 'охуительно', 'охуительный', 'охуяньчик', 'охуячивать', 'охуячить', 'очкун', 'падла', 'падонки', 'падонок', 'паскуда', 'педерас', 'педик', 'педрик', 'педрила', 'педрилло', 'педрило', 'педрилы', 'пездень', 'пездит', 'пездишь', 'пездо', 'пездят', 'пи3д', 'пи3де', 'пи3ду', 'пиzдец', 'пидар', 'пидарaс', 'пидарас', 'пидарасы', 'пидары', 'пидор', 'пидорасы', 'пидорка', 'пидорок', 'пидоры', 'пидрас', 'пизда', 'пиздануть', 'пиздануться', 'пиздарваньчик', 'пиздато', 'пиздатое', 'пиздатый', 'пизденка', 'пизденыш', 'пиздёныш', 'пиздеть', 'пиздец', 'пиздит', 'пиздить', 'пиздиться', 'пиздишь', 'пиздища', 'пиздище', 'пиздобол', 'пиздоболы', 'пиздобратия', 'пиздоватая', 'пиздоватый', 'пиздолиз', 'пиздонутые', 'пиздорванец', 'пиздорванка', 'пиздострадатель', 'пизду', 'пиздуй', 'пиздун', 'пиздунья', 'пизды', 'пиздюга', 'пиздюк', 'пиздюлина', 'пиздюля', 'пиздят', 'пиздячить', 'писбшки', 'писька', 'писькострадатель', 'писюн', 'писюшка', 'по хуй', 'по хую', 'подговнять', 'подонки', 'подонок', 'подъебнуть', 'подъебнуться', 'поебать', 'поебень', 'поёбываает', 'поскуда', 'посрать', 'потаскуха', 'похуй', 'похуист', 'похуистка', 'похую', 'придурок', 'приебаться', 'припиздень', 'припизднутый', 'припиздюлина', 'пробзделся', 'проблядь', 'проеб', 'проебанка', 'проебать', 'промандеть', 'промудеть', 'пропизделся', 'пропиздеть', 'пропиздячить', 'разхуячить', 'разъеб', 'разъеба', 'разъебай', 'разъебать', 'распиздай', 'распиздеться', 'распиздяй', 'распиздяйство', 'распроеть', 'сволота', 'сволочь', 'сговнять', 'секель', 'серун', 'серька', 'сестроеб', 'сикель', 'сирать', 'сирывать', 'соси', 'спиздел', 'спиздеть', 'спиздил', 'спиздила', 'спиздили', 'спиздит', 'спиздить', 'срака', 'сраку', 'сранье', 'срун', 'ссака', 'ссышь', 'стерва', 'страхопиздище', 'суходрочка', 'сучара', 'сучий', 'сучка', 'сучко', 'сучонок', 'сучье', 'сцание', 'сцать', 'сцука', 'сцуки', 'сцуконах', 'сцуль', 'сцыха', 'сцышь', 'съебаться', 'сыкун', 'трахае6', 'трахаеб', 'трахаёб', 'трахатель', 'ублюдок', 'уебать', 'уёбища', 'уебище', 'уёбище', 'уебищное', 'уёбищное', 'уебк', 'уебки', 'уёбки', 'уебок', 'уёбок', 'урюк', 'усраться', 'ушлепок', 'хyё', 'хyй', 'хyйня', 'хитровыебанный', 'хуeм', 'хуе', 'хуё', 'хуевато', 'хуёвенький', 'хуевина', 'хуево', 'хуевый', 'хуёвый', 'хуек', 'хуёк', 'хуел', 'хуем', 'хуенч', 'хуеныш', 'хуенький', 'хуеплет', 'хуеплёт', 'хуепромышленник', 'хуерик', 'хуерыло', 'хуесос', 'хуесоска', 'хуета', 'хуетень', 'хуею', 'хуи', 'хуй', 'хуйком', 'хуйло', 'хуйня', 'хуйрик', 'хуище', 'хуля', 'хую', 'хуюл', 'хуя', 'хуяк', 'хуякать', 'хуякнуть', 'хуяра', 'хуясе', 'хуячить', 'целка', 'чмо', 'чмошник', 'чмырь', 'шалава', 'шалавой', 'шараёбиться', 'шлюха', 'шлюхой', 'шлюшка']
async def msg(message: types.message):
	
	if not message.from_user.id in config.elite_ids:
		if message.entities != None:
			if message.entities[0].type == 'url':
				m_link = re.findall(regex, message.text)

				for i in m_link:
					if "http://" in i:
						pass
					elif "https://" in i:
						pass
					else:i = "http://"+i

					i1 = '.'.join(urlparse(i).netloc.split('.')[-2:]).lower()
					if i1 in p_delete:
						await bot.delete_message(message.chat.id, message.message_id)
						print("  MSG_LINK_PDELETE    ", message)
						return
					else:

						for t in t_word:
							if t in i:
								await bot.delete_message(message.chat.id, message.message_id)
								print("  MSG_LINK_WITH_TWORD    ", message)
								return
							else:pass

						if "aliexpress" in i1:
							if "sl" in i1:
								await bot.delete_message(message.chat.id, message.message_id)
								print("  MSG_LINK_ALI    ", message)
								return
							else:
								i = i.replace("http://", "https://")
								page = urlopen(i).read().decode("utf-8")
								html = bs(page, "html.parser")
								category = html.select(".snow-ali-kit_Typography-Secondary__link__1i67dw")[1].text
								if category == "Компьютерные комплектующие":
									await bot.delete_message(message.chat.id, message.message_id)
									print("  MSG_LINK_ALI    ", message)
									return
								else:pass				
						if "t.me" in i1:
							if i == "http://t.me/+vzrnZLJLiZI0YTc6" or i == "https://t.me/+vzrnZLJLiZI0YTc6" or i == "http://t.me/opaplaylist" or i == "https://t.me/opaplaylist":
								pass
							else:
								await bot.delete_message(message.chat.id, message.message_id)
								print("  MSG_LINK_WITH_TWORD    ", message)
								return
			else:pass
		else:
			text = str(message.text.lower())

			#checking for containing the word
			for i in text.split():
				if i in sense_words:
					await bot.delete_message(message.chat.id, message.message_id)

					if message.from_user.username == None:
						third = ""
					else:third = "@"+message.from_user.username
					if message.from_user.last_name == None:
						second = ""
					else:second = message.from_user.last_name

					message_id = str(message.message_id)
					username_g = str(message.chat.username)
					user = f"{message.from_user.first_name} {second} {third}"
					
					p = str(message.text)
					p1 = p.replace(str(i), f"<code>{i.lower()}</code>")
					print(i)
					o_text = f"""{user}
	Совпадение

	{p1}"""
					
					builder = InlineKeyboardBuilder().row(types.InlineKeyboardButton(text="RO 60S", callback_data = "ro_60s"+str(message.from_user.id)), types.InlineKeyboardButton(text="ID: "+str(message.from_user.id), url = 'tg://user?id='+str(message.from_user.id)))


					await bot.send_message(chat_id = config.elite_ids[2], text = o_text, reply_markup = builder.as_markup(), parse_mode='html')
					await bot.send_message(chat_id = config.elite_ids[3], text = o_text, reply_markup = builder.as_markup(), parse_mode = "html")

					print("  MSG_BADB    ", message)
					return
				else:pass

			for j in sense_words:
				if j in  "".join(text.split()):
					
					if message.from_user.username == None:
						third = ""
					else:third = "@"+message.from_user.username
					if message.from_user.last_name == None:
						second = ""
					else:second = message.from_user.last_name

					message_id = str(message.message_id)
					username_g = str(message.chat.username)
					user = f"{message.from_user.first_name} {second} {third}"
					
					p = str(message.text)
					p1 = p.replace(str(j), f"<code>{j.lower()}</code>")
					print(j)
					o_text = f"""{user}
	Подозрение

	{p1}"""
					
					builder = InlineKeyboardBuilder().row(types.InlineKeyboardButton(text="RO 60s", callback_data = "ro_60s"+str(message.from_user.id)), types.InlineKeyboardButton(text="Сообщение", url = f"t.me/{username_g}/{message_id}"))

					await bot.send_message(chat_id = config.elite_ids[2], text = o_text, reply_markup = builder.as_markup(), parse_mode='html')
					await bot.send_message(chat_id = config.elite_ids[3], text = o_text, reply_markup = builder.as_markup(), parse_mode = "html")
					print("  MSG_MBADB    ", message)
					return
				else:pass

		print('  MSG    ', message)
	else:pass


from time import sleep
@dp.callback_query(lambda c: 'ro_60s' in c.data)
async def ro_60s(call: types.CallbackQuery):
	try:
		await bot.forward_message(chat_id = int(call.data[6:]), from_chat_id = config.group_id, message_id = int(call.message.reply_markup.inline_keyboard[0][1].url.split("/")[-1]))
		await bot.delete_message(chat_id = config.group_id, message_id = int(call.message.reply_markup.inline_keyboard[0][1].url.split("/")[-1]))
	except Exception as e:
		print(e)

	await bot.restrict_chat_member(chat_id = config.group_id, user_id = int(call.data[6:]), 
		permissions = types.ChatPermissions(can_send_messages=False))

	await bot.send_message(chat_id = int(call.data[6:]), text = f"""Вас приветствует бот канала "Double Front" во избежание полной блокировки настоятельно рекомендуем Вам ознакомиться с правилами

{btns.rules}""")

	sleep(60)
	await bot.restrict_chat_member(chat_id = config.group_id, user_id = int(call.data[6:]), 
		permissions = types.ChatPermissions(
			can_send_messages=True,
			can_send_media_messages=True,
            can_send_polls=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True,
            can_change_info=True,
            can_invite_users=True,
            can_pin_messages=True))

	


	print('  RO_60S    ', call)


async def price_def(message: types.message):

	hl = hlink('таблице', web_price_id)
	await message.answer(f'{message.from_user.first_name}, Актуальный прайс смотрите в {hl}', disable_web_page_preview=True)
	
	print('  PRICE    ', message)


async def document(message: types.message):
	
	await message.answer_document(caption = 'Договор я отправляю уже заполненный с своей стороны вы его распечатываете  и тоже заполняете от руки потом отправляете мне в формате (фото,скан)', document = document_id)
	
	print('  DOCUMENT    ', message)


async def faq_msg(message: types.message):
	
	builder = InlineKeyboardBuilder()
	for i in range(len(btns.faq_btns_text)):
		if i == 6:
			builder.row(types.InlineKeyboardButton(text=btns.faq_btns_text[i], url = 't.me/+vzrnZLJLiZI0YTc6'))
		else:
			builder.row(types.InlineKeyboardButton(text=btns.faq_btns_text[i], callback_data="faq_cl"+str(i)))
	
	await message.answer('Нажмите на интересующий вас вопрос', reply_markup = builder.as_markup())

	print('  F.A.Q.    ', message)



async def webprice(message: types.message):

	if message.from_user.id in config.elite_ids:
		if len(message.entities) == 2:
			if message.entities[1].type == 'url':
		
				global web_price_id
				web_price_id = message.text[10:]

				with open(BASE_DIR+'/data/web_price_id', 'w') as f:
					f.write(f'{web_price_id}')
					f.close()

				builder = InlineKeyboardBuilder()
				builder.row(types.InlineKeyboardButton(text="Уведомление пользователям", callback_data="newprice_resend"))
				await message.answer(f'ID Прайса успешно изменено на \n<code>{web_price_id}</code>', reply_markup = builder.as_markup())

			else: await message.answer('Syntax: /webprice url')
		else: await message.answer('Syntax: /webprice url')
	else:pass

	print('  NEW_WEBPRICE    ', message)


async def newprice(message: types.message):
	
	if message.from_user.id in config.elite_ids:
		if message.document == None:
		    await message.answer('Отправьте файл с подписью /newprice')
		else:
		    global price_id
		    price_id = message.document.file_id
		    
		    with open(BASE_DIR+'/data/file_ids', 'r') as fin:
		        lines = fin.readlines()
		        lines[0] = message.document.file_id
		        
		        with open(BASE_DIR+'/data/file_ids', 'w') as fout:
		            lines[0] = lines[0].replace('\n', '')
		            lines[1] = lines[1].replace('\n', '')
		            lines[2] = lines[2].replace('\n', '')
		            fout.write(f'''{lines[0]}\n{lines[1]}\n{lines[2]}''')
		            fout.close()
		        fin.close()

		    builder = InlineKeyboardBuilder()
		    builder.row(types.InlineKeyboardButton(text="Уведомление пользователям", callback_data="newprice_resend"))
		    await message.answer(f'ID Прайса успешно изменено на \n<code>{price_id}</code>', reply_markup = builder.as_markup())
	else:pass

	print('  NEWPRICE    ', message)
	

async def newdocument(message: types.message):
	
	if message.from_user.id in config.elite_ids:
		if message.document == None:
		    await message.answer('Отправьте файл с подписью /newdocument')
		else:
		    global document_id
		    document_id = message.document.file_id
		    
		    with open(BASE_DIR+'/data/file_ids', 'r') as fin:
		        lines = fin.readlines()
		        lines[1] = message.document.file_id
		        
		        with open(BASE_DIR+'/data/file_ids', 'w') as fout:
		            lines[0] = lines[0].replace('\n', '')
		            lines[1] = lines[1].replace('\n', '')
		            lines[2] = lines[2].replace('\n', '')
		            fout.write(f'''{lines[0]}\n{lines[1]}\n{lines[2]}''')
		            fout.close()
		        fin.close()
		    await message.answer(f'ID Договора успешно изменен на \n<code>{document_id}</code>')    
	else:pass

	print('  NEWDOCUMENT    ', message)
	

async def newvideo(message: types.message):
	
	if message.from_user.id in config.elite_ids:
		if message.video == None:
		    await message.answer('Отправьте файл с подписью /newvideo')
		else:
		    global video_id
		    video_id = message.video.file_id
		    
		    with open(BASE_DIR+'/data/file_ids', 'r') as fin:
		        lines = fin.readlines()
		        lines[2] = message.video.file_id
		        
		        with open(BASE_DIR+'/data/file_ids', 'w') as fout:
		            lines[0] = lines[0].replace('\n', '')
		            lines[1] = lines[1].replace('\n', '')
		            lines[2] = lines[2].replace('\n', '')
		            fout.write(f'''{lines[0]}\n{lines[1]}\n{lines[2]}''')
		            fout.close()
		        fin.close()
		    await message.answer(f'ID Видео успешно изменено на \n<code>{video_id}</code>')    
	else:pass

	print('  NEWVIDEO    ', message)
	

async def accept_msg_delete(message: types.message):

	await bot.delete_message(message.chat.id, message.message_id)

	print('  NEWMEMBER_MSG_DELETED    ', message)


async def delivery(message: types.message):

	await message.answer(btns.faq_a[1])

	print('  DELIVERY    ', delivery)


async def payment(message: types.message):

	await message.answer(btns.faq_a[2])

	print('  PAYMENT    ', message)


async def garranty(message: types.message):

	await message.answer(btns.faq_a[4])
	print('  GARRANTY    ', message)


async def cours(message: types.message):

	await message.answer_video(caption = btns.cours, video = video_id)

	print('  COURS    ', message)

	
async def review(message: types.message):

	await message.answer(text = btns.review)

	print('  REVIEW    ', message)


async def seller(message: types.message):

	hl = hlink('продавцу', 't.me/Fenrir322')
	answer = f'{message.chat.first_name}, можете написать напрямую {hl}, а так же задать свой вопрос здесь, вам ответит оператор !'
	await message.answer(answer)

	print('  SELLER    ', message)


async def faq2(message: types.message):
	await message.answer(btns.faq_a[1])
	print('  FAQ2_MSG    ', message)
	
async def faq3(message: types.message):
	await message.answer(btns.faq_a[3])
	print('  FAQ3_MSG    ', message)
	
async def faq4(message: types.message):
	await message.answer(btns.faq_a[2])
	print('  FAQ4_MSG    ', message)
	
async def faq5(message: types.message):
	await message.answer(btns.faq_a[4])
	print('  FAQ5_MSG    ', message)

async def faq6(message: types.message):
	await message.answer(btns.faq_a[-1])
	print('  FAQ6_MSG    ', message)

async def rules(message: types.message):
	await message.answer(btns.rules)
	print('  RULES    ', message)


@r.chat_join_request()
async def join_request(update: types.ChatJoinRequest, bot: Bot):

	main_text = (f'''Здравствуйте. {update.from_user.first_name}
В Double front вы можете приобрести новые видеокарты, а также остальные комплектующие из Китая.
Цены на комплектующие указаны в таблице, стоимость и сроки доставки можно узнать в F.A.Q.

Последовательность заказа:
-Выбор модели (Доставка Китай-Москва считается отдельно)
-Консультация с продавцом @Fenrir322
-Подписание договора купли продажи(18+)
-Оплата
-После оплаты в течении 3-5 дней вам отправляем фото и видео отчет

Если у вас остались вопросы, посмотрите раздел F.A.Q. или напишите ваш вопрос''')
	hl = hlink('таблице', web_price_id)
	await bot.send_message(update.from_user.id, text=main_text, reply_markup = keyboard)
	await bot.send_message(update.from_user.id, f'Актуальный прайс смотрите в {hl}', disable_web_page_preview=True)
	await bot.approve_chat_join_request(update.chat.id, update.from_user.id)

	print('  JOIN_REQ    ', update)


@dp.callback_query(Text(text = 'newprice_resend'))
async def join_request_succes(call: types.CallbackQuery):
	
	await call.message.edit_text(call.message.text, reply_markup = InlineKeyboardBuilder().as_markup())
	print('  NEWPRICE_RESEND    ',call) 


@dp.callback_query(lambda c: 'faq_cl' in c.data)
async def faq_cl(call: types.CallbackQuery):

	if int(call.data[6:]) == 0:
		await call.message.delete()
		await call.message.answer_document(caption = 'Договор я отправляю уже заполненный с своей стороны вы его распечатываете  и тоже заполняете от руки потом отправляете мне в формате (фото,скан)', document = document_id)
	else:
		await call.message.edit_text(btns.faq_btns_text[int(call.data[6:])])
		await call.message.answer(btns.faq_a[int(call.data[6:])])

	print('  FAQ_INLINE    ', call)



dp.message.register(accept_msg_delete, F.new_chat_members)

#start
dp.message.register(start, F.chat.type == "private", filters.Command(commands = ['start', 'START', 'Start', 'sratr']))
dp.message.register(start, F.chat.type == "private", lambda msg: msg.text and Levenshtein.ratio(msg.text, "start") > 0.7)
dp.message.register(start, F.chat.type == "private", lambda msg: msg.text and Levenshtein.ratio(msg.text, "старт") > 0.7)


#price_def
dp.message.register(price_def, F.chat.type == "private", lambda msg: msg.text and Levenshtein.ratio(msg.text, "прайс") > 0.7)
dp.message.register(price_def, F.chat.type == "private", lambda msg: msg.text and Levenshtein.ratio(msg.text.lower(), "получить прайс") > 0.75)
dp.message.register(price_def, F.chat.type == "private", lambda msg: msg.text and Levenshtein.ratio(msg.text.lower(), "какая цена") > 0.75)
dp.message.register(price_def, F.chat.type == "private", lambda msg: msg.text and Levenshtein.ratio(msg.text.lower(), "цена") > 0.75)
dp.message.register(price_def, F.chat.type == "private", lambda msg: msg.text and Levenshtein.ratio(msg.text.lower(), "цены") > 0.75)
dp.message.register(price_def, F.chat.type == "private", lambda msg: msg.text and Levenshtein.ratio(msg.text, "сколько стоит") > 0.5)

#delivery
dp.message.register(delivery, F.chat.type == "private", lambda msg: msg.text and Levenshtein.ratio(msg.text, "доставка") > 0.5)


#review
dp.message.register(review, F.chat.type == "private", lambda msg: msg.text and Levenshtein.ratio(msg.text.lower(), "отзыв") > 0.5)


#seller

dp.message.register(faq6, F.chat.type == "private", lambda msg: msg.text and Levenshtein.ratio(msg.text, btns.faq_btns_text[5]) > 0.7)

dp.message.register(seller, F.chat.type == "private", lambda msg: msg.text and Levenshtein.ratio(msg.text.lower(), "Написать продавцу") > 0.5)
dp.message.register(seller, F.chat.type == "private", lambda msg: msg.text and Levenshtein.ratio(msg.text.lower(), "продавец") > 0.6)
dp.message.register(seller, F.chat.type == "private", lambda msg: msg.text and Levenshtein.ratio(msg.text.lower(), "заказать") > 0.5)
dp.message.register(seller, F.chat.type == "private", lambda msg: msg.text and Levenshtein.ratio(msg.text.lower(), "Кому писать для заказа") > 0.5)
dp.message.register(seller, F.chat.type == "private", lambda msg: msg.text and Levenshtein.ratio(msg.text.lower(), "Кому писать") > 0.5)


#cours
dp.message.register(cours, F.chat.type == "private", lambda msg: msg.text and Levenshtein.ratio(msg.text, "курс") > 0.5)
dp.message.register(cours, F.chat.type == "private", lambda msg: msg.text and Levenshtein.ratio(msg.text, "Где посмотреть курс USDT ?") > 0.5)
dp.message.register(cours, F.chat.type == "private", lambda msg: msg.text and Levenshtein.ratio(msg.text, "usdt") > 0.5)


#garranty
dp.message.register(garranty, F.chat.type == "private", lambda msg: msg.text and Levenshtein.ratio(msg.text.lower(), "Гарантия") > 0.5)


#payment
dp.message.register(payment, F.chat.type == "private", lambda msg: msg.text and Levenshtein.ratio(msg.text, "оплата") > 0.5)
dp.message.register(payment, F.chat.type == "private", lambda msg: msg.text and Levenshtein.ratio(msg.text, "способ оплаты") > 0.5)


#faq_msg
dp.message.register(faq2, F.chat.type == "private", lambda msg: msg.text and Levenshtein.ratio(msg.text, btns.faq_btns_text[1]) > 0.7)
dp.message.register(faq3, F.chat.type == "private", lambda msg: msg.text and Levenshtein.ratio(msg.text, btns.faq_btns_text[2]) > 0.7)
dp.message.register(faq4, F.chat.type == "private", lambda msg: msg.text and Levenshtein.ratio(msg.text, btns.faq_btns_text[3]) > 0.7)
dp.message.register(faq5, F.chat.type == "private", lambda msg: msg.text and Levenshtein.ratio(msg.text, btns.faq_btns_text[4]) > 0.7)
dp.message.register(faq6, F.chat.type == "private", lambda msg: msg.text and Levenshtein.ratio(msg.text, btns.faq_btns_text[5]) > 0.7)
dp.message.register(faq3, F.chat.type == "private", lambda msg: msg.text and Levenshtein.ratio(msg.text, 'Время и стоимость') > 0.7)
dp.message.register(faq3, F.chat.type == "private", lambda msg: msg.text and Levenshtein.ratio(msg.text, 'Время') > 0.7)
dp.message.register(faq3, F.chat.type == "private", lambda msg: msg.text and Levenshtein.ratio(msg.text, 'стоимость') > 0.7)
dp.message.register(faq3, F.chat.type == "private", lambda msg: msg.text and Levenshtein.ratio(msg.text, 'сроки') > 0.7)

dp.message.register(faq_msg, F.chat.type == "private", lambda msg: msg.text and Levenshtein.ratio(msg.text, "вопрос") > 0.7)
dp.message.register(faq_msg, F.chat.type == "private", lambda msg: msg.text and Levenshtein.ratio(msg.text, "F.A.Q - Задать вопрос") > 0.5)
dp.message.register(faq_msg, F.chat.type == "private", lambda msg: msg.text and Levenshtein.ratio(msg.text, "F.A.Q") > 0.5)


#document
dp.message.register(document, F.chat.type == "private", lambda msg: msg.text and Levenshtein.ratio(msg.text, "Договор") > 0.5)
dp.message.register(document, F.chat.type == "private", lambda msg: msg.text and Levenshtein.ratio(msg.text, "Документ") > 0.5)


#newfiles
dp.message.register(newprice, F.chat.type == "private", filters.Command(commands = ['newprice'], ))
dp.message.register(newdocument, F.chat.type == "private", filters.Command(commands = ['newdocument']))
dp.message.register(newvideo, F.chat.type == "private", filters.Command(commands = ['newvideo']))
dp.message.register(webprice, F.chat.type == "private", filters.Command(commands = ['webprice']))

#rules
dp.message.register(rules, F.chat.type == "private", filters.Command(commands = ['rules']))
dp.message.register(rules, F.chat.type == "private", filters.Command(commands = ['rule']))
dp.message.register(rules, F.chat.type == "private", lambda msg: msg.text and Levenshtein.ratio(msg.text, "rules") > 0.7)
dp.message.register(rules, F.chat.type == "private", lambda msg: msg.text and Levenshtein.ratio(msg.text, "rule") > 0.7)
dp.message.register(rules, F.chat.type == "private", lambda msg: msg.text and Levenshtein.ratio(msg.text, "Правила") > 0.5)
dp.message.register(rules, F.chat.type == "private", lambda msg: msg.text and Levenshtein.ratio(msg.text, "Правила группы") > 0.5)


#other messages
dp.message.register(my_msg, F.chat.type == "private")
dp.message.register(msg)



dp.include_router(r)
async def main():
	await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
	asyncio.run(main())