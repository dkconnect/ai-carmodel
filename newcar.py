from flask import Flask, render_template, Response
import threading
import pygame
import cv2
import numpy as np

app = Flask(__name__)

# Initialize Pygame and create a surface to render on
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Car Training Visualization")

def run_pygame():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        screen.fill((0, 0, 0))  # Clear screen with black

        # Example: Draw a red circle for visualization (replace with your car drawing logic)
        pygame.draw.circle(screen, (255, 0, 0), (400, 300), 50)

        pygame.display.flip()  # Update the display

# Function to generate frames
def generate_frames():
    while True:
        # Create a numpy array from the screen surface
        frame = pygame.surfarray.array3d(screen)
        frame = np.rot90(frame)
        frame = np.flipud(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Encode the frame to JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # Start the Pygame loop in a separate thread
    threading.Thread(target=run_pygame).start()

    # Start the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)
