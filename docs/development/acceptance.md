# Acceptance workflow

MailFlowSend використовує evidence-driven development workflow:

~~~text
DESIGN
→ implementation
→ targeted tests
→ DEV runtime acceptance
→ current/FAST gate
→ fixes
→ Windows runtime acceptance
→ FULL/current gate
→ documentation closure
→ merge
→ post-merge clean-checkout CI
~~~

Acceptance marker не можна синтезувати заднім числом.

Git discipline:

- feature branch;
- exact SHA evidence;
- CI before merge;
- runtime acceptance before closure;
- post-merge CI на exact new main SHA.
