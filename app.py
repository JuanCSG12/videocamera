import socketio
import time
from flask import Response, Flask, render_template
from threading import Thread, Lock


global video_frame
video_frame = None

global thread_lock
thread_lock = Lock()

class CSICamera:
    '''
    Camera for Jetson Nano IMX219 based camera
    Credit: https://github.com/feicccccccc/donkeycar/blob/dev/donkeycar/parts/camera.py
    gstreamer init string from https://github.com/NVIDIA-AI-IOT/jetbot/blob/master/jetbot/camera.py
    '''

    def gstreamer_pipeline(self, capture_width=1280, capture_height=720, output_width=1280, output_height=720,
                           framerate=60, flip_method=0):
        camera='nvarguscamerasrc sensor-id=0 ee-mode=1 ee-strength=0 tnr-mode=2 tnr-strength=1 wbmode=3 ! video/x-raw(memory:NVMM), width=%d, height=%d, format=(string)NV12, framerate=(fraction)%d/1 ! nvvidconv flip-method=%d ! nvvidconv ! video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! videoconvert ! appsink drop=True'
        return camera % (
            capture_width, capture_height, framerate, flip_method, output_width, output_height)

    def __init__(self, image_w=1280, image_h=720, image_d=3, capture_width=1280, capture_height=720, framerate=60,
                 gstreamer_flip=2):
        '''
        gstreamer_flip = 0 - no flip
        gstreamer_flip = 1 - rotate CCW 90
        gstreamer_flip = 2 - flip vertically
        gstreamer_flip = 3 - rotate CW 90
        '''
        self.w = image_w
        self.h = image_h
        self.running = True
        self.frame = None
        self.flip_method = gstreamer_flip
        self.capture_width = capture_width
        self.capture_height = capture_height
        self.framerate = framerate

        self.w = image_w
        self.h = image_h
        self.running = True
        self.frame = None
        self.flip_method = gstreamer_flip
        self.capture_width = capture_width
        self.capture_height = capture_height
        self.framerate = framerate


    def init_camera(self):
        import cv2

        # initialize the camera and stream
        self.camera = cv2.VideoCapture(
            self.gstreamer_pipeline(
                capture_width=self.capture_width,
                capture_height=self.capture_height,
                output_width=self.w,
                output_height=self.h,
                framerate=self.framerate,
                flip_method=self.flip_method),
            cv2.CAP_GSTREAMER)

        self.poll_camera()
        print('CSICamera loaded.. .warming camera')
        time.sleep(2)

    def update(self):
        self.init_camera()
        while self.running:
            self.poll_camera()

    def poll_camera(self):
        global video_frame, thread_lock
        import cv2
        self.ret, frame = self.camera.read()
        if frame is not None:
            with thread_lock:
                video_frame = frame.copy()

            self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    def run(self):
        self.poll_camera()

        return self.frame

    def run_threaded(self):
        return self.frame

    def shutdown(self):
        self.running = False
        print('stopping CSICamera')
        time.sleep(.5)
        del self.camera
class CSICamera1:
    '''
    Camera for Jetson Nano IMX219 based camera
    Credit: https://github.com/feicccccccc/donkeycar/blob/dev/donkeycar/parts/camera.py
    gstreamer init string from https://github.com/NVIDIA-AI-IOT/jetbot/blob/master/jetbot/camera.py
    '''

    def gstreamer_pipeline(self, capture_width=1280, capture_height=720, output_width=1280, output_height=720,
                           framerate=60, flip_method=0):
        camera='nvarguscamerasrc sensor-id=1 ee-mode=1 ee-strength=0 tnr-mode=2 tnr-strength=1 wbmode=3 ! video/x-raw(memory:NVMM), width=%d, height=%d, format=(string)NV12, framerate=(fraction)%d/1 ! nvvidconv flip-method=%d ! nvvidconv ! video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! videoconvert ! appsink drop=True'
        return camera % (
            capture_width, capture_height, framerate, flip_method, output_width, output_height)

    def __init__(self, image_w=1280, image_h=720, image_d=3, capture_width=1280, capture_height=720, framerate=60,
                 gstreamer_flip=2):
        '''
        gstreamer_flip = 0 - no flip
        gstreamer_flip = 1 - rotate CCW 90
        gstreamer_flip = 2 - flip vertically
        gstreamer_flip = 3 - rotate CW 90
        '''
        self.w = image_w
        self.h = image_h
        self.running = True
        self.frame = None
        self.flip_method = gstreamer_flip
        self.capture_width = capture_width
        self.capture_height = capture_height
        self.framerate = framerate

        self.w = image_w
        self.h = image_h
        self.running = True
        self.frame = None
        self.flip_method = gstreamer_flip
        self.capture_width = capture_width
        self.capture_height = capture_height
        self.framerate = framerate


    def init_camera(self):
        import cv2

        # initialize the camera and stream
        self.camera = cv2.VideoCapture(
            self.gstreamer_pipeline(
                capture_width=self.capture_width,
                capture_height=self.capture_height,
                output_width=self.w,
                output_height=self.h,
                framerate=self.framerate,
                flip_method=self.flip_method),
            cv2.CAP_GSTREAMER)

        self.poll_camera()
        print('CSICamera loaded.. .warming camera')
        time.sleep(2)

    def update(self):
        self.init_camera()
        while self.running:
            self.poll_camera()

    def poll_camera(self):
        import cv2
        ret, frame = self.camera.read()
        if frame is not None:
            self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    def run(self):
        self.poll_camera()

        return self.frame

    def run_threaded(self):
        return self.frame

    def shutdown(self):
        self.running = False
        print('stopping CSICamera')
        time.sleep(.5)
        del self.camera

def encodeFrame():
    global thread_lock
    import cv2
    while True:
        # Acquire thread_lock to access the global video_frame objects
        with thread_lock:
            global video_frame
            if video_frame is None:
                continue
            frame1 = video_frame.copy()
            frame2 = cam1.run_threaded()  # Captura el frame de la segunda cámara

        # Resize las imágenes al tamaño deseado
        frame1 = cv2.resize(frame1, (640, 720))
        frame2 = cv2.resize(frame2, (640, 720))

        # Combina las imágenes horizontalmente
        panoramic_frame = cv2.hconcat([frame1, frame2])

        # Codifica la imagen combinada
        return_key, encoded_image = cv2.imencode(".jpg", panoramic_frame)
        if not return_key:
            continue

        # Output image as a byte array
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(encoded_image) + b'\r\n')


# Create the Flask object for the application
app = Flask(__name__)

@app.route("/")
def Hola():
    return render_template('index.html')

@app.route("/video")
def streamFrames():
    return Response(encodeFrame(), mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == '__main__':
    cam = CSICamera(image_w=640, image_h=720, capture_width=1280, capture_height=720)
    cam1 = CSICamera1(image_w=640, image_h=720, capture_width=1280, capture_height=720)
    # Create a thread and attach the method that captures the image frames, to it
    process_thread = Thread(target=cam.update)
    process_thread1 = Thread(target=cam1.update)
    process_thread.daemon = True
    process_thread1.daemon = True

    # Start the thread
    process_thread.start()
    process_thread1.start()

    # start the Flask Web Application
    # While it can be run on any feasible IP, IP = 0.0.0.0 renders the web app on
    # the host machine's localhost and is discoverable by other machines on the same network
    app.run("0.0.0.0", port="8080")
