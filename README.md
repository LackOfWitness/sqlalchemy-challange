<img src="Surfsup/Hawaii Weather Readme Header.jpg" alt="Hawaii Weather Header" width="100%" style="max-width: 800px; display: block; margin: 0 auto; border-radius: 10px; border: 2px solid #333; box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);">

# SQLAlchemy Challenge - Surfs Up!

## Overview
This project involves a climate analysis of Honolulu, Hawaii to help with vacation planning. The analysis uses Python, SQLAlchemy ORM queries, Pandas, and Matplotlib to explore and visualize climate data.

## Project Structure
- `SurfsUp/`
  - `app.py`: Flask API application
  - `climate_starter.ipynb`: Jupyter notebook containing data analysis
  - `Resources/`
    - `hawaii.sqlite`: SQLite database with climate data

## Analysis Performed
1. Precipitation Analysis
   - Retrieved the last 12 months of precipitation data
   - Loaded results into a Pandas DataFrame
   - Plotted the results and calculated summary statistics

2. Station Analysis
   - Calculated total number of stations
   - Found the most active station
   - Calculated lowest, highest, and average temperatures for the most active station
   - Retrieved the last 12 months of temperature observation data for the most active station
   - Plotted results as a histogram

## Flask API Routes
- `/`: Home page listing all available routes
- `/api/v1.0/precipitation`: Returns precipitation data for the last 12 months
- `/api/v1.0/stations`: Returns a list of stations
- `/api/v1.0/tobs`: Returns temperature observations for the most active station in the last year
- `/api/v1.0/<start>`: Returns temperature statistics from a given start date to the end of the dataset
- `/api/v1.0/<start>/<end>`: Returns temperature statistics for a specified date range

<p align="center">
  <img src="Surfsup/Flask Route Snapshot.jpg" alt="Flask Route Snapshot" width="80%" style="display: block; margin: 0 auto;">
</p>

## Getting Started
1. Clone this repository
2. Install required dependencies
3. Run `climate_starter.ipynb` for data analysis
4. Run `app.py` to start the Flask application

## Technologies Used

### Refer to requirements.txt for the complete list of dependencies.

- Python
- SQLAlchemy
- Flask
- Pandas
- Matplotlib

## Author
Sergei N. Sergeev

## Acknowledgments
- Data provided by [Menne et al., 2012](https://journals.ametsoc.org/view/journals/atot/29/7/jtech-d-11-00103_1.xml)