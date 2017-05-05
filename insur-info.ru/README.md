# Парсер интернет-портала «Страхование сегодня»

(__PHP 5.x__) Извлечение информации о состоянии лицензии страховых компаниях с сайта `«Страхование сегодня»` (insur-info.ru).

## Описание
Для скачивания данных с сайта использовалась программа [Content Downloader](http://sbfactory.ru). Каждая страница сохраняется в файл вида `article_X_.txt`.
Содержимое файлов - HTML код таблицы

## Файлы
- [export_result.php](export_result.php) - обработка данных:
	- извлечение данных из текстовых файлов
	- очистка
	- приведение к нужному виду
	- создание сводную таблицу
	- сохранение в .xlsx файл
- [output.xlsx](output.xlsx) - пример выходных данных