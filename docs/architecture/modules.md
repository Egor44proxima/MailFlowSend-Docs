# Runtime modules

MailFlowSend використовує modular runtime із versioned ABI.

Поточний baseline:

~~~text
ABI 1
~~~

Module host має контролювати lifecycle, error boundaries та unload safety. Module failure не повинен створювати silent business-state mutation.
