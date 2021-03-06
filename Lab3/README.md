#Lab3
##Gimiranov Erik, KP-42

###Розробка засобів кешування з використанням redis

####Завдання роботи полягає у наступному:

1. Встановити сервер redis.

2. Розробити модуль кешування на основі пакету redis-py.

3. Підготувати тестові дані (50-100тис. документів MongoDB).

4. Реалізувати збереження результатів пошуку в базі даних redis (створити
кеш).

5. Реалізувати функцію отримання результатів пошуку з кешу, у випадку,
коли основна база даних не оновлювалась до створення кешу.

####Функціональні вимоги:

1. Згенерувати набір даних бази даних MongoDB у кількості 50-100 тис.
документів згідно із предметною галуззю.

2. Забезпечити створення кешу та підтримку його у актуальному стані за
допомогою сервера redis. Ключем кешу вибрати параметри пошуку,
обрані користувачем.

3. Перевірити швидкість отримання результатів пошуку з використанням
кешу та без нього.

####Screenshots:
![Screen1](https://s17.postimg.org/juanbfizj/screen3lab3.png)
![Screen2](https://s17.postimg.org/6stjzbjz3/screen1lab3.png)
![Screen3](https://s17.postimg.org/m09jjobtr/screen2lab3.png)
