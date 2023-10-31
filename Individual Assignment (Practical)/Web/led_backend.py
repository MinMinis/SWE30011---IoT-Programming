import serial
import MySQLdb
from flask import Flask, render_template

app = Flask(__name__)

sensors = {
    1 : {'name' : 'Humidity', 'state' : 0 },
    2 : {'name' : 'Temperature', 'state' : 0 },
}
database = {
    1 : {'name' : 'Database', 'state' : 0 },
    2 : [],
}


def read_sensor_data(): # Update the sensor data
    global sensors # Access the global variable sensors
    global database # Access the global variable database
    sensor = ser.readline() # Read the data from the Arduino
    print(sensor)
    sensor_str = sensor.decode('utf-8')  # Decode the bytes to a string
    for line_sensor in sensor_str.split('\n'): # Split the string into lines
        if line_sensor.startswith('Humidity'): # Check if the line starts with Humidity
            sensors[1]['state'] = float(line_sensor.split('=')[1].strip()) # Get the value after the =
        elif line_sensor.startswith('Temperature'): # Check if the line starts with Temperature
            sensors[2]['state'] = float(line_sensor.split('=')[1].strip()) # Get the value after the =
def connect_to_database():
    try:
        return MySQLdb.connect("localhost", "pi", "", "sensor_data")
    except Exception as e:
        ser.write(b"4")  # write serial input for Arduino code to trigger red light
        print(f"Error connecting to the database: {e}")
        return None
# Main function when accessing the website
@app.route("/") # This is the main page
def index(): # This function will be executed when the main page is accessed
    read_sensor_data() # Update the sensor data
    # TODO: Read the status of the pins ON/OFF and update dictionary
    # This data will be sent to index.html (pins dictionary)
    templateData = { 'sensors' : sensors, 'database' :database } # Create a dictionary with the data to be sent
    # Pass the template data into the template index.html and return it
    return render_template('index.html', **templateData) # Return the template

# Function with buttons to toggle to store the data into the database or not
@app.route("/<toggleDatabase>")
def toggle_store_data(toggleDatabase): # This function will be executed when the main page is accessed
    read_sensor_data() # Update the sensor data
    dbConn = None
    try:
        dbConn = connect_to_database()
        if dbConn:
            cursor = dbConn.cursor()
            if toggleDatabase == "storeData":
                database[1]['state'] = 1
                ser.write(b"2")
                # Insert the data into the database
                cursor.execute("INSERT INTO sensor_data (humidity, temperature) VALUES (%s, %s)",
                               (str(sensors[1]['state']), str(sensors[2]['state'])))
                dbConn.commit()
                print("Data stored in the database")
                cursor.execute("SELECT * FROM sensor_data ORDER BY dataID DESC LIMIT 10")
                rows = cursor.fetchall()
                for row in rows:
                    database[2].append({'humidity': row[1], 'temperature': row[2], 'time_stamp': row[3]})
            elif toggleDatabase == "noStoreData":
                database[1]['state'] = 0
                ser.write(b"3")

            elif toggleDatabase == "getDatabase":
                cursor.execute("SELECT * FROM sensor_data ORDER BY dataID DESC LIMIT 10")
                rows = cursor.fetchall()
                for row in rows:
                    database[2].append({'humidity': row[1], 'temperature': row[2], 'time_stamp': row[3]})
    finally:
        while len(database[2]) > 10:
            database[2].pop(0)
        if dbConn:
            dbConn.close()
    templateData = { 'sensors' : sensors, 'database' : database }
    return render_template('index.html', **templateData) # Return the template
@app.route("/automatically")
def automatic():
    read_sensor_data() # Update the sensor data
    ser.write(b"1") #write serial input for Arduino code to trigger automatic code
    templateData = { 'sensors' : sensors, 'database' : database }
    return render_template('index.html', **templateData)

#get data directly from arduino and send to the website
@app.route("/getData")
def getData():
    read_sensor_data() # Update the sensor data
    templateData = { 'sensors' : sensors, 'database' : database }
    return render_template('index.html', **templateData)

# Main function when accessing the website
if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout = 1)
    ser.flush()
    app.run(host='0.0.0.0', port = 80, debug = True)
