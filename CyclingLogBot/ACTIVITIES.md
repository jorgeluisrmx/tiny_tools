
##### ---- gral tasks ---- #####

- [    ] Notes on pyton telegram bot (clbot document)
- [ x ] Include in basic documentation the libraries i am using
- [ x ] Create commit about process on GpxActivity
- [ x ] Add notes to Python Kg about fysom
- [ x ] Add explore file
- [ x ] Commit database addition
- [ x ] Add changes to class diagram ****
- [    ] document sqlite3 row factory


##### ---- v1.0 tasks ---- #####

- [ x ] totals 1.0
- [ x ] stage_summary 1.0
- [ x ] summary by month 1.0
- [ x ] summary by year 1.0
- [ x ] route_summary 1.0 basic implementation


##### ---- v1.1 tasks ---- #####

- rankings
- Detailed description of route
- month resumme
- entry points: set token
- entry points: set elevation api key
- entry points: create user from dir


##### ---- v1.2 tasks ---- #####

- summary by date
- activity inspection
- Activate an deactive bot in second process


##### ---- v1.3 tasks ---- #####

- trends


#### NOTES --------------------------------------

How to start a background process in Python: http://stackoverflow.com/questions/1196074/how-to-start-a-background-process-in-python

## Ideas for explore activities


Months ranqued by distance
SELECT strftime("%m", date) as month,
	   strftime("%Y", date) as year,
	   sum(distance) as distance
FROM activities
GROUP BY year, month
ORDER BY distance DESC
LIMIT 10

Months rankes by elevation_gain
SELECT strftime("%m", date) as month,
	   strftime("%Y", date) as year,
	   sum(elev_gain) as elev_gain
FROM activities
GROUP BY year, month
ORDER BY elev_gain DESC
LIMIT 10

Months ranked by time_moving
SELECT strftime("%m", date) as month,
	   strftime("%Y", date) as year,
	   sum(time_moving) as time_moving
FROM activities
GROUP BY year, month
ORDER BY time_moving DESC
LIMIT 10

Routes ranked by distance
SELECT route,
		mod,
	   sum(distance) as distance
FROM activities
GROUP BY route, mod
ORDER BY distance DESC
LIMIT 10

Route, mod ranked by distance
SELECT route,
	   sum(distance) as distance
FROM activities
GROUP BY route
ORDER BY distance DESC
LIMIT 10

* Each month route dedication


* * Detailed description of route
SELECT *
FROM (
	SELECT mod,
		sum(distance) as total_distance,
		sum(time_moving) as total_time_moving,
		min(time_moving) as best_time,
		avg(speed_moving) as avg_speed,
		max(speed_moving) as best_speed,
		max(speed_max) as best_max_speed
	FROM activities
	WHERE route='Nogueras'
	GROUP BY mod
	ORDER BY total_distance DESC
) r1 LEFT JOIN (
	SELECT mod, date as date_time_moving, time_moving
	FROM activities
	WHERE route='Nogueras'
) r2 ON r1.mod=r2.mod AND r1.best_time=r2.time_moving


u'\u26f0' montain total_elev_gain  
u'\U0001f682' speed train
u'\U0001f3ce' max_speed f1_car
u'\u23f3' time sand watch
u'\u23f1' time moving cronometer
u'\U0001f4c6' calendar
u'\U0001f3c1' squared flag
u'\U0001f6b4' bike
u'\U0001f3c5' medal
u'\U0001f422' tortuga
u'\U0001f430' liebre
u'\U0001f3a2' descenso
u'\U0001f985' aguila
u'\U0001f41c' hormiga



