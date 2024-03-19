## Using tables 
aircraft-data_nov_dec.csv
Airplane_Cleaned.csv
autoscout24-germany-dataset.csv
CARS_1.csv
USA_cars_datasets.csv
imdb_top_1000.csv
netflix_titles.csv
## Using columns:
```
reg_state .
reg_city .
flight .
tail_number .
reg_expiration .
reg_owner .
manufacturer .
model .
Engine Type .
Multi Engine .
TP mods .
Model .
Company .
make .
gear .
offerType .
fuel 
transmission_type .
fuel_type .
car_name 
body_type .
country .
vin .
brand .
state .
title_status .
color 
condition 
Certificate 
Gross .
Poster_Link 
Director 
Series_Title 
Overview 
Star2 
Star3 
Star1 
Star4 
Genre 
show_id 
cast 
title 
director 
description 
type 
listed_in 
rating 
duration 
date_added 
```
# How Did I cluster by copilot 
- I wrote: `I will send you few rows of diferent tables could you please clustered columns of these tables ?`
- I wrote: `I will send you all tables in cvs format i will say done when i will be done`
- Then I send 15 rows of each table to copilot and I worote done. 
- I wrote all names of columns in the list above.
- I wrote `Could you please guess the clusters`, this does not worke and copilot response was `As an AI, I can provide a high-level approach to clustering the data based on the columns you’ve provided. However, I’m unable to perform the actual clustering operation or guess the clusters without running a specific clustering algorithm on the data. Here’s a general approach:`
- I wrote `Could you show similar groups of columns` and I got the response below. (Ad Clustering by Microsoft Copilot)
- I wrote `Could you split it to more groups ?` and I got the response below. (Ad Granular Clustering by Microsoft Copilot)
## Clustering by Microsoft Copilot
Sure, based on the data you've provided, here are some potential groupings of similar columns:

1. **Geographical Information**: These columns contain location-related information.
   - `reg_state`
   - `reg_city`
   - `country`
   - `state`

2. **Vehicle/Flight Information**: These columns contain information about vehicles or flights.
   - `flight`
   - `tail_number`
   - `manufacturer`
   - `model`
   - `make`
   - `car_name`
   - `brand`
   - `vin`
   - `Engine Type`
   - `Multi Engine`
   - `TP mods`
   - `Model`
   - `Company`

3. **Registration/Ownership Information**: These columns contain information about the registration or ownership of a vehicle or flight.
   - `reg_expiration`
   - `reg_owner`
   - `title_status`

4. **Fuel/Transmission Information**: These columns contain information about the fuel type or transmission of a vehicle.
   - `fuel`
   - `transmission_type`
   - `fuel_type`

5. **Offer/Price Information**: These columns contain information about the offer type or price of a vehicle.
   - `offerType`
   - `price`
   - `Gross`

6. **Media Information**: These columns contain information about movies, TV shows, or series.
   - `Poster_Link`
   - `Director`
   - `Series_Title`
   - `Overview`
   - `Star2`
   - `Star3`
   - `Star1`
   - `Star4`
   - `Genre`
   - `show_id`
   - `title`
   - `director`
   - `description`
   - `type`
   - `listed_in`
   - `rating`
   - `duration`
   - `date_added`

Please note that these are just suggested groupings based on the column names and the context provided. The actual similarity between columns would depend on the specific values in these columns. If you have a specific clustering algorithm or similarity measure in mind, please provide more details. I'm here to help!

## Granular Clustering by Microsoft Copilot
Absolutely, here are more granular groupings of the columns:

1. **Flight Information**: These columns contain specific information about flights.
   - `flight`
   - `tail_number`

2. **Vehicle Registration Information**: These columns contain information about the registration of a vehicle.
   - `reg_expiration`
   - `reg_owner`
   - `vin`
   - `title_status`

3. **Vehicle Manufacturing Information**: These columns contain information about the manufacturer and model of a vehicle.
   - `manufacturer`
   - `model`
   - `make`
   - `brand`
   - `Model`
   - `Company`

4. **Vehicle Specifications**: These columns contain information about the specifications of a vehicle.
   - `Engine Type`
   - `Multi Engine`
   - `TP mods`
   - `gear`
   - `transmission_type`
   - `fuel_type`
   - `body_type`

5. **Geographical Information**: These columns contain location-related information.
   - `reg_state`
   - `reg_city`
   - `country`
   - `state`

6. **Offer Information**: These columns contain information about the offer type or price of a vehicle.
   - `offerType`
   - `price`
   - `Gross`

7. **Media Titles and Descriptions**: These columns contain the titles and descriptions of movies, TV shows, or series.
   - `Series_Title`
   - `Overview`
   - `title`
   - `description`
   - `type`
   - `listed_in`

8. **Media Ratings and Duration**: These columns contain the ratings and duration of movies, TV shows, or series.
   - `rating`
   - `duration`
   - `date_added`

9. **Media Production Information**: These columns contain information about the director and cast of movies, TV shows, or series.
   - `Poster_Link`
   - `Director`
   - `Star2`
   - `Star3`
   - `Star1`
   - `Star4`
   - `show_id`
   - `cast`
   - `director`

10. **Vehicle Condition and Color**: These columns contain information about the condition and color of a vehicle.
   - `condition`
   - `color`

11. **Media Genre**: These columns contain information about the genre of movies, TV shows, or series.
   - `Genre`

Please note that these are just suggested groupings based on the column names and the context provided. The actual similarity between columns would depend on the specific values in these columns. If you have a specific clustering algorithm or similarity measure in mind, please provide more details. I'm here to help!

