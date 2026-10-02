# Кампанії

MailFlowSend підтримує контрольований lifecycle кампанії від authoring до immutable dispatch snapshot.

~~~text
Draft
→ recipients / attachments / template
→ preflight
→ recipient resolution
→ eligibility
→ immutable dispatch snapshot
→ Queue
~~~

Після freeze Queue/Retry/SMTP використовують frozen payload. Зміна шаблону або runtime Spintax preference не повинна перегенеровувати вже зафіксований dispatch.

Підтримувані business flows включають DOCUMENTS, DEBT та GENERAL сценарії.
