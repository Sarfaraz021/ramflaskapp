from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

# Function to access the camera and capture snapshots
def get_camera():
    camera = cv2.VideoCapture(0)  # 0 for default camera
    while True:
        success, frame = camera.read()
        if not success:
            break
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    camera.release()

# Route to render the index.html template
@app.route('/')
def index():
    return render_template('index.html')

# Route to stream camera feed
@app.route('/video_feed')
def video_feed():
    return Response(get_camera(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
