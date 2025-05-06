SELECT TO_CHAR(d::date, 'YYYY-MM-DD') AS generated_date, string_agg(base_type, ', ') AS event_types
FROM generate_series('2025-01-01', '2025-12-31', '1 day'::interval) d
LEFT JOIN events e ON d::date = e.date
GROUP BY TO_CHAR(d::date, 'YYYY-MM-DD')
ORDER BY generated_date;