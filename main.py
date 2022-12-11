import requests
import json
import mysql.connector
import FlightData
from time import sleep

mydb = mysql.connector.connect(
  host="lin-13041-7784-mysql-primary.servers.linodedb.net",
  user="linroot",
  passwd="7ZmXl9xm9J@qsBIZ",
  database="Departures"
)


while True:

    mycursor = mydb.cursor()

    url = "https://www.mit.gl/wp-content/themes/mitgl/webservice.php?type=Departures&icao=BGJN"

    response = requests.get(url)
    data = response.json()

    for row in data:
        

        f = FlightData.Flight(
            Rute=row['Rute'],
            DepartureAirport = row['DepartureAirport'],
            ArrivalAirport = row['ArrivalAirport'],
            Planned = row['Planned'],
            Estimated = row['Estimated'],
            FlightHash = row['FlightHash'],
            ArrivalICAO = row['ArrivalICAO'],
            DepartureICAO = row['DepartureICAO'],
            DeparturingRooms = None,
            Status_kl = row['Status']['kl'],
            Status_en = row['Status']['en'],
            Status_da = row['Status']['da']
        )

        f.save(mydb)

    sleep(60)


