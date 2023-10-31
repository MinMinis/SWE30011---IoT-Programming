import serial

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

while True:
    line = ser.readline()
    try:
        decoded_line = line.decode('utf-8')  # Decode the bytes to a string
        print(decoded_line)
    except UnicodeDecodeError as e:
        print(f"Error decoding line: {e}. Raw bytes: {line}")
