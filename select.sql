SELECT TO_CHAR(d::date, 'YYYY-MM-DD') AS date, string_agg(base_type, ',')
FROM generate_series('2025-01-01', '2025-01-31', '1 day'::interval) d
LEFT JOIN events e ON d::date = e.date
GROUP BY d::date ORDER BY d::date;

/*  
Функция generate_series генерирует последовательность значений из указанного промежутка начало-конец-шаг (start, stop, interval)
d - псевдоним (alias) для результирующего столбца с датами (аналог table_1 для с-са left join ниже)

The LEFT JOIN keyword returns all records from the left table (table1) - здесь столбец d с датами, 
and the matching records from the right table (table2). The result is 0 records from the right side, if there is no match.
If there is a match - two tables will be joined.

LEFT JOIN Syntax

SELECT column_name(s)  здесь колонки перечисляются из обеих таблиц
FROM table1
LEFT JOIN table2
ON table1.column_name = table2.column_name;


e — это псевдоним для events.
on d::date = e.date: Условие соединения. Мы сравниваем сгенерированные даты (приведенные к типу date) с датами в таблице events. Если даты совпадают, строки будут объединены.

select d::date, coalesce(base_type, 0) as base_type

d::date: Мы выбираем сгенерированные даты и приводим их к типу date 

coalesce(base_type, 0): Функция coalesce возвращает первое ненулевое значение из списка. В данном случае, если значение base_type равно NULL (что произойдет, если для данной даты нет соответствующей записи в events), то будет возвращено значение 0. Это позволяет избежать появления NULL в результирующем наборе. В моем коде (e.base_type, '0') так как для ф-ции coalesce значения дб одинак типа поэтому 0 приведен к строке, тк base_type is varchar  

as base_type: Псевдоним для результирующего столбца, который будет содержать итоговые значения.

Синтаксис функции Oracle/PLSQL TO_CHAR:

TO_CHAR( value, [ format_mask ], [ nls_language ] ) только 1 аргумент обязателен
*/