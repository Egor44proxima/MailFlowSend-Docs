# Архітектура

MailFlowSend — Windows desktop application:

~~~text
Vue UI
  ↕ Wails bindings
Go application / Core
  ↕
SQLite canonical state
  ↕
runtime modules / SMTP / filesystem evidence
~~~

## Ownership

- **Vue** — presentation та operator intent.
- **App/Wails layer** — explicit application actions.
- **Core/coredb** — canonical business rules, persistence, evidence projection.
- **SQLite** — canonical state.
- **Runtime modules** — bounded ABI contract.

UI не повинна реконструювати canonical business logic із DOM або локального cache.
