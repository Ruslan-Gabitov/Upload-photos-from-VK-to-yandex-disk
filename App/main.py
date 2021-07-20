import requests
from pprint import pprint
import time
from tqdm import tqdm
import os
from dotenv import load_dotenv
import datetime
import argparse

class Vcontakte:
    def __init__(self, token, rev=True, count=5):
        self.token = token
        self.rev = rev
        self.count = count

    def get_profile_photos_url(self, id):
        profile_photos_url = []
        url = "https://api.vk.com/method/photos.get"
        params = {
            "access_token": self.token,
            "v": "5.131",
            "owner_id": id,
            "album_id": "profile",
            "photo_sizes": True,
            "rev": self.rev,
            "count": self.count,
            "extended": True,
        }
        responce = requests.get(url, params=params)
        for sizes_fotos in responce.json()["response"]["items"]:
            profile_photos_url.append(
                {
                    "likes": sizes_fotos["likes"]["count"],
                    "type": sizes_fotos["sizes"][-1]["type"],
                    "url": sizes_fotos["sizes"][-1]["url"],
                    "date": sizes_fotos["date"]
                }
            )

        return profile_photos_url
    
    def get_id_by_short_name(self, user_name):
        url = "https://api.vk.com/method/utils.resolveScreenName"
        params = {
            "access_token": self.token,
            "v": "5.131",
            "screen_name": user_name
            }
        responce = requests.get(url, params=params)
        if user_name.isdigit():
            return user_name
        else:    
            return responce.json()['response']['object_id']



class YaDisck:
    def __init__(self, token, url_downloadable_files):
        self.token = token
        self.url_downloadable_files = url_downloadable_files

    def get_headers(self):
        return {
            "Authorization": f"OAuth {self.token}",
            "Content-Type": "application/json",
        }

    def create_folder_yadisck(self, folder_name):
        params = {"path": "disk:/{}/".format(folder_name)}
        headers = self.get_headers()
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        response = requests.put(url, headers=headers, params=params)
        response.raise_for_status
        return folder_name

    def download_yandex_disk(self, folder_name):
        dik = []
        headers = self.get_headers()
        url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        for urls in tqdm(self.url_downloadable_files):
            if urls["likes"] not in dik:
                dik.append(urls["likes"])
                path = "disk:/{}/{}.jpg".format(folder_name, urls["likes"])
            else:
                dik.append(urls["likes"])
                value = datetime.datetime.fromtimestamp(urls["date"])
                path = "disk:/{}/{}{}.jpg".format(
                    folder_name, urls["likes"], f"{value:-%Y-%m-%d}"
                )
            params = {"path": path, "url": urls["url"]}
            time.sleep(1)
            response = requests.post(url, headers=headers, params=params)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Программа сохраняет последние загруженные фото профиля(аватары) на яндекс диск')
    parser.add_argument('user_id', help='Ввидите user_name или ID пользователя')
    parser.add_argument('-c', '--count', help='Ввидите количество фото которые хотите сохранить(defoult = 5)')
    args = parser.parse_args()

    load_dotenv()

    vk = Vcontakte(token=os.getenv('VK_TOKEN'), count=args.count)
    ya_disck = YaDisck(
        token=os.getenv('YA_TOKEN'), url_downloadable_files=vk.get_profile_photos_url(id=vk.get_id_by_short_name(args.user_id))
    )
    folder_name = ya_disck.create_folder_yadisck(folder_name = "vkontakte")
    ya_disck.download_yandex_disk(folder_name)
