# Описание программы:
Программа скачивает 5 последних фотографий профиля (автар) социальной сети Vkontakte максимального размера и автоматически сохраняет на яндекс диск.

#### Установка зависимостей:
```
pip install -r requirements.txt
```
Так же вам понадобятся токены доступа для [Yandex](https://yandex.ru/dev/direct/doc/dg/concepts/access.html) и [Vkontakte](https://vk.com/dev/access_token)
Токены необходимо разместить в файле ```App/.env```, как показанно в примере ниже
```
VK_TOKEN=Ваш токен
YA_TOKEN=Ваш токен
```

#### Пример использования:
Вызов справки:
```
$ python3 main.py -h
```
#### Как использовать программу:
После имени файла ```main.py``` необходимо указать короткое имя пользователя либо его ID состоящее из цифр.
Далее можно указать необязательный параметр ```-c --count``` число после него означает количество фотографий которое сохранится на яндекс диск, если его не указывать то по умолчанию сохраниться 5 фотографий.
```
Input
$ python3 App/main.py user_name/ID -c 6

Output
100%|█████████████████████████████████████████████| 6/6 [00:08<00:00,  1.40s/it]
```
Если программа отработала корректно вы увидите загруженный sidebar на 100%