# FYP-2020
Recommendation system for farmers using Machine Learning and IoT

Project aims at providing recommendation system for farmers.
Real time data is taken from the soil and is sent to the cloud.
The APIs mentioned below, process the real time data and provide crop and fertilizer recommendations.


# Usage:

Navigate to Backend/APIs

Command: python app.py

App routes:
localhost:5555/crop

Response:
{
'crop_name' :
'soil_moisture':
}

localhost:5555/fertilizer

Returns the fertilizer recommendation wrt to the crop
