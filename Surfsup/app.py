# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Declare a Base using `automap_base()`
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)

# # Assign the measurement class to a variable called `Measurement` and
# # the station class to a variable called `Station`
Measurement = Base.classes.measurement
Station = Base.classes.station

# #################################################
# # Flask Setup
# #################################################

app = Flask(__name__)

# #################################################

# Show the Welcome Page pages as hyperlinks

# #################################################

@app.route("/")
def welcome():
    """List all available API routes."""

    # Create a session
    session = Session(engine)

    # Calculate the minimum and maximum date
    min_date = session.query(func.min(Measurement.date)).first()[0]
    max_date = session.query(func.max(Measurement.date)).first()[0]

    # Close the session
    session.close()

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Hawaii Climate Analysis API</title>
        <style>
            body {{ 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                line-height: 1.6; 
                padding: 20px; 
                max-width: 800px; 
                margin: 0 auto; 
                background-color: #f0f8ff; 
                color: #333;
            }}
            h1 {{ color: #00539C; }}
            h2 {{ color: #0077BE; }}
            .route {{ 
                background-color: #ffffff; 
                padding: 15px; 
                margin-bottom: 15px; 
                border-radius: 8px; 
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                transition: transform 0.2s ease-in-out;
            }}
            .route:hover {{
                transform: translateY(-3px);
            }}
            .route h3 {{ 
                margin-top: 0; 
                color: #00539C;
            }}
            a {{ 
                color: #0077BE; 
                text-decoration: none; 
                transition: color 0.2s ease-in-out;
            }}
            a:hover {{ 
                color: #00539C;
                text-decoration: underline; 
            }}
            input[type="date"] {{ 
                margin-right: 10px; 
                padding: 5px;
                border: 1px solid #0077BE;
                border-radius: 4px;
            }}
            button {{
                background-color: #0077BE;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
                cursor: pointer;
                transition: background-color 0.2s ease-in-out;
            }}
            button:hover {{
                background-color: #00539C;
            }}
            .header-image {{ 
                width: 100%; 
                max-height: 300px; 
                object-fit: cover; 
                border-radius: 10px; 
                margin-bottom: 20px; 
                box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
            }}
            .acknowledgement {{ 
                font-size: 0.8em; 
                margin-top: 20px; 
                color: #666;
            }}
        </style>
    </head>
    <body>
        <img src="https://content.r9cdn.net/rimg/dimg/29/40/3f4ec996-city-28070-16c96b74d6d.jpg?width=1366&height=768&xhint=3379&yhint=2867&crop=true" alt="Hawaii" class="header-image">
        <h1>Welcome to the Hawaii Climate Analysis API!</h1>
        <p>Analysis Date Range: {min_date} to {max_date}</p>
        
        <h2>Available Routes:</h2>
        
        <div class="route">
            <h3>Precipitation Data</h3>
            <p>View precipitation data for the last 12 months:</p>
            <a href="/api/v1.0/precipitation">/api/v1.0/precipitation</a>
        </div>
        
        <div class="route">
            <h3>Stations</h3>
            <p>View the list of weather stations:</p>
            <a href="/api/v1.0/stations">/api/v1.0/stations</a>
        </div>
        
        <div class="route">
            <h3>Temperature Observations</h3>
            <p>View temperature observations of the most active station for the last year:</p>
            <a href="/api/v1.0/tobs">/api/v1.0/tobs</a>
        </div>
        
        <div class="route">
            <h3>Temperature Stats from Start Date</h3>
            <p>View minimum, average, and maximum temperatures from a start date:</p>
            <input type="date" id="start-date" min="{min_date}" max="{max_date}">
            <button onclick="generateStartLink()">Generate Link</button>
            <p id="start-link"></p>
        </div>
        
        <div class="route">
            <h3>Temperature Stats for Date Range</h3>
            <p>View minimum, average, and maximum temperatures for a date range:</p>
            <input type="date" id="range-start-date" min="{min_date}" max="{max_date}">
            <input type="date" id="range-end-date" min="{min_date}" max="{max_date}">
            <button onclick="generateRangeLink()">Generate Link</button>
            <p id="range-link"></p>
        </div>
        
        <p class="acknowledgement">Data provided by <a href="https://journals.ametsoc.org/view/journals/atot/29/7/jtech-d-11-00103_1.xml">Menne et al., 2012</a></p>
        
        <script>
            function generateStartLink() {{
                const startDate = document.getElementById('start-date').value;
                if (startDate) {{
                    const link = `/api/v1.0/${{startDate}}`;
                    document.getElementById('start-link').innerHTML = `<a href="${{link}}">${{link}}</a>`;
                }}
            }}

            function generateRangeLink() {{
                const startDate = document.getElementById('range-start-date').value;
                const endDate = document.getElementById('range-end-date').value;
                if (startDate && endDate) {{
                    const link = `/api/v1.0/${{startDate}}/${{endDate}}`;
                    document.getElementById('range-link').innerHTML = `<a href="${{link}}">${{link}}</a>`;
                }}
            }}
        </script>
    </body>
    </html>
    """

# #################################################
# # Flask Routes
# #################################################

@app.route("/api/v1.0/precipitation")
def precipitation_data():
    """Return the precipitation data as JSON"""

    # Create a session
    session = Session(engine)

    # Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using `date` as the key and `prcp` as the value.
    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    most_recent_date = dt.datetime.strptime(most_recent_date[0], '%Y-%m-%d')
    one_year_ago = most_recent_date - dt.timedelta(days=366)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago).all()
    
#     # Close the session
    session.close()

#     # Create a dictionary from the row data and append to a list of all_precipitation
    all_precipitation = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)

@app.route("/api/v1.0/stations")    
def stations():
    """Return a JSON list of stations from the dataset."""
    # Create a session
    session = Session(engine)

    # Query all stations
    results = session.query(Station.station).all()

    # Close the session
    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a JSON list of Temperature Observations (tobs) for the previous year."""
    # Create a session
    session = Session(engine)

    # Query the dates and temperature observations of the most active station for the last year of data.
    most_active_station = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).first()
    most_active_station = most_active_station[0]
    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    most_recent_date = dt.datetime.strptime(most_recent_date[0], '%Y-%m-%d')
    one_year_ago = most_recent_date - dt.timedelta(days=366)
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= one_year_ago).filter(Measurement.station == most_active_station).all()

    # Close the session
    session.close()

    # Create a dictionary from the row data and append to a list of all_tobs
    all_tobs = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
def start(start):
    """Return a JSON dictionary of the minimum temperature, the average temperature, and the max temperature for a given start date."""
    # Create a session
    session = Session(engine)

    # Query the minimum temperature, the average temperature, and the max temperature for a given start date
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()

    # Close the session
    session.close()

    # Convert query results to a dictionary
    temp_stats = {
        "TMIN": results[0][0],
        "TAVG": results[0][1],
        "TMAX": results[0][2]
    }

    return jsonify(temp_stats)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    """Return a JSON dictionary of the minimum temperature, the average temperature, and the max temperature for a given start-end range."""
    # Create a session
    session = Session(engine)

    # Query the minimum temperature, the average temperature, and the max temperature for a given start-end range
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    # Close the session
    session.close()

    # Convert query results to a dictionary
    temp_stats = {
        "TMIN": results[0][0],
        "TAVG": results[0][1],
        "TMAX": results[0][2]
    }

    return jsonify(temp_stats)

if __name__ == "__main__":
    app.run(debug=True)
