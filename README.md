# Требуется
1. Python 3.6 и выше
2. Система Linux

### Queue REDIS
Обязательно требуется редис, для работы асинхронных задач.
Что бы запустить воркер, необходимо ввести через `supervisorctl1`
```shell
python3 worker.py
```

Все задачи должны лежать в папке `App/Jobs` и быть подписанным на контракт `JobContract`
```text
Подпись на контракт это обязательное имплементирование
методов который требует интерфейс.
Все задачи которые скопированы но не входящие в контракт, будут отброшены

```
Вызывать задачу достаточно легко, необходимо придерживаться структура расположения входных атрибутов
```python
from App.Jobs import TestJob
TestJob.dispatch(a=1, b="2")
```
