import mysql.connector

class Flight:
    def __init__(self, Rute, DepartureAirport, ArrivalAirport, Planned, Estimated, FlightHash, ArrivalICAO, DepartureICAO, DeparturingRooms, Status_kl, Status_en, Status_da):
        self.Rute = Rute
        self.DepartureAirport = DepartureAirport
        self.ArrivalAirport = ArrivalAirport
        self.Planned = Planned
        self.Estimated = Estimated
        self.FlightHash = FlightHash
        self.ArrivalICAO = ArrivalICAO
        self.DepartureICAO = DepartureICAO
        self.DeparturingRooms = None
        self.Status_kl = Status_kl
        self.Status_en = Status_en
        self.Status_da = Status_da

    def save(self, db):
        # Check if the flight already exists in the database
        with db.cursor() as cursor:
            sql = "SELECT * FROM Flights WHERE FlightHash = %s"
            cursor.execute(sql, (self.FlightHash,))
            result = cursor.fetchone()

        # If the flight already exists, update the existing row
        if result:
            with db.cursor() as cursor:
                sql = "UPDATE Flights SET Rute = %s, DepartureAirport = %s, ArrivalAirport = %s, Planned = %s, Estimated = %s, FlightHash = %s, ArrivalICAO = %s, DepartureICAO = %s, DeparturingRooms = %s, Status_kl = %s, Status_en = %s, Status_da = %s WHERE FlightHash = %s"
                values = (
                    self.Rute,
                    self.DepartureAirport,
                    self.ArrivalAirport,
                    self.Planned,
                    self.Estimated,
                    self.FlightHash,
                    self.ArrivalICAO,
                    self.DepartureICAO,
                    self.DeparturingRooms,
                    self.Status_kl,
                    self.Status_en,
                    self.Status_da,
                    self.FlightHash
                )
                cursor.execute(sql, values)
            print("Row updated")
        else:
            # If the flight doesn't exist, insert a new row
            with db.cursor() as cursor:
                    sql = "INSERT INTO Flights (Rute, DepartureAirport, ArrivalAirport, Planned, Estimated, FlightHash, ArrivalICAO, DepartureICAO, DeparturingRooms, Status_kl, Status_en, Status_da) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    val = (self.rute, self.departureAirport, self.arrivalAirport, self.planned, self.estimated, self.flightHash, self.arrivalICAO, self.departureICAO, self.departuringRooms, self.status_kl, self.status_en, self.status_da)
                    cursor.execute(sql, val)
            
            print("Row inserted")
        db.commit()




def find_rooms_by_hash(cursor, hash):
    sql = "SELECT * FROM Rooms WHERE FlightHash = %s"
    cursor.execute(sql, (hash,))
    results = cursor.fetchall()
    return results       