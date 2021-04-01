project21_bot
# Квест “На сколько процентов ты фикловец”? (для студентов 1 курса ФиКЛ)

## Краткое описание проекта

Бот с заданиями про фикл 

## Подробное описание
* Что должно получится в итоге (консольная программа, бот, что-то еще)?

Бот, который предлагает несколько типов заданий, к каждому разделу предлагается инструкция (https://docs.google.com/document/d/1hgPy0Vsa7PNyp3mQeZ_X2BlrSkZZJt2MtVMJfq9CEWw/edit): 

**Мемы** ("В каждом задании этого раздела вам будет показан мем, связанный с нашим потоком. Вам нужно будет выбрать один вариант ответа или ввести слово.")

Например: 

*Введите слово*

![alt text](https://sun9-6.userapi.com/impg/AcFoF4MPLEMPs2DESBLPX1xI5RLMcor8-XjTyQ/h5epHIYDODo.jpg?size=1239x736&quality=96&sign=7d1c1a38758938b2aca21082123a43c5&type=album)

**Цитаты** ("В этом разделе вам будут представлены цитаты преподавателей. Отгадайте, кому они принадлежат.")

Например:

*“Видите ли вы эту красивую табличку с буквами? Она вам нравится или вызывает ужас? Вы пока подумайте, а я включу «Щенячий патруль»”. Введите сначала имя, потом фамилию преподавателя. (Инна Зибер)*

**Организация учебного процесса** ("В этом разделе будут вопросы, связанные с учебным процессом на фикле. Выберите верный вариант ответа или введите слово.")

Например: 

*Какие семинары загадочно исчезают из РУЗа?*

*фонетика (верный)*

*социолингвистика*

*академическое письмо*

*пары по языкам*

В конце бот возвращает количество набранных баллов/процент правильных ответов 

Например:

*Ваш результат:*

*0-29% - ты не с фикла! но можешь перевестись сюда :))*

*30-54% - кажется, ты мало ходил на  пары. ну ничего, впереди еще три года.*

*55-79% - есть недочеты, но ты молодец!*

*80-100% - ты настоящий фикловец!*
 
* Что ваша программа принимает как входные данные?

1) Принимает ответ на запрос "Выберите раздел" (название раздела "мемы"/"цитаты"/"организация учебного процесса")

2) Принимает ответы на задания: для первых двух разделов введенные слова или словосочетания, для третьего выбранный из предложенных вариантов ответ
 
* Какие модули программа будет использовать (re, math)?

pybot, pyTelegramBotAPI

* Если используете лингвистические данные, опишите какие

текстовые ответы пользователя, цитаты

## Критерий завершенного проекта
* Как мы (преподаватели и остальные студенты) поймем, что вы все сделали круто?

Бот здоровается, позволяет выбрать раздел заданий (мемы/цитаты/вопросы), присылает инструкцию к разделу задания, принимает ответы, считает и присылает результат. 

* Например, если вы делаете антиплагиатор кода, как нам понять, что он работает правильно?

не зависает, умеет обрабатывать разные случаи, в конце получается результат теста
## Команда проекта

* ФИО и группа 

Елена Зайцева, 201 

Диана Аскарова, 204

Анна Ткач, 201 

## Таймлайн проекта
* Когда и что будет сделано (примерно)

21.03 - **подробный** план проекта, узнать, как работают библиотеки для телеграма, создание бота

## Чего вам не хватает для реализации проекта
* Что надо еще узнать?

не хватает знаний про pybot, pyTelegramBotAPI
* Какие-то другие проблемы

## Распределение обязанностей в команде
* По каждому человеку, кто и что будет делать

*До 21 марта:*

Лена - создание бота

Диана - содержание (составление заданий)

Аня - описание проекта (ридми)
