import requests
from urllib.parse import urlparse
import os
from dotenv import load_dotenv
import argparse



def shorten_link(api_token, link): #функция для сокращения ссылок
    url = "https://api.vk.ru/method/utils.getShortLink" #Вк ссылка через которую сокращается ввденная ссылка
    payload = {
        "url": link,#Показываем программе какую ссылку нужно преобразовать
        "access_token": api_token,#Для работы вк
        "v": 5.199
    }
    response = requests.get(url, params=payload)#Запрашиваем сокращение ссылки
    response.raise_for_status()#Проверяем дошел ли запрос
    return response.json()["response"]["short_url"]#Возвращаем сокращенную ссылку

    

def count_cliks(api_token, link): #функция для счета ссылок
    parsed_link = urlparse(link) #Делим ссылку на части
    key = parsed_link.path.split("/") #Достаем часть после vk.cc
    url = "https://api.vk.ru/method/utils.getLinkStats" #Вк ссылка через которую мы считаем клики
    payload = {
        "key": key[1],
        "v": 5.199,
        "access_token": api_token,
    }
    response = requests.get(url, params=payload)#Запрашиваем сокращение ссылки
    response.raise_for_status()#Проверяем дошел ли запрос
    return response.json()["response"]["stats"][0]["views"] #Возвращаем кол-во кликов по ссылке
    # return response.json()



def is_shorten_link(api_token, link): #функция для проверки ссылки на сокращенность
    url = "https://api.vk.ru/method/utils.getLinkStats" #Вк ссылка через которую мы проверяем ссылку на сокращенность
    parsed_link = urlparse(link) #Делим ссылку на части
    key = parsed_link.path.split("/") #Достаем часть после vk.cc
    payload = {
        "key": key[1],
        "v": 5.199,
        "access_token": api_token,
    }
    response = requests.get(url, params=payload)#Запрашиваем сокращение ссылки
    response.raise_for_status()#Проверяем дошел ли запрос
    return "response" in response.json()#Есть ли в response.json response


def main():
    load_dotenv()
    api_token = os.environ['VK_API_TOKEN']
    # link = input("Введите ссылку: ")
    parser = argparse.ArgumentParser(description="Сокращает ссылку и считает клики по ней с помощью Vk-API")
    parser.add_argument('link', type=str, help="Ссылка на страницу")
    args = parser.parse_args()
    try:#Блок проверки
        if is_shorten_link(api_token, args.link):    #если сокращенная ссылка
            cliks = count_cliks(api_token, args.link)
            print(cliks)#запускаем функцию
        else:                                   #если не сокращенная ссылка
            short_link = shorten_link(api_token, args.link) 
            print(short_link)#запускаем функцию
    except KeyError:#Если ошибка
        print("Ссылка указана неверно")
    except IndexError:#Если ошибка
        print("Кликов по ссылке не было")

if __name__ == "__main__":
    main()