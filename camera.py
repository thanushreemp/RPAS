
import cv2
import time


def generate_frames():
    cap = cv2.VideoCapture(0)
    
    # Set the camera capture frame rate
    cap.set(cv2.CAP_PROP_FPS, 60)

    # Initialize variables for FPS calculation
    start_time = time.time()
    frames_captured = 0
    fps = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        else:
            # Calculate FPS
            frames_captured += 1
            elapsed_time = time.time() - start_time
            if elapsed_time >= 1:
                fps = frames_captured / elapsed_time
                start_time = time.time()
                frames_captured = 0

            # Put FPS text on the frame
            cv2.putText(frame, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                    


