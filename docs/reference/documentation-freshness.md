# Актуальність документації

MailFlowSend-Docs використовує **source baseline contract**: публічна документація завжди прив'язана до конкретного commit у приватному application repository.

<div id="docs-source-status"></div>

## Контракт

~~~text
MailFlowSend/main
      ↓ compare
Documented Source SHA
      ↓
CURRENT / OUTDATED / UNKNOWN
~~~

### CURRENT

`MailFlowSend/main` точно збігається з `documented_source_sha`. Документація описує поточний accepted source baseline.

### OUTDATED

У `MailFlowSend/main` уже є нові commits після documented baseline.

Це **навмисно не виправляється автоматичним підняттям SHA**. Спочатку потрібно:

1. перевірити, що змінилося в application repo;
2. оновити User Manual / Developer Handbook / Architecture / Release docs, якщо зміни зачіпають їх;
3. пройти `mkdocs build --strict`;
4. тільки після цього оновити `docs/_meta/source-baseline.json` на новий accepted source SHA.

### UNKNOWN

Workflow не зміг перевірити приватний source repository. Найчастіша причина — відсутній або недоступний Actions secret `MAILFLOWSEND_SOURCE_TOKEN`.

## Чому baseline не оновлюється автоматично

Автоматична заміна старого SHA на новий зробила б стару документацію “CURRENT” без перевірки змісту.

Тому правильний fail-closed contract:

~~~text
new source commit
→ OUTDATED
→ documentation review/update
→ deliberate baseline bump
→ CURRENT
~~~

## Автоматична перевірка

GitHub Pages workflow запускається:

- при push у `MailFlowSend-Docs/main`;
- вручну;
- щогодини за schedule.

Під час build він отримує current `MailFlowSend/main` SHA через read-only token, генерує `assets/source-status.json` і публікує status на Pages.

Після deploy окремий **Freshness Gate** завершує workflow помилкою, якщо status не `CURRENT`. Це дає червоний сигнал в GitHub Actions, але сайт при цьому вже опублікований з видимим `OUTDATED` або `UNKNOWN` banner.

## Required secret

У `MailFlowSend-Docs` потрібен repository Actions secret:

~~~text
MAILFLOWSEND_SOURCE_TOKEN
~~~

Рекомендований token:

- Fine-grained personal access token;
- Repository access: **Only select repositories → MailFlowSend**;
- Repository permissions: **Contents: Read-only**;
- без write/admin permissions.

Token не виводиться на Pages і не записується в status JSON.
