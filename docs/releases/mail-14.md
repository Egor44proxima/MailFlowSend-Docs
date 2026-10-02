# MAIL-14 · Deterministic Spintax

MAIL-14 додав deterministic Spintax engine та operator runtime control.

## Основні властивості

- isolated parser/validator/renderer;
- deterministic variant selection;
- canonical Core rendering;
- kill-switch;
- fail-closed behavior;
- raw {a|b} syntax не повинна потрапляти у send payload при disabled feature;
- immutable dispatch freeze: retry/resend не rerollить контент.

Runtime control має precedence:

~~~text
environment override
→ persisted operator preference
→ safe default OFF
~~~

Зміна preference впливає на майбутні preview/freeze, а не на вже frozen dispatches.
