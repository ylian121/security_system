from flask import Flask, render_template, Response, request
import cv2

app = Flask(__name__)

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

@app.route('/', methods=['GET', 'POST'])
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

@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001,debug=True, threaded=True)