# 19 · Модулі

**Контекст:** READ_ONLY

## Призначення

Workspace **Модулі** показує runtime module discovery, version/ABI compatibility та health. Він призначений для inspection і refresh, а не для довільного unload/replacement під час активної роботи.

## Accepted architecture

MailFlowSend host має один Go/Wails runtime і використовує stable native C ABI boundary для DLL modules.

~~~text
Go/Wails host
→ ModuleHost
→ C ABI v1
→ native DLL module
~~~

ABI v1 contract включає bounded exports на кшталт:

~~~text
MF_ABIVersion
MF_ModuleInfo
MF_Init
MF_Health
MF_Execute
MF_Shutdown
MF_Free
~~~

## Що перевіряти

Для кожного discovered module важливі:

- module name/identity;
- version;
- ABI version;
- load/discovery status;
- health;
- runtime error detail;
- required export compatibility.

## ABI mismatch

Module із несумісним ABI не повинен “частково працювати”. ModuleHost має fail-closed на compatibility boundary.

Поточний application baseline:

~~~text
ABI 1
~~~

## Runtime safety

Production feature modules не повинні завантажувати незалежний Go runtime через Go c-shared DLL у Wails Go host без окремого accepted safety design.

Для Go-native independently updateable features безпечніший direction — process isolation; native extensions можуть використовувати C ABI.

## Operator workflow

1. Відкрити Modules.
2. Натиснути refresh.
3. Перевірити expected module count.
4. Перевірити health/ABI.
5. При failure перейти у **Діагностику** / **Системний журнал**.
6. Не замінювати DLL “на гарячу” вручну під час active operations.

## Safety boundary

- Workspace READ_ONLY.
- Не виконує send.
- Не mutate Queue.
- Не обходить ABI check.
- Не здійснює destructive module lifecycle без окремого accepted operation contract.

## Пов'язані workspace

- **Діагностика** — module subsystem health.
- **Системний журнал** — module lifecycle/error events.
- **Налаштування** — application configuration, але не ABI replacement.
