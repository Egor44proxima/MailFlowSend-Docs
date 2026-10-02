# Дані та SQLite

Поточний baseline:

~~~text
Schema v53
~~~

SQLite є canonical persistence layer для business state та bounded technical observability.

Різні owners включають clients/contact registry, campaigns/dispatch snapshots, Queue/attempts, Delivery/DSN evidence, History projections, Recovery metadata та application logging.

!!! warning
    Не редагуйте canonical SQLite вручну для виправлення business state.
