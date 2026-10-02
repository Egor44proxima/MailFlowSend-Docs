# Інсталяція та запуск

Публічна документація не фіксує конкретні production paths. Використовуйте офіційний зібраний пакет MailFlowSend і затверджений runtime data directory.

## Development stack

~~~text
Go
Wails
Node.js / npm
SQLite
~~~

Поточний baseline: Core 0.16.9, schema v53, ABI 1.

## Перед запуском

1. Перевірте runtime mode.
2. Перевірте canonical SQLite DB.
3. Перевірте runtime modules.
4. Для production send перевірте SMTP profile та credentials через підтримуваний механізм.
5. Не змішуйте DEV і PROD databases.
