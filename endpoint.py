
from flask import Flask, request
from datetime import datetime
import json
import mysql.connector
import itertools

class create_dict(dict): 
  
    # __init__ function 
    def __init__(self): 
        self = dict() 
          
    # Function to add key:value 
    def add(self, key, value): 
        self[key] = value

def dictfetchall(cursor):
    """Returns all rows from a cursor as a list of dicts"""
    desc = cursor.description
    return [dict(zip([col[0] for col in desc], row)) 
            for row in cursor.fetchall()]

mydb = mysql.connector.connect(
  host="lin-13041-7784-mysql-primary.servers.linodedb.net",
  user="linroot",
  passwd="7ZmXl9xm9J@qsBIZ",
  database="Departures"
)

app = Flask(__name__)

@app.route("/api/data", methods=["POST"])
def receive_data():
    json_data = json.loads(request.data)

    # Connect to the MySQL database
    

    # Create a cursor object to execute SQL queries
    cursor = mydb.cursor()

    

    # Iterate through the items in the dictionary and insert them into the SQL table
    for item in json_data:
        query = "INSERT INTO Rooms (RoomNumber, FlightHash) VALUES (%s, %s)"
        cursor.execute(query, (item['RoomNumber'], item['FlightHash']))

    # Commit the changes to the database
    mydb.commit()

    # Close the cursor and connection
    cursor.close()
    mydb.close()

    for room in json_data:
        print(room["FlightHash"])
        print(room["RoomNumber"])
        print()

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
    result = []
    while True:
        with mydb.cursor() as cursor:
            sql = "SELECT * FROM Flights WHERE DATE(Planned) = %s"
            cursor.execute(sql, (date,))  # Note the extra comma here
            rows = dictfetchall(cursor)

            # Process the rows
            for row in rows:
                # Convert the datetime objects to strings
                planned = row["Planned"].strftime("%m/%d/%Y %H:%M:%S")
                estimated = None
                if row["Estimated"] is not None:
                    estimated = row["Estimated"].strftime("%m/%d/%Y %H:%M:%S")

                # Update the dictionary with the new values
                row["Planned"] = planned
                row["Estimated"] = estimated

                # Append the dictionary to the result list
                result.append(row)

            # Move to the next result set
            more_results = cursor.nextset()

            # If there are no more result sets, break out of the loop
            if not more_results:
                break
        for flight in result:
            planned = flight['Planned']
            planned = flight["Planned"].strftime("%m/%d/%Y %H:%M:%S")
            flight['Planned'] = planned
            estimated = ""
            if flight['Estimated'] is not None:
                estimated = flight["Estimated"].strftime("%m/%d/%Y %H:%M:%S")
                flight["Estimated"] = estimated
    # Format the query result as a JSON string and return it
    return json.dumps(result, indent=2), 200

    


app.run()
