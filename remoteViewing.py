from flask import Flask, render_template, Response, request
import cv2

remote_viewing_app = Flask(__name__)

# Camera class to handle video capture
class Camera:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        
    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None
        # Convert the frame to JPEG format
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

    def __del__(self):
        self.cap.release()

@remote_viewing_app.route('/', methods=['GET', 'POST'])
def move():
    result = ""
    if request.method == 'POST':
        # Handle POST requests here
        return render_template('index.html', res_str=result)
                        
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        if frame is None:
            break
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@remote_viewing_app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

