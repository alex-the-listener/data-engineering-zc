# Module 1 Homework Solutions

```sql

/*
QUESTION 4: Which was the pick-up day with the longest trip distance?
Answer:`2025-11-14`
*/
--QUERY USED--
SELECT 
    lpep_pickup_datetime,
    trip_distance
FROM green_taxi_trips
WHERE trip_distance < 100
ORDER BY trip_distance DESC
LIMIT 1;


/*
QUESTION 5: Which were the top pickup zones with the largest total_amount sum on November 18, 2025?
*/
--QUERY USED--
SELECT 
    z."Zone",
    SUM(t.total_amount) AS total_amount_sum
FROM green_taxi_trips t
JOIN zones z 
  ON t."PULocationID" = z."LocationID"
WHERE t.lpep_pickup_datetime >= '2025-11-18 00:00:00'
  AND t.lpep_pickup_datetime < '2025-11-19 00:00:00'
GROUP BY z."Zone"
ORDER BY total_amount_sum DESC
LIMIT 1;



/*
QUESTION 6: For passengers picked up in East Harlem North in November 2025, which drop-off zone had the largest tip?
Answer: JFK Airport (or your top result)
*/
--QUERY USED--
SELECT 
    z_dropoff."Zone" AS dropoff_zone,
    MAX(t.tip_amount) AS max_tip
FROM green_taxi_trips t
JOIN zones z_pickup 
  ON t."PULocationID" = z_pickup."LocationID"
JOIN zones z_dropoff 
  ON t."DOLocationID" = z_dropoff."LocationID"
WHERE z_pickup."Zone" = 'East Harlem North'
  AND t.lpep_pickup_datetime >= '2025-11-01 00:00:00'
  AND t.lpep_pickup_datetime < '2025-12-01 00:00:00'
GROUP BY z_dropoff."Zone"
ORDER BY max_tip DESC
LIMIT 1;