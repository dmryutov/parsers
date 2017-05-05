# Парсер сайта ГАС «Правосудие»

(__Python 3.x__) Извлечение судебных решений с сайта `ГАС «Правосудие»` (bsr.sudrf.ru).

## Описание
На сайте осуществляется динамическая загрузка контента. Поэтому используются не совсем обычный метод извлечения данных.
Реализовано 2 версии программы:
- С использованием dryscrape
- С использованием selenium

### Selenium
- Работает на всех основных операционных системах
- Работа с любым установленным браузером
- Реализовано несколько версий (1 поток, несколько потоков, несколько процессов)
- ≈ 1000 страниц / час
### Dryscrape
- Работает только на Unix
- ≈ 6500 страниц / час

## Общий алгоритм
- Загрузка сервера/браузера
- Открытие первого дела из поисковой выдачи
- Выгрузка всех доступных полей (кроме последнего)
- Поиск имени подсудимого в тексте судебного акта (последнее поле)
- Переход на следующее дело путем нажатия на кнопку "Далее"
- Повторять до тех пор, пока доступна кнопка "Далее"