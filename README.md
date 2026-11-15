# OldSchool Journal

Учебный блог OldSchool Journal переносится с Ruby on Rails на Python и Django. Код Django находится в `django_blog/`. Текущая версия Django показывает стартовую страницу. Очерёдность переноса разделов описана в [плане](docs/DJANGO-PLAN.md).

## Локальный запуск Django на Windows

Откройте PowerShell в папке репозитория `blog`. Для первого запуска выполните команды по порядку. `venv` создаёт отдельное окружение для библиотек этого проекта. `migrate` создаёт нужные таблицы в локальном файле базы SQLite.

```powershell
python -m venv .venv
cd django_blog
..\.venv\Scripts\python.exe -m pip install -r requirements.txt
..\.venv\Scripts\python.exe manage.py migrate
..\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
```

Откройте [http://127.0.0.1:8000](http://127.0.0.1:8000). Для повторного запуска достаточно открыть `blog/django_blog` и выполнить последнюю команду. Сервер останавливается сочетанием `Ctrl+C`. Файл локальной базы `django_blog/db.sqlite3` создаётся автоматически и хранится вне Git.

## Локальный запуск Rails

Откройте терминал в папке `blog`. Установите Ruby 3.3 и Bundler 2.7.1.
В Windows используйте [RubyInstaller с Devkit](https://rubyinstaller.org/downloads/).
Devkit содержит инструменты, которые нужны для сборки некоторых библиотек Ruby.

```text
gem install bundler -v 2.7.1
```

В Windows добавьте поддержку вашей платформы в список версий библиотек:

```text
bundle _2.7.1_ lock --add-platform x64-mingw-ucrt
```

Установите библиотеки, подготовьте локальную базу данных и запустите сайт:

```text
bundle _2.7.1_ install
bundle _2.7.1_ exec ruby bin/rails db:prepare
bundle _2.7.1_ exec ruby bin/rails server -b 127.0.0.1
```

Когда сервер запустится, откройте [http://127.0.0.1:3000](http://127.0.0.1:3000).
Остановить сервер можно сочетанием `Ctrl+C` в терминале.

Данные локального сайта хранятся в `storage/development.sqlite3`. При первом
запуске создаётся новая база. В Git сохранён код проекта и описание структуры
базы. Для возврата старых записей нужен прежний файл базы или его резервная копия.

## Документация

| Файл | Что в нём |
| --- | --- |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | Как Rails открывает страницу, где находятся данные и как проверяются права. |
| [TESTING.md](docs/TESTING.md) | Команды автотестов и шаги проверки в браузере. |
| [STATUS.md](docs/STATUS.md) | Из какой ветки восстановлен блог, что проверено и как продолжить запуск. |
| [DJANGO-PLAN.md](docs/DJANGO-PLAN.md) | Согласованные этапы переноса и проверка результата каждого этапа. |
| [WSL.md](docs/WSL.md) | История настройки WSL, пути установки, расход ресурсов и сравнение Rails с Django. |
| [AGENTS.md](AGENTS.md) | Инструкции для Codex при работе с этим репозиторием. |
