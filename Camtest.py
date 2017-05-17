""""
SENDS VIDEO AND SOUND TO WEB INTERFACE
"""
import cv2

from flask import Flask, render_template, Response

app = Flask(__name__)

"""CLASSES"""
class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(1)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

"""LOCAL METHODS"""
def generateImage(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

        

"""FLASK METHODS"""
@app.route("/wav")
def streamwav():
    def generate():
        with open("signals/song.wav", "rb") as fwav:
            data = fwav.read(1024)
            while data:
                yield data
                data = fwav.read(1024)
    return Response(generate(), mimetype="audio/x-wav")

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(generateImage(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

"""MAIN TRIGGER"""
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)