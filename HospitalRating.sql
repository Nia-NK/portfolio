SELECT * FROM [Hospital General Information]

-- Delete nulls of rating
DELETE FROM [Hospital General Information]
WHERE Hospital_overall_rating

-- Check the average rating in general
-- Avg is 3
SELECT AVG(Hospital_overall_rating) FROM [Hospital General Information]

-- Check the percentage of number of hospitals lower than the average rating per state
-- Step1: Calculate the overall average hospital rating
WITH AverageRating AS (
	SELECT AVG(CAST(Hospital_overall_rating AS FLOAT)) AS AvgRating
	FROM [Hospital General Information]
)
-- Step2: Count hospitals below the overall average to get the percentage group by state
SELECT 
	State,
	SUM(CASE WHEN CAST(Hospital_overall_rating AS FLOAT) < ar.AvgRating THEN 1 ELSE 0 END) AS HospitalsBelowAvg,
	COUNT(*) AS TotalHospitals,
	ROUND(SUM(CASE WHEN CAST(Hospital_overall_rating AS FLOAT) < ar.AvgRating THEN 1 ELSE 0 END) *100/ COUNT(*) , 2) AS PercentageBelowAvg
FROM [Hospital General Information]
CROSS JOIN AverageRating ar
GROUP BY State
ORDER BY PercentageBelowAvg DESC;

-- DC, AK, GU, VI, PR are 100% below average
-- WV, CT, NV, NM are over 90% below average
-- Top 5 States that have the least below average hospitals are SD, DE, WI, MN, IN, UT
-- Total number of hospitals are too various per state so this might not be a good enough indicator to compare state to state

-- Hmmmm then what about Patient experience national comparison?
-- which state has the most "Above the national average"
-- Since the number of hospitals varies a lot, percentage is used here as well

SELECT State, 
	SUM(CASE WHEN Patient_experience_national_comparison = 'Above the national average' THEN 1 ELSE 0 END) AS Patient_Exp_Count,
	COUNT(*) AS TotalRatings,
	ROUND(SUM(CASE WHEN Patient_experience_national_comparison = 'Above the national average' THEN 1 ELSE 0 END) *100/ COUNT(*) , 2) AS PercentageAboveAvg
FROM [Hospital General Information]
GROUP BY State
ORDER BY PercentageAboveAvg DESC;
-- Most top overall rating states have high patient exprience ratings


-- What about by Hospital Ownership??
SELECT Hospital_Ownership, COUNT(*) AS Cnt, AVG(Hospital_overall_rating) AS AvgRating
FROM [Hospital General Information]
GROUP BY Hospital_Ownership
ORDER BY AVG(Hospital_overall_rating) DESC

-- it's either 2 or 3, what about Emergency Services?
-- Emergency Services is a boolen value: 1 = yes, 0= no

SELECT Emergency_Services, Hospital_Ownership, COUNT(Emergency_Services)
FROM [Hospital General Information]
GROUP BY Hospital_Ownership, Emergency_Services

SELECT 
	Hospital_Ownership,
	[1] AS Yes,
	[0] AS No
FROM
	(
		SELECT
			Emergency_Services,
			Hospital_Ownership,
			COUNT(*) AS Count
		FROM
			[Hospital General Information]
		GROUP BY
			Hospital_Ownership,
			Emergency_Services
	) AS SourceTable
PIVOT
	(
		SUM(Count)
		FOR Emergency_Services IN ([1],[0])
	) AS PivotTable
ORDER BY
	[1] DESC;

-- I live in Philly and got curious - let's narrow this down to PA and find the best hospital
SELECT City, Hospital_Name, Hospital_overall_rating
FROM [Hospital General Information]
WHERE State = 'PA'
ORDER BY Hospital_overall_rating DESC;
-- Two hospitals in PA are 5 out of 5!

