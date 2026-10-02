# Відновлення та безпека

Recovery subsystem має окремі readiness gates, backup catalog та restore evidence.

Безпечні правила:

- не видаляти WAL/SHM вручну як ремонт;
- не переписувати manifests;
- не підміняти restore ручним копіюванням файлів під час активної роботи;
- не використовувати recovery для зміни immutable delivery/history evidence;
- diagnostic failure не є автоматичною підставою для restore.

Перед restore перевіряються readiness, backup integrity та відсутність активних операцій, які можуть конфліктувати з відновленням.
