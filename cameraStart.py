import io
from picamera import PiCamera
from flask import Flask, Response
from gevent.pywsgi import WSGIServer

app = Flask(__name__)

def generate_frames():
    with PiCamera() as camera:
        # Lower resolution and moderate frame rate for minimal lag
        camera.resolution = (320, 240)  # Lower resolution reduces bandwidth
        camera.framerate = 30  # Higher framerate for smoother video
        stream = io.BytesIO()

        # Continuous frame capture
        for _ in camera.capture_continuous(stream, format='jpeg', use_video_port=True):
            stream.seek(0)
            # Yield each frame as a multipart HTTP response
            frame = stream.read()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            stream.seek(0)
            stream.truncate()

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # Use gevent WSGI server for better performance
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()
