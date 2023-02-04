import configparser
import functions

settings = configparser.ConfigParser()
settings.read('settings.ini')

#base_settings
TOKEN = settings['settings']['TOKEN']
admin = 370028521 #settings['settings']['admin']
cover = 'me.jpg'

status = '🔴'

#text
bio = "Меня зовут Марк и я умею писать на Python🐍\nМои первые шаги в обучении программированию начались в 14 лет🧑‍💻, " \
        "тогда я пытался писать простенькие игры\nСейчас же сфера моих интересов расширилась💻\nСписок моих начинаний начинается от " \
        "разработки телеграмм ботов🤖 и до смарт-контрактов на Solidity🧬\n\nСейчас мне 19 лет я учусь в ВУЗе на специальности 'программная инженерия'👾 " \
        "И имею за плечами курсы от Яндекс.Лицея🟨⬜️\n\n" \
        "Теперь я хочу делать что-то, что принесёт людям пользу, собственно, я открыт для предложений⚡️"
go_to_dialog = 'Ты можешь задать мне вопрос❔\nПросто напиши сообщение, и я с тобой свяжусь📲'
start = f'Это бот-визитка Марка, тут можно узнать о его деятельности и задать пару вопросов\nБудь, как дома🏠\n{functions.get_status()} '
thank_you = "спасибо за вопрос📈"

#buttons_label
button_bio = 'Обо мне🧸'
button_go_to_dialog = "Задай свой вопрос🫧"
button_link = "GitHub👽"
link = 'https://github.com/auternous'

