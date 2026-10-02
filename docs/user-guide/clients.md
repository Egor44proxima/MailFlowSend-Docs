# Клієнти

Workspace **Клієнти** — canonical registry для бізнес-клієнтів та контактних даних.

## Основні можливості

- пошук і фільтри;
- quick view клієнта;
- cooperation status;
- контакти;
- CSM binding;
- duplicate/data-quality evidence;
- navigation до пов'язаних workspace.

## Safety rules

- клієнти не створюються автоматично під час matching;
- fuzzy matching є advisory only;
- ambiguous match не створює canonical binding;
- зміна cooperation status не переписує historical evidence.

!!! tip
    Якщо email клієнта відсутній, відправка має блокуватися policy, а не підставляти невідому адресу.
