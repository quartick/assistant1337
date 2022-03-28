# -*- coding: utf-8 -*-

"""Модуль обработки команд."""
import pickle
import re

# Обработка команд
def words_recog(result):
    with open("Pickle/wordkey.pickle", "rb") as word:
        words = pickle.load(word)

    result = result.lower()
    for key in words:
        for i in range(len(words[key])):
            find_num = r"\b" + f"{words[key][i]}" + r"\b"
            if re.search(find_num, result):
                result = result.replace(words[key][i], key)

    return result

def site_recog(result):
    with open("Pickle/site_base.pickle", "rb") as word:
        site = pickle.load(word)
    result = result.lower()
    for key in site:
        for i in range(len(site[key])):
            find_num = r"\b" + f"{site[key][i]}" + r"\b"
            if re.search(find_num, result):
                result = result.replace(site[key][i], key)

    return result

# База всех команд, для обработки
def key_words():
    words = {"открой": ["открой", "аткрой", "открыть"],
             "сайт": ["сайт", "страница", "страничку"],
             "папку": ["папка", "папку"],
             "система": ["ситема", "сестема", "system", 'система'],
             "время": ["время", "часы"],
             "дата": ["дата", "день", "data"],
             "умеешь": ["умеешь", "уметь", "можешь", "способна",
                        "помощь", "справка"],
             "браузер": ["браузер"],
             "добавить": ["добавить", "добавь"],
             "изменить": ["изменить", "измени"],
             "что": ["что"],
             "пока": ["прощай", "пока"],
             "вконтакте": ["вк", "вконтакте", "vk"],
             "одноклассники": ["одноклассники"],
             "гитлаб": ["гитлаб", "гит", "репозиторий"],
             "интаграм": ["инст", "интаграм", "инстаграмм",
                          "instagram", "instagramm"],
             "екурсы": ["курсы", "екурсы", "сфу"],
             "youtube": ["ютюб", "youtube", "ютюбчик", "видео"],
             "почта": ["мыло", "почта"],
             "яндекс": ["яндекс"],
             "google": ["google", "гугл"],
             "сделай": ["сделай"],
             "где": ["где"],
             "новости": ["новости"],
             "файл": ["файл"],
             "Downloads": ["Downloads", "Загрузки", "загрузки"],
             "Documents": ["Documents", "Документы", "документы", "доки"],
             "Desktop": ["Desktop", "Рабочий", "Стол", "стол", "рабочий"],
             "Picture": ["Picture", "Изображения", "изображения"]}

    with open("Pickle/wordkey.pickle", "wb") as f:
        pickle.dump(words, f)

    with open("Pickle/wordkey.pickle", "rb") as f:
        x = pickle.load(f)

        print(x)


if __name__ == "__main__":
    key_words()
