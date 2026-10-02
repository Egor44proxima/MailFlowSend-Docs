# Середовище і збірка

Основний application stack:

~~~text
Go
Wails
Vue
Node.js / npm
SQLite
~~~

Для документації:

~~~bash
python -m pip install -r requirements.txt
mkdocs serve
~~~

Strict production build:

~~~bash
mkdocs build --strict
~~~

Публічний docs repository не містить production DB, credentials або приватних runtime artifacts.
