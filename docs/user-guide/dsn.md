# DSN

**DSN огляд** працює з inbound delivery-status evidence та correlation review.

~~~text
CORRELATED
AMBIGUOUS
UNMATCHED
~~~

DSN parser/correlation не повинен вгадувати recipient identity. Ambiguous або unmatched evidence зберігається для review без небезпечного projection rewrite.

!!! note
    DSN artifact — це evidence. Він не є командою на автоматичний retry/resend.
