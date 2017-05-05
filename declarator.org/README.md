# Парсер сайта «declarator.org»

(__Python 2.x__) Извлечение информации из деклараций о доходах с сайта `declarator.org`.

## Описание
Для скачивания и первоначальной обработки деклараций использовалась программа Universal Text Extractor. Декларации объединяются в один .csv файл.
Содержимое файла - таблица вида:
- Должностное лицо
- Имущество
- Год
- Должность
- Орган
- Тип декларации
- Ссылка

## Файлы
- [authority_links.txt](authority_links.txt) - перечень органов власти и ссылок на них
- [db_scheme.pdf](db_scheme.pdf) - предполагаемая схема БД
- [example](example) - пример обработки
	- [declarations.csv](example/declarations.csv) - декларации, скачанные и обработанные с помощью Universal Text Extractor
	- [links.txt](example/links.txt) - список ссылок, которые необходимо скачать
	- [organizations.csv](example/organizations.csv) - перечень органов власти и соответствующих регионов
- [project.json](project.json) - проект программы Universal Text Extractor
- [script.py](script.py) - обработка объединенных деклараций и подготовка файлов для загрузки в БД