
from flask import Flask, request
from datetime import datetime
import json
import mysql.connector

class create_dict(dict): 
  
    # __init__ function 
    def __init__(self): 
        self = dict() 
          
    # Function to add key:value 
    def add(self, key, value): 
        self[key] = value

mydb = mysql.connector.connect(
  host="lin-13041-7784-mysql-primary.servers.linodedb.net",
  user="linroot",
  passwd="7ZmXl9xm9J@qsBIZ",
  database="Departures"
)

app = Flask(__name__)

@app.route("/api/data", methods=["POST"])
def receive_data():
    # Get the JSON data from the request
    data = request.get_json()

    # Print the data
    print(data)

    return "Data received", 200




@app.route("/flights")
def flights():
    # Get the date parameter from the URL
    date = request.args.get("date")
    if date is None:
        # If the date parameter is not set, return a "Bad Request" error
        return "Bad Request", 400

    # Parse the date parameter into a datetime object
    date = datetime.strptime(date, r"%d/%m/%Y")

    # Query the database for all flights on the given date
    with mydb.cursor() as cursor:
        sql = "SELECT * FROM Flights WHERE DATE(Planned) = %s"
        cursor.execute(sql, (date,))  # Note the extra comma here
        result = cursor.fetchall()
   
    mydict = create_dict()
    keys = []
    for i,row in enumerate(result):
        planned = row[3]
        planned.strftime("%m/%d/%Y %H:%M:%S")
        estimated = None
        if row is not None:
            estimated = row[4]
            estimated = estimated.strftime("%m/%d/%Y %H:%M:%S")
        mydict.add(str(i),(({
            "Rute":row[0],
            "DepartureAirport": row[1],
            "ArrivalAirport": row[2],
            "Planned": str(planned),
            #Might be a problem but we'll take a look at it
            "Estimated": str(estimated),
            "Status_kl": row[5],
            "Status_en": row[6],
            "Status_da": row[7],
            "FlightHash": row[8],
            "ArrivalICAO": row[9],
            "DepartureICAO":row[10]
        })))

        for i,x in enumerate(row):
            print(str(i) + " " + str(x))
    # Format the query result as a JSON string and return it
    return json.dumps(mydict, indent=2), 200
    


app.run()
