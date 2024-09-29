-- Type string column to numeric - 1 or 0 for calculation

ALTER TABLE titles_casts
ADD type_numeric INTEGER

SELECT * FROM titles_casts

UPDATE titles_casts
SET type_numeric = 1
WHERE type is not null;

SELECT * FROM titles_casts;

-- Count and percent of total by type
-- Movies are about 70% to total 

SELECT type, SUM(type_numeric), SUM(type_numeric)*100 / ( SELECT SUM(type_numeric) FROM titles_casts) AS Pct_total
FROM titles_casts
GROUP BY type, type_numeric

-- Join with Information table to explore Genres and ratings
-- TOP 5 are Dramas, Comedies, Action&Adventure, and Documentaries

SELECT info.Category as Genre, COUNT(Category) as cnt
FROM titles_casts as title
JOIN information as info on title.show_id = info.show_id 
WHERE Category is not NULL AND Category <> ''
GROUP BY Category
ORDER BY cnt DESC

-- Change date_added column from string to datetime
-- 25-Sep-21

SELECT CONVERT(date, date_added) AS Date_modified
FROM date_country

ALTER TABLE date_country
ADD date_added_modified AS CONVERT(date, date_added)

SELECT * FROM date_country

-- International TV shows By year added
-- Most international tv shows were added in 2019 and 2020 - maybe because of Covid?
SELECT YEAR(yr.date_added_modified) as AddedYear,  COUNT(Category) as cnt
FROM titles_casts as title
JOIN information as info on title.show_id = info.show_id JOIN date_country as yr ON info.show_id = yr.show_id
WHERE Category = 'International TV Shows'
GROUP BY YEAR(yr.date_added_modified), Category
ORDER BY cnt DESC

-- By Rating using CTE
WITH RatedTitles AS (
    SELECT info.rating
    FROM titles_casts AS title
    JOIN information AS info ON title.show_id = info.show_id
    WHERE info.rating IS NOT NULL AND info.rating <> ''
)

SELECT rating, COUNT(rating) AS cnt
FROM RatedTitles
GROUP BY rating
ORDER BY cnt DESC;

-- top 10 PG-13 directors by rating and type
SELECT t.director, COUNT(*) as cnt
FROM titles_casts as t
JOIN information as i ON t.show_id = i.show_id 
WHERE rating = 'PG-13'
GROUP BY director
ORDER BY cnt DESC 
OFFSET 0 ROWS FETCH NEXT 10 ROWS ONLY;

-- Top 10 comedy casts by country
-- top1 is Adam Sandler.. Where is Will Ferrell??
SELECT t.cast1 , COUNT(*) as cnt
FROM information as i JOIN titles_casts as t ON i.show_id = t.show_id
WHERE i.Category = 'Comedies' OR i.Category = 'TV Comedies' AND t.cast1 is not NULL AND t.cast1 <> ''
GROUP BY t.cast1
ORDER BY cnt DESC 
OFFSET 0 ROWS FETCH NEXT 10 ROWS ONLY;


-- Top 10 movie Countries 
SELECT c.country , COUNT(*) as cnt
FROM information as i JOIN date_country as c ON i.show_id = c.show_id JOIN titles_casts as t ON c.show_id = t.show_id
WHERE t.type = 'Movie' AND t.type <>'' AND t.type is not NULL
GROUP BY c.country
ORDER BY cnt DESC
OFFSET 0 ROWS FETCH NEXT 10 ROWS ONLY;
