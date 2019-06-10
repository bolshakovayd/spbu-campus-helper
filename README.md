# spbu-campus-helper
[Презентация проекта](https://docs.google.com/presentation/d/1PqykPoWtQMUStxEYumRljzamU94FKUVrGeJ4StjKZFg/edit?usp=sharing)

# Развертывание
Необходим аккаунт на [Heroku](https://www.heroku.com).
1. Устанавливаем и авторизируемся в [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
2. [Создаем приложение Heroku](https://devcenter.heroku.com/articles/creating-apps), устанавливаем Python Buildpack:
```$ heroku buildpacks:set heroku/python```
3. В файле `config.py` выставляем `<TELEGRAM BOT TOKEN>` -- токен бота, полученный у @BotFather, `<HEROKU APP NAME>` -- имя Heroku приложения, `<SPBU stxxxxxx LOGIN>` и `<SPBU PASSWORD>` -- данные для авторизации на сайте.
4. Заливаем на Heroku посредством Git.
