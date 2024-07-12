-- $ sqlite3 database/store_data.db < search.sql
SELECT store_name
FROM stores
WHERE prefecture_name = '岐阜県'
GROUP BY store_name
HAVING COUNT(DISTINCT store_type) = 2
AND SUM(CASE WHEN store_type NOT IN ('しまむら', 'アベイル') THEN 1 ELSE 0 END) = 0;
