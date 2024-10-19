import requests
from urllib.parse import urlparse
import os
from dotenv import load_dotenv
import argparse


def shorten_link(api_token, link):
    url = "https://api.vk.ru/method/utils.getShortLink" 
    payload = {
        "url": link,
        "access_token": api_token,
        "v": 5.199
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    return response.json()["response"]["short_url"]

    
def count_cliks(api_token, link): 
    parsed_link = urlparse(link) 
    key = parsed_link.path.split("/") 
    url = "https://api.vk.ru/method/utils.getLinkStats" 
    payload = {
        "key": key[1],
        "v": 5.199,
        "access_token": api_token,
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    return response.json()["response"]["stats"][0]["views"] 


def is_shorten_link(api_token, link): 
    url = "https://api.vk.ru/method/utils.getLinkStats" 
    parsed_link = urlparse(link) 
    key = parsed_link.path.split("/") 
    payload = {
        "key": key[1],
        "v": 5.199,
        "access_token": api_token,
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    return "response" in response.json()


def main():
    load_dotenv()
    api_token = os.environ['VK_API_TOKEN']
    parser = argparse.ArgumentParser(description="Сокращает ссылку и считает клики по ней с помощью Vk-API")
    parser.add_argument('link', type=str, help="Ссылка на страницу")
    args = parser.parse_args()
    try:
        if is_shorten_link(api_token, args.link):   
            cliks = count_cliks(api_token, args.link)
            print(cliks)
        else:                                  
            short_link = shorten_link(api_token, args.link) 
            print(short_link)
    except KeyError:
        print("Ссылка указана неверно")
    except IndexError:
        print("Кликов по ссылке не было")


if __name__ == "__main__":
    main()