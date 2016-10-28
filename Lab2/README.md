# Lab2MongoDB
Gimiranov Erik, KP-42
####Завдання роботи полягає у наступному:

1. Розробити схему бази даних на основі предметної галузі з ЛР№2-Ч1 у
спосіб, що застосовується в СУБД MongoDB.
2. Розробити модуль роботи з базою даних на основі пакету PyMongo.
3. Реалізувати дві операції на вибір із використанням паралельної обробки
даних Map/Reduce.
4. Реалізувати обчислення та виведення результату складного агрегативного
запиту до бази даних з використанням функції aggregate() сервера
MongoDB.

####Тексти функції Map/Reduce та aggregate():
map = Code("""

				   function(){
					    var clientName = this.client.name;
					    this.product.forEach(function(z) {
						    emit(clientName, z.price);
					    });
           };
           """)
           
reduce = Code("""

					  function(key, valuesPrices){
						  var sum = 0;
						  for (var i = 0; i < valuesPrices.length; i++) {
						    sum += valuesPrices[i];
						  }
						  return sum;
            };
            """)

pipeline = [

			{"$unwind": "$product"},
			{"$group": {"_id": "$product.title", "count": {"$sum": 1}}},
			{"$sort": SON([("count", -1)])}
		]
    
#### Screenshots:
![Screen1](https://s10.postimg.org/i4vtp6lc7/Screenshot_from_2016_10_10_10_36_37.png)
![Screen2](https://s13.postimg.org/s3v25g7id/Screenshot_from_2016_10_10_10_37_09.png)
