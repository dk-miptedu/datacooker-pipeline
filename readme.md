# Создание DATA-API
## Аннотация

Необходимо создать инструмент, который автоматизирует процедуру заполнения контракта AI-модели/стратегии на стороне сервиса, осуществляющего вызов, с учетом:

* Модели данных от источников, которые опрашивает сервис
* Модель данных на вход стратегии/модели
* Правила преобразования данных для подачи на стратегию/модель, например: `дата рождения в возраст`, `адрес в код региона`


Задача открытая, нет ограничений для участников в выборе решения. На выходе должен получиться инструмент, который позволит:
решать интеграционные задачи силами “гражданских” разработчиков (системный аналитик, Риск-технолог и так далее);
упростить производственный процесс для задач добавления новых источников данных на модели, изменения контрактов существующих.
Будет плюсом, если будет предусмотрен интеллектуальный режим отладки.


## Алгоритм решения - `Data-API pipeline`

Схема 1. workflow процесса подготовки данных


![1733767027671](./assets/img/data-api-fabrica-v2.png)

**Описание алгоритма**

**Предусловие**
1. Получены Данные(ответы) от внешних систем согласно регламента;
2. Определены Схемы данных внешних источников;
3. Определана Схема данных контракта для запроса к AI-модели.

**Основной сценарий**
1. Система получает "Данные внешних источников", "Схемы данных внешних источников", "Схему данных контракта для AI-модели";
2. Система обрабатывает Данные внешних источников и меняет наименование ключа в атрибуте на соответствующее значение description из Схемы данных внешнего источника и формирует новый набор данных;
3. Система формирует promt для GigaChat и соединяет новый набор данных и Схему данных котракта AI-модели;
4. Система выполняет запрос к GigaChat, получает ответ и формирует Payload запроса для AI-модели: сохраняет его в файл в формате JSON.

**Постусловие**
1. Система получает подтверждение выполненного задания.

