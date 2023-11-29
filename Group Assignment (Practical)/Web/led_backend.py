import serial
import MySQLdb
from flask import Flask, render_template
import paho.mqtt.publish as publish
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

app = Flask(__name__)
topic = "v1/devices/me/telemetry"
device='/dev/ttyUSB0'
device_id = "OwvtaAzFoOYeUU1WSILH"
ser = serial.Serial(device, 9600, timeout=1)  # Establish the connection on a specific port
hostname = "192.168.153.131"
port = 1884
sensors = { # Dictionary with the sensors
    1 : {'name' : 'Humidity', 'state' : 0 },
    2 : {'name' : 'Temperature', 'state' : 0 },
}
database = { # Dictionary with the database
    1 : {'name' : 'Database', 'state' : 0 },
    2 : [],
}
def read_sensor_data(): # Update the sensor data
    global sensors # Access the global variable sensors
    global database # Access the global variable database
    sensor = ser.readline() # Read the data from the Arduino
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
def send_to_cloud():
    try:
        # mosquitto_pub -d -q 1 -h 192.168.153.131 -p 1884 -t v1/devices/me/telemetry -u OwvtaAzFoOYeUU1WSILH -m "{temperature:29,humidity:50}"
        # Use subprocess to run mosquitto_pub command
        temperature = sensors[2]['state']
        humidity = sensors[1]['state']
        publish.single(topic, f'{{"temperature":{temperature},"humidity":{humidity}}}', hostname=hostname, port=port, qos=1, auth={'username': device_id})
    except Exception as e:
        ser.write(b"4")  # write serial input for Arduino code to trigger red light
        print(f"Error sending data to the cloud: {e}")
def print_sensor_data():
    print(f"Humidity: {sensors[1]['state']}")
    print(f"Temperature: {sensors[2]['state']}")
def update_sensor_data_and_send_to_cloud():
    read_sensor_data()
    send_to_cloud()

# Main function when accessing the website
@app.route("/") # This is the main page
def index(): # This function will be executed when the main page is accessed
    read_sensor_data()
    templateData = { 'sensors' : sensors, 'database' :database } # Create a dictionary with the data to be sent
    return render_template('index.html', **templateData) # Return the template

# Function with buttons to toggle to store the data into the database or not
@app.route("/<toggleDatabase>")
def toggle_store_data(toggleDatabase): # This function will be executed when the main page is accessed
    update_sensor_data_and_send_to_cloud()  # Update and send data immediately
    dbConn = None
    try:
        dbConn = connect_to_database() # Connect to the database
        if dbConn:
            cursor = dbConn.cursor() # Create a cursor
            if toggleDatabase == "storeData": # Check if the button is storeData
                database[1]['state'] = 1 # Turn on the database
                ser.write(b"2") # write serial input for Arduino code to trigger green light
                # Insert the data into the database
                cursor.execute("INSERT INTO sensor_data (humidity, temperature) VALUES (%s, %s)",
                               (str(sensors[1]['state']), str(sensors[2]['state'])))
                dbConn.commit() # Commit the changes
                print("Data stored in the database") # Print a message
                cursor.execute("SELECT * FROM sensor_data ORDER BY dataID DESC LIMIT 10") # Get the last 10 data
                rows = cursor.fetchall() # Fetch the rows
                for row in rows: # Loop through the rows
                    database[2].append({'humidity': row[1], 'temperature': row[2], 'time_stamp': row[3]}) # Append the data to the database
            elif toggleDatabase == "noStoreData": # Check if the button is noStoreData
                database[1]['state'] = 0 # Turn off the database
                ser.write(b"3") # write serial input for Arduino code to trigger red light

            elif toggleDatabase == "getDatabase":  # Check if the button is getDatabase
                cursor.execute("SELECT * FROM sensor_data ORDER BY dataID DESC LIMIT 10") # Get the last 10 data
                rows = cursor.fetchall()
                for row in rows:
                    database[2].append({'humidity': row[1], 'temperature': row[2], 'time_stamp': row[3]})
    except paho.mqtt.MQTTException as mqtt_error:
        ser.write(b"4")  # write serial input for Arduino code to trigger red light
        print(f"MQTT Exception: {mqtt_error}")
        # Handle the MQTT connection error here (e.g., log, send notification, etc.)

    finally:
        while len(database[2]) > 10:  # Check if the database is greater than 10
            if database[2]:
                try:
                    database[2].pop(0)  # Remove the first element
                except IndexError:
                    break  # Break out of the loop if the list is empty or index is out of range
            else:
                break  # Break out of the loop if the list is empty
        if dbConn: # Close the database
            dbConn.close()
    templateData = { 'sensors' : sensors, 'database' : database } # Create a dictionary with the data to be sent
    return render_template('index.html', **templateData) # Return the template
@app.route("/automatically") #URL/automatically
def automatic():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_sensor_data_and_send_to_cloud, trigger=IntervalTrigger(seconds=2))
    scheduler.add_job(print_sensor_data, trigger=IntervalTrigger(seconds=2))
    scheduler.start()
    ser.write(b"1") #write serial input for Arduino code to trigger automatic code
    templateData = { 'sensors' : sensors, 'database' : database }
    return render_template('index.html', **templateData)
#get data directly from arduino and send to the website
@app.route("/getData") #URL/getData
def getData():
    read_sensor_data()
    templateData = { 'sensors' : sensors, 'database' : database } # Create a dictionary with the data to be sent
    return render_template('index.html', **templateData) # Return the template
# Main function when accessing the website
if __name__ == '__main__':
    ser = serial.Serial(device, 9600, timeout = 1) # Establish the connection on a specific port
    ser.flush() # Clear the serial buffer
    app.run(host='0.0.0.0', port = 80, debug = True) # Run the app
