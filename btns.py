
from aiogram.utils.markdown import hlink

main_btns = ["Получить прайс", "Правила группы", "F.A.Q - Задать вопрос", "Написать продавцу"]

hl = hlink('Тинькофф', 'https://p2p.binance.com/en/trade/Tinkoff/USDT?fiat=RUB')
hl1 = hlink('Сбербанк', 'https://p2p.binance.com/en/trade/RosBank/USDT?fiat=RUB')
cours = f'Курс смотрим на криптовалютном обменнике Binance\n{hl1}\n{hl}'

review = 'Канал с отзывами \nt.me/+vzrnZLJLiZI0YTc6'


faq_btns_text = ["Договор", "Шаги по оформлению заказа", "Сроки доставки и стоимость", "Способы оплаты", "Гарантия", "Условия заказа", "Отзывы"]

faq_a = ['',
'''1. Вы выбираете нужный вам товар из прайса и пишите продавцу (@Nikita909Fenrir), что готовы к покупке. Полностью прописываете мне в сообщение то, что вы готовы заказать. 
2. Я подготавливаю договор и скидываю его вам, если все верно, то вы его распечатываете, заполняете от руки, далее скидываете мне его скан или чёткие фотографии. 
Обращаю ваше внимание, что в договоре указывается цена доставки КИТАЙ - МОСКВА. Внимательно прочитайте п.5 и спецификацию.
3. Оплата. 
Когда вы будете готовы к оплате пишите мне «готов к оплате». Мы с вами вместе оплачиваем. Вы можете попросить меня с вами созвониться или отправить видеокружок для подтверждения, что оплату провожу именно я.
4. Через 3-5 дней я скидываю вам видео и фото отчёт. Чуть позже ещё скидываю вам трек номер для отслеживания Китай - Москва. 
5. Когда товар приходит на склад в Москву его передают в транспортную компанию РФ. В основном мы доверяем Желдор (600-1200р.) при получении. Также вы можете выбрать другую транспортную, это может быть чуть дороже, например СДЭК (до 1700 руб.) Это обговаривается сразу при заключении договора.
''',


'''Доставка 10-16 дней до Москвы. Оттуда отправляется транспортной компанией (СДЭК и т.д.). 
Пока товар летит до Москвы, его можно будет отследить через трек-номер. Вы получите трек-номер как посылка будет на терминале аэропорта.

Пример стоимости за доставку:
Видеокарта 3 кг - 80 USDT
Видеокарта 2 кг - 70 USDT
Если в заказе больше позиций или другие комплектующие - цена за доставку уточняется у продавца @Nikita909Fenrir .

Доставка с Китая до Москвы оплачивается при заключение договора (В договоре будет прописана)
Доставка с Москвы до региона оплачивается при получение (СДЭК до 1700 руб.)''',



'''1. По реквизитам указанным в договоре.
2. На расчетный счёт 3 лица (Создаётся ордер на обмен USDT) . Мы предоставляем скидку в 1 000 рублей.''',



f'''Предоставляем гарантию на купленный у нас товар:
	Видеокарта - 2 года гарантии. В случае брака отправляем видеокарту на ремонт ( Отправляем {hlink('VIK-on', 'https://www.youtube.com/c/VIKon-msk')})  ГАРАНТИЮ ПРЕДОСТАВЛЯЕМ МЫ, НЕ VIK-on!!!
	Остальные комплектующие - 1 год гарантии. В случае брака возвращаем денежные средства или отправляем замену.

	Обстоятельства не подлежащему гарантийному случаю описаны в договоре.

	Все расходы, связанные с отправлением товара до пункта проверки товара осуществляется за счет покупателя, в случае признания неисправностей, ремонт и отправление товара покупателю лежат на Продавце''',


'''- Заказ одной позиции доступен: 
 NVIDIA от 20 серии 
 АMD начиная от 6600 и выше
 Блоки питания

- Заказ остальных комплектующих доступен от двух разных позиций 
Пример: ЦП+материнская плата, ССД+ОЗУ и т.д.
'''
]

rules = """
ПРАВИЛА

Во избежание недопонимания со стороны администрации группы, а так же возникновения конфликтных ситуаций,
ЗАПРЕЩАЕТСЯ:
1. Развивать провоцирующие темы, политического и религиозного контекста. Разжигание конфликта в любом его проявлении.
2. Спам и флуд: картинками, стикерами, как комического, порно-эротического, так и оскорбляющего формата. (Более 2-3 стикеров/картинок в 3 минуты)
3. Публикация: наркотических, шокирующих, и подобных материалов.
4. Оскорблять участников группы и администрацию. (За оскорбления в ЛС с администратором, Вы понесёте ответственность и в чате группы) 
5. Отправлять ссылки на сторонние группы, чаты и прочее без согласования с администрацией. Уточните предварительно, администрация всегда в сети!
6. Навязывать участникам группы покупку на Amazon, Computer univers, NewEgg, прочих торговых площадках, о чьей репутации Вы утверждать не в состоянии. Не возводите частный опыт в общую практику!
7. Консультации по покупке комплектующих на сторонних магазинах/площадках, например - AliExpress, ДНС и вышеупомянутых. Любая работа стоит затраченных на нее ресурсов
8. Продавать/покупать личные вещи, для этого есть Авито и аналогичные площадки. Администрация не несёт ответственность если Вам будут пытаться продать что-либо участники группы.
9. Просить занять/купить. Направлять людей к себе в ЛС, расценивается как попытка мошенничества.  
10. Ненормативная лексика. Соблюдайте культуру речи, группа - общественное пространство. (Количество/Рамки регулируется на усмотрение администрации)
11. Запрещено нарушать любые правила платформы Телеграм.

В случае нарушения правил, меры применяются на усмотрение администратора

Насчёт апелляции писать @kataev_av 

Уважайте себя и участников данной группы.
Благодарим за понимание.
"""