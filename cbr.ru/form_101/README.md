# Парсер сайта «Центральный банк Российской Федерации»

(__PHP 5.x__) Извлечение финансовых показателей банков (101 форма) с сайта `Центральный банк Российской Федерации` (cbr.ru).

## Описание
Для скачивания данных с сайта использовалась программа [Content Downloader](http://sbfactory.ru). Каждая страница сохраняется в файл вида `article_X_.txt`.

## Файлы
- [bank_list.php](bank_list.php) - перечень банков в формате `'Номер лицензии' => 'Краткое наименование'`
- [export_result.php](export_result.php) - создает сводную таблицу и сохраняет в .xlsx файл
- [files](files) - скачанные вспомогательные файлы
	- [full_name.txt](files/full_name.txt) - полное наименование банка
	- [id.txt](files/id.txt) - id банка
	- [link.txt](files/link.txt) - ссылка на банк
	- [name.txt](files/name.txt) - краткое наименование банка
	- [number.txt](files/number.txt) - номер лицензии банка
- [generate_links.php](generate_links.php) - генерация ссылок для обработки
- [get_cell.php](get_cell.php) - вспомогательный файл, содержащий объявления функций
- [get_data.php](get_data.php) - обработка данных:
	- извлечение данных из текстовых файлов
	- очистка
	- приведение к нужному виду
	- сохранение в БД
- [get_indicator.php](get_indicator.php) - парсер индикаторов с сайта `profbanking.com`
- [links.txt](links.txt) - список ссылок, которые необходимо скачать
- [projects](projects) - проекты программы Content Downloader
	- [finance.cdp](projects/finance.cdp) - финсовые показатели
	- [full_name.cdp](projects/full_name.cdp) - полное наименование банка
	- [number_id_name.cdp](projects/number_id_name.cdp) - номер лицензии, id и краткое наименование банка