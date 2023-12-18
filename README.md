<b>Описание:</b>
Данное приложение является микросервисом, который автоматически сапостовляет пользовательский запрос с названиями городов сервиса https://www.geonames.org/ при помощи модели TF-IDF (Term frequency–inverse document frequency).

<b>Описание работы сервиса:</b>
1. Приложение получает на вход строку с названием города. 
2. Идет проверка, существуют ли данные в БД. Если нет, идет закачка данных непосредственно с сервиса geonames.org. 
3. Далее идет предобработка данных и запись итогового датафрейма в БД.
4. Если данные уже были загружены в БД, то они считываются прямо из базы.
5. Запрос пользователя сравниваеся с именами и альтернативными именами городов. 
6. Если максимальное косинусное сходство составило менее 0.99, происходит транслитерация запроса пользователя и повторная прогонка нового запроса через алгоритм. В результате работы двух ступеней идет отбор записей с максимальным косинусным сходством.
7. Далее идет построение итогового датафлейма с результатами работы алгоритма. Дополнительно выводятся данные в виде списка словарей.
8. Сервис наделен функционалом добавления геолокаций в БД. Если в результате обработки пользовательского запроса верной локации обнаружено не было, ее можно добавить вручную. При повторной проверке даные будут содержаться в БД и смогут выдать верный результат.


<b>Выходные данные:</b>
1. Таблица с 5-ю наиболее релевантными названиями городов, включающая в себя
- Название города в кодировке ascii, city_ascii_name
- Регион/область, region_name
- Страна, country
- Косинусное сходство, cosine_similarity
2. Список словарей, содержащих данные из таблицы.

<b>Применяемый стек технологий:</b>
- Python 3.11
- Docker compose
- Database Postgres
- ASGI web server Unicorn

<b>Используемые библиотеки и фреймворки:</b>
- SQLAlchemy
- TfIdfVectorizer 
- FastAPI
- Bootstrap 5

На базе приложения разработан самодостаточный микросервис.
Cтраница сервиса https://geonames.svoj.by/

