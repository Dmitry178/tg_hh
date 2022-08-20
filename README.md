# tg_hh
Telegram бот отправляет запросы на hh.ru и отображает результаты.<br>

Команды бота:<br>
/start - запуск бота<br>
/help - короткая справка<br>
/region - отображение текущего региона поиска по hh.ru<br>
/region &lt;N&gt; - установка региона поиска в hh.ru, где &lt;N&gt; - номер региона в hh.ru, например:<br>
&nbsp;&nbsp;0 - все регионы,<br>
&nbsp;&nbsp;1 - Москва,<br>
&nbsp;&nbsp;2 - Санкт-Петербург<br>
/query <запрос> - новый запрос в hh.ru<br>
/query - повторить запрос, который был введён ранее<br>
/next - следующая страница запроса<br>
/prev - предыдущая страница запроса<br>
/getvac_&lt;vac&gt; - подробнее о вакансии с ID=&lt;vac&gt;<br>

После команд /query и /region допустимо ставить _ вместо пробела<br>

Примеры запросов:<br>
/region 0<br>
/region_2<br>
/query_python<br>
/query python AND AI
