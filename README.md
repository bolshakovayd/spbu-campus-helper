# spbu-campus-helper
[Презентация проекта](https://docs.google.com/presentation/d/1PqykPoWtQMUStxEYumRljzamU94FKUVrGeJ4StjKZFg/edit?usp=sharing)

# Развертывание на Heroku
Для начала настроим платформу для развертывания.
0. Регистриемся на [Heroku](https://www.heroku.com).
1. Устанавливаем и авторизируемся в [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli):
Для Debian-based дистрибутивов (Ubuntu, GNU/Debian):
```shell
$ curl https://cli-assets.heroku.com/install-ubuntu.sh | sh
```
Для Arch-based дистрибутивов (Arch Linux, Manjaro):
```shell
$ yay -S heroku-cli
```
затем
```shell
$ heroku login
```
2. [Создаем приложение Heroku](https://devcenter.heroku.com/articles/creating-apps) и подключаем локальный Git репозиторий:
```shell
$ heroku create <HEROKU APP NAME>
$ heroku git:remote -a
```
4. Устанавливаем Python Buildpack:
```shell
$ heroku buildpacks:set heroku/python
```
5. Теперь пора зарешистрировать самого бота:
  Заходим к @BotFather в Telegram, создаем бота.
5. В файле `config.py` выставляем
  1) `<TELEGRAM BOT TOKEN>` - токен бота, полученный у @BotFather в Telegram.
  2) `<HEROKU APP NAME>` - имя Heroku приложения.
  3) `<SPBU stxxxxxx LOGIN>` и `<SPBU PASSWORD>` - данные для авторизации на сайте [Dormitory Availability](https://campus-free.spbu.ru).
6. Заливаем на Heroku посредством Git:
```shell
$ git push heroku master
```
