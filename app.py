from flask import Flask, render_template, request, jsonify, Response
import time
from camera import generate_frames  # Import the video streaming functions and camera object

from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

app = Flask(__name__, template_folder="templates")

x_joy_value = None
y_joy_value = None

# Initialize I2C bus and PCA9685 board
i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c)
pca.frequency = 50  # Set the PWM frequency (adjust based on your servo specifications)

# Create servo objects for X and Y servos
x_servo = servo.Servo(pca.channels[0])  # Channel 0 for X servo
y_servo = servo.Servo(pca.channels[1])  # Channel 1 for Y servo

@app.route('/process_joystick_data', methods=['POST'])
def process_joystick_data():
    global x_joy_value, y_joy_value
    joystick_data = request.get_json()
    print('Received joystick data:', joystick_data)

    # Access the x, y, and cardinalDirection values
    x_joy_value = int(joystick_data['x'])
    y_joy_value = int(joystick_data['y'])
    cardinal_direction = joystick_data['cardinalDirection']

    print('X value:', x_joy_value)
    print('Y value:', y_joy_value)
    print('Cardinal Direction:', cardinal_direction)

    # Convert joystick values to servo angles
    x_angle = map_value(x_joy_value, -100, 100, 0, 60)
    y_angle = map_value(y_joy_value, -100, 100, 0, 60)

    # Set servo angles
    x_servo.angle = x_angle
    y_servo.angle = y_angle

    return jsonify({'message': 'Joystick data received successfully'})

@app.route("/", methods=["GET", "POST"])
def control_servo():
    global x_joy_value, y_joy_value
    x_value = x_joy_value
    y_value = y_joy_value
    error_message = None

    if request.method == "POST":
        try:
            x_value = x_joy_value
            y_value = y_joy_value

            # Validate range for X and Y values (adjust based on your requirements)
            if x_value < -100 or x_value > 100:
                raise ValueError("X value out of range (-100 to 100)")
            if y_value < -100 or y_value > 100:
                raise ValueError("Y value out of range (-100 to 100)")

        except ValueError as e:
            error_message = str(e)

    return render_template("index.html", x_value=x_value, y_value=y_value, error_message=error_message)

# Function for value mapping (adjust based on your specific servo behavior)
def map_value(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

# Route for video streaming
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
