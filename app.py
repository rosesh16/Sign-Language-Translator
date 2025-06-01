"""
Real-Time Sign Language Translation Web Application
Complete single-file solution for NGO and accessibility use

This application combines:
- Flask web server
- MediaPipe hand detection  
- OpenCV video processing
- Your original recognition algorithm from Function.py
"""

from flask import Flask, render_template_string, Response, jsonify
import cv2 as cv
import mediapipe as mp
import numpy as np
import base64
import time

app = Flask(__name__)

# Global variables for video processing
camera = None
is_camera_active = False
current_gesture = ""
gesture_history = []
max_history = 50

# MediaPipe setup
mp_hands = mp.solutions.hands # pyright: ignore[reportAttributeAccessIssue]
mp_drawing = mp.solutions.drawing_utils # type: ignore

#==============================================================================
# GESTURE RECOGNITION ENGINE (from your original Function.py)
#==============================================================================

def persons_input(hand_coordinates):
    """
    Core gesture recognition function - your original algorithm
    """
    def distance(x1,y1,x2,y2):
        distance=int((((x1-x2)**2)+((y1-y2)**2))**(1/2))
        return distance
    
    persons_input=""
    
    # Consider pawn is Vertical
    hand_horz=False
    
    # Consider all fingure are Down
    thumbs_up=False
    index_up=False
    middel_up=False
    ring_up=False
    littel_up=False
    
    # Here I am using Hand Cordinates(HC) values , which we got from video input.
    # With the help of HC values , I can determine wither the fingure is UP or DOWN
    # In "hand_cordinate[12][1]" , "12" is the index and "1" is X_cordinate (and "2" for Y_cordinate) 
    # For more information, refer the "HAND_CORD" image (to understand the HC)
    
    if distance(hand_coordinates[0][2],0,hand_coordinates[12][2],0) < distance(hand_coordinates[0][1],0,hand_coordinates[12][1],0):
        hand_horz=True
    if distance(hand_coordinates[0][1],hand_coordinates[0][2],hand_coordinates[3][1],hand_coordinates[3][2]) < distance(hand_coordinates[0][1],hand_coordinates[0][2],hand_coordinates[4][1],hand_coordinates[4][2]):
        thumbs_up=True  
    if distance(hand_coordinates[0][1],hand_coordinates[0][2],hand_coordinates[6][1],hand_coordinates[6][2]) < distance(hand_coordinates[0][1],hand_coordinates[0][2],hand_coordinates[8][1],hand_coordinates[8][2]):
        index_up=True
    if distance(hand_coordinates[0][1],hand_coordinates[0][2],hand_coordinates[10][1],hand_coordinates[10][2]) < distance(hand_coordinates[0][1],hand_coordinates[0][2],hand_coordinates[12][1],hand_coordinates[12][2]):
        middel_up=True
    if distance(hand_coordinates[0][1],hand_coordinates[0][2],hand_coordinates[14][1],hand_coordinates[14][2]) < distance(hand_coordinates[0][1],hand_coordinates[0][2],hand_coordinates[16][1],hand_coordinates[16][2]):
        ring_up=True
    if distance(hand_coordinates[0][1],hand_coordinates[0][2],hand_coordinates[18][1],hand_coordinates[18][2]) < distance(hand_coordinates[0][1],hand_coordinates[0][2],hand_coordinates[20][1],hand_coordinates[20][2]):
        littel_up=True
        
    # Get persons_input according to HC values
    
    if index_up==False and middel_up==False and ring_up==False and littel_up==False and thumbs_up==True and hand_horz==False:
        if distance(hand_coordinates[4][1],hand_coordinates[4][2],hand_coordinates[16][1],hand_coordinates[16][2]) < distance(hand_coordinates[4][1],hand_coordinates[4][2],hand_coordinates[13][1],hand_coordinates[13][2]):
            persons_input=" O"
        elif distance(hand_coordinates[4][1],hand_coordinates[4][2],hand_coordinates[18][1],hand_coordinates[18][2]) < distance(hand_coordinates[14][1],hand_coordinates[14][2],hand_coordinates[18][1],hand_coordinates[18][2]):
            persons_input=" M"
        elif distance(hand_coordinates[4][1],hand_coordinates[4][2],hand_coordinates[18][1],hand_coordinates[18][2]) < distance(hand_coordinates[10][1],hand_coordinates[10][2],hand_coordinates[18][1],hand_coordinates[18][2]):
            persons_input=" N"
        elif distance(hand_coordinates[4][1],hand_coordinates[4][2],hand_coordinates[18][1],hand_coordinates[18][2]) < distance(hand_coordinates[6][1],hand_coordinates[6][2],hand_coordinates[18][1],hand_coordinates[18][2]):
            persons_input=" T"
        else :
            persons_input=" A"
    elif index_up==True and middel_up==True and ring_up==True and littel_up==True and thumbs_up==True and hand_horz==False:
        if distance(hand_coordinates[4][1],hand_coordinates[4][2],hand_coordinates[12][1],hand_coordinates[12][2]) < distance(hand_coordinates[4][1],hand_coordinates[4][2],hand_coordinates[11][1],hand_coordinates[11][2]):
            persons_input=" C"
        elif distance(hand_coordinates[4][1],hand_coordinates[4][2],hand_coordinates[17][1],hand_coordinates[17][2]) < distance(hand_coordinates[4][1],hand_coordinates[4][2],hand_coordinates[5][1],hand_coordinates[5][2]):
            persons_input=" B"
    elif index_up==False and middel_up==False and ring_up==False and littel_up==False and thumbs_up==False and hand_horz==False:
        if distance(hand_coordinates[20][1],hand_coordinates[20][2],hand_coordinates[4][1],hand_coordinates[4][2]) < distance(hand_coordinates[19][1],hand_coordinates[19][2],hand_coordinates[4][1],hand_coordinates[4][2]):
            persons_input=" E"
        else:
            persons_input=" S"
    elif index_up==False and middel_up==True and ring_up==True and littel_up==True and thumbs_up==True and hand_horz==False:
        persons_input=" F"
    elif index_up==True and middel_up==False and ring_up==False and littel_up==False and thumbs_up==True and hand_horz==True:
        if distance(hand_coordinates[8][1],hand_coordinates[8][2],hand_coordinates[4][1],hand_coordinates[4][2]) < distance(hand_coordinates[6][1],hand_coordinates[6][2],hand_coordinates[4][1],hand_coordinates[4][2]):
            persons_input=" Q"
        elif distance(hand_coordinates[12][1],hand_coordinates[12][2],hand_coordinates[4][1],hand_coordinates[4][2]) < distance(hand_coordinates[10][1],hand_coordinates[10][2],hand_coordinates[4][1],hand_coordinates[4][2]):
            persons_input=" P"
        else:
            persons_input=" G"
    elif index_up==True and middel_up==True and ring_up==False and littel_up==False and thumbs_up==True and hand_horz==True:
        if distance(hand_coordinates[12][1],hand_coordinates[12][2],hand_coordinates[4][1],hand_coordinates[4][2]) < distance(hand_coordinates[10][1],hand_coordinates[10][2],hand_coordinates[4][1],hand_coordinates[4][2]):
            persons_input=" P"
        else:
            persons_input=" H"
    elif index_up==False and middel_up==False and ring_up==False and littel_up==True and thumbs_up==False and hand_horz==False:
        persons_input=" I"
    elif index_up==False and middel_up==False and ring_up==False and littel_up==True and thumbs_up==False and hand_horz==True:
        persons_input=" J"
    elif index_up==True and middel_up==True and ring_up==False and littel_up==False and thumbs_up==True and hand_horz==False:
        if hand_coordinates[8][1] < hand_coordinates[12][1]:
            persons_input=" R"
        elif distance(hand_coordinates[4][1],hand_coordinates[4][2],hand_coordinates[14][1],hand_coordinates[14][2]) < distance(hand_coordinates[9][1],hand_coordinates[9][2],hand_coordinates[14][1],hand_coordinates[14][2]):
            if 2*distance(hand_coordinates[5][1],hand_coordinates[5][2],hand_coordinates[9][1],hand_coordinates[9][2]) < distance(hand_coordinates[8][1],hand_coordinates[8][2],hand_coordinates[12][1],hand_coordinates[12][2]):
                persons_input=" V"
            else:
                persons_input=" U"
        elif distance(hand_coordinates[4][1],hand_coordinates[4][2],hand_coordinates[14][1],hand_coordinates[14][2]) < distance(hand_coordinates[5][1],hand_coordinates[5][2],hand_coordinates[14][1],hand_coordinates[14][2]):
            persons_input=" K"
    elif index_up==True and middel_up==False and ring_up==False and littel_up==False and thumbs_up==True and hand_horz==False:
        if distance(hand_coordinates[3][1],hand_coordinates[3][2],hand_coordinates[14][1],hand_coordinates[14][2]) < distance(hand_coordinates[14][1],hand_coordinates[14][2],hand_coordinates[4][1],hand_coordinates[4][2]):
            persons_input=" L"
        elif distance(hand_coordinates[8][1],hand_coordinates[8][2],hand_coordinates[10][1],hand_coordinates[10][2]) < distance(hand_coordinates[6][1],hand_coordinates[6][2],hand_coordinates[10][1],hand_coordinates[10][2]):
            persons_input=" X"
        else:
            persons_input=" D"
    elif index_up==True and middel_up==True and ring_up==False and littel_up==False and thumbs_up==False and hand_horz==False:
        if hand_coordinates[8][1] < hand_coordinates[12][1]:
            persons_input=" R"
        elif 2*distance(hand_coordinates[5][1],hand_coordinates[5][2],hand_coordinates[9][1],hand_coordinates[9][2]) < distance(hand_coordinates[8][1],hand_coordinates[8][2],hand_coordinates[12][1],hand_coordinates[12][2]):
            persons_input=" V"
        else:
            persons_input=" U"
    elif index_up==True and middel_up==True and ring_up==True and littel_up==False and thumbs_up==True and hand_horz==False:
        persons_input=" W"
    elif index_up==False and middel_up==False and ring_up==False and littel_up==True and thumbs_up==True and hand_horz==False:
        if distance(hand_coordinates[3][1],hand_coordinates[3][2],hand_coordinates[18][1],hand_coordinates[18][2]) < distance(hand_coordinates[4][1],hand_coordinates[4][2],hand_coordinates[18][1],hand_coordinates[18][2]):
            persons_input=" Y"
        else:
            persons_input=" I"
        
    return persons_input

#==============================================================================
# VIDEO CAMERA CLASS
#==============================================================================

class VideoCamera:
    def __init__(self):
        try:
            self.video = cv.VideoCapture(0)
            if not self.video.isOpened():
                print("Warning: Could not open camera. Check camera permissions.")
                self.video = None
            else:
                print("Camera initialized successfully")
            
            self.hands = mp_hands.Hands(
                static_image_mode=False,
                max_num_hands=1,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5
            )
        except Exception as e:
            print(f"Error initializing camera: {e}")
            self.video = None
            self.hands = None
    
    def __del__(self):
        if self.video and self.video.isOpened():
            self.video.release()
    
    def get_frame(self):
        try:
            if self.video is None or not self.video.isOpened():
                # Return a dummy frame
                dummy_frame = np.zeros((480, 640, 3), dtype=np.uint8)
                cv.putText(dummy_frame, "Camera not available", (50, 240), 
                          cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                ret, buffer = cv.imencode('.jpg', dummy_frame)
                frame = base64.b64encode(buffer).decode('utf-8') # type: ignore
                return frame, "", None
            
            success, image = self.video.read()
            if not success:
                return None, None, None
            
            # Process the image for hand detection
            image.flags.writeable = False
            image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
            
            if self.hands:
                results = self.hands.process(image)
            else:
                results = None
            
            # Draw the hand annotations on the image
            image.flags.writeable = True
            image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
            
            gesture = ""
            hand_landmarks_data = None
            
            if results and results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Draw landmarks on image
                    mp_drawing.draw_landmarks(
                        image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    
                    # Extract coordinates for recognition
                    img_h, img_w = image.shape[:2]
                    hand_coordinate = []
                    
                    for idx, landmark in enumerate(hand_landmarks.landmark):
                        x_coord = int(landmark.x * img_w)
                        y_coord = int(landmark.y * img_h)
                        hand_coordinate.append([idx, x_coord, y_coord])
                    
                    hand_coordinate = np.array(hand_coordinate)
                    gesture = persons_input(hand_coordinate)
                    hand_landmarks_data = hand_coordinate.tolist()
                    
                    # Draw bounding box
                    if len(hand_coordinate) > 0:
                        x_coords = hand_coordinate[:, 1]
                        y_coords = hand_coordinate[:, 2]
                        x_min, x_max = np.min(x_coords), np.max(x_coords)
                        y_min, y_max = np.min(y_coords), np.max(y_coords)
                        
                        # Draw rectangle and text
                        cv.rectangle(image, (x_min-10, y_min-10), (x_max+10, y_max+10), (0, 255, 0), 2)
                        cv.putText(image, gesture.strip(), (x_min-10, y_min-20), 
                                  cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Add status text
            cv.putText(image, f"Status: {'Active' if gesture else 'Ready'}", (10, 30), 
                      cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Flip image horizontally for mirror effect
            image = cv.flip(image, 1)
            
            # Encode image to base64 for web transmission
            ret, buffer = cv.imencode('.jpg', image)
            frame = base64.b64encode(buffer).decode('utf-8') # type: ignore
            
            return frame, gesture.strip(), hand_landmarks_data
            
        except Exception as e:
            print(f"Error in get_frame: {e}")
            return None, None, None

#==============================================================================
# FLASK ROUTES
#==============================================================================

def generate_frames():
    global camera, current_gesture, gesture_history
    
    while is_camera_active:
        if camera is None:
            try:
                camera = VideoCamera()
            except Exception as e:
                print(f"Error creating camera: {e}")
                break
        
        frame, gesture, landmarks = camera.get_frame()
        
        if frame:
            # Update current gesture and history
            if gesture and gesture != current_gesture:
                current_gesture = gesture
                timestamp = time.strftime("%H:%M:%S")
                gesture_entry = {
                    'gesture': gesture,
                    'timestamp': timestamp,
                    'landmarks': landmarks
                }
                gesture_history.append(gesture_entry)
                
                # Limit history size
                if len(gesture_history) > max_history:
                    gesture_history.pop(0)
                
                print(f"New gesture detected: {gesture} at {timestamp}")
            
            yield f"--frame\r\nContent-Type: image/jpeg\r\n\r\n"
            yield base64.b64decode(frame)
            yield f"\r\n"
        
        time.sleep(0.1)  # Control frame rate

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/start_camera')
def start_camera():
    global is_camera_active, camera
    try:
        if not is_camera_active:
            is_camera_active = True
            if camera is None:
                camera = VideoCamera()
            print("Camera started successfully")
        return jsonify({'status': 'started', 'message': 'Camera activated'})
    except Exception as e:
        print(f"Error starting camera: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/stop_camera')
def stop_camera():
    global is_camera_active, camera
    try:
        is_camera_active = False
        if camera:
            del camera
            camera = None
        print("Camera stopped successfully")
        return jsonify({'status': 'stopped', 'message': 'Camera deactivated'})
    except Exception as e:
        print(f"Error stopping camera: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), # type: ignore
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_current_gesture')
def get_current_gesture():
    return jsonify({
        'gesture': current_gesture,
        'timestamp': time.strftime("%H:%M:%S")
    })

@app.route('/get_gesture_history')
def get_gesture_history():
    return jsonify({'history': gesture_history})

@app.route('/clear_history')
def clear_history():
    global gesture_history
    gesture_history = []
    return jsonify({'status': 'cleared'})

@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'camera_active': is_camera_active,
        'current_gesture': current_gesture,
        'history_count': len(gesture_history)
    })

#==============================================================================
# HTML TEMPLATE (EMBEDDED)
#==============================================================================

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sign Language Translator</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #1e293b;
            line-height: 1.6;
            min-height: 100vh;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            min-height: 100vh;
        }

        .header {
            text-align: center;
            margin-bottom: 2rem;
            padding: 2rem 0;
            background: rgba(255,255,255,0.95);
            color: #2563eb;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);
        }

        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            background: linear-gradient(45deg, #2563eb, #7c3aed);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .subtitle {
            font-size: 1.1rem;
            opacity: 0.8;
            color: #64748b;
        }

        .main-content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2rem;
            align-items: start;
        }

        .video-section {
            background: rgba(255,255,255,0.95);
            border-radius: 15px;
            padding: 1.5rem;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);
        }

        .video-container {
            position: relative;
            width: 100%;
            height: 400px;
            border-radius: 12px;
            overflow: hidden;
            background: #000;
            margin-bottom: 1rem;
            border: 2px solid #e5e7eb;
        }

        #video-feed {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }

        .camera-placeholder {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100%;
            color: #64748b;
            background: linear-gradient(45deg, #f8fafc, #e2e8f0);
        }

        .camera-placeholder i {
            font-size: 3rem;
            margin-bottom: 1rem;
            opacity: 0.5;
        }

        .camera-controls {
            display: flex;
            gap: 1rem;
            justify-content: center;
        }

        .btn {
            padding: 0.75rem 1.5rem;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s ease;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 1rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .btn-primary {
            background: linear-gradient(45deg, #2563eb, #3b82f6);
            color: white;
            box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4);
        }

        .btn-primary:hover:not(:disabled) {
            background: linear-gradient(45deg, #1d4ed8, #2563eb);
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(37, 99, 235, 0.6);
        }

        .btn-secondary {
            background: linear-gradient(45deg, #64748b, #94a3b8);
            color: white;
            box-shadow: 0 4px 15px rgba(100, 116, 139, 0.4);
        }

        .btn-secondary:hover:not(:disabled) {
            background: linear-gradient(45deg, #475569, #64748b);
            transform: translateY(-2px);
        }

        .btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }

        .recognition-section {
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }

        .current-gesture {
            background: rgba(255,255,255,0.95);
            border-radius: 15px;
            padding: 2rem;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);
            text-align: center;
        }

        .current-gesture h2 {
            margin-bottom: 1.5rem;
            background: linear-gradient(45deg, #2563eb, #7c3aed);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .letter-display {
            font-size: 4rem;
            font-weight: 900;
            color: #2563eb;
            background: linear-gradient(135deg, #dbeafe, #bfdbfe);
            width: 120px;
            height: 120px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 3px solid #2563eb;
            margin: 0 auto 1rem;
            box-shadow: 0 8px 25px rgba(37, 99, 235, 0.3);
            transition: all 0.3s ease;
        }

        .letter-display.active {
            animation: pulse 1s ease-in-out;
        }

        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }

        .timestamp {
            color: #64748b;
            font-size: 0.875rem;
            font-weight: 500;
        }

        .history-section {
            background: rgba(255,255,255,0.95);
            border-radius: 15px;
            padding: 1.5rem;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);
            grid-column: 1 / -1;
            margin-top: 1rem;
        }

        .history-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
        }

        .history-header h3 {
            background: linear-gradient(45deg, #2563eb, #7c3aed);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .btn-small {
            padding: 0.5rem 1rem;
            font-size: 0.875rem;
        }

        .history-list {
            max-height: 200px;
            overflow-y: auto;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 1rem;
            background: #f8fafc;
        }

        .history-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.75rem;
            border-bottom: 1px solid #e2e8f0;
            border-radius: 8px;
            margin-bottom: 0.5rem;
            background: white;
            transition: all 0.2s ease;
        }

        .history-item:hover {
            background: #f1f5f9;
            transform: translateX(5px);
        }

        .history-item:last-child {
            border-bottom: none;
            margin-bottom: 0;
        }

        .history-gesture {
            font-size: 1.5rem;
            font-weight: bold;
            color: #2563eb;
        }

        .history-time {
            color: #64748b;
            font-size: 0.875rem;
            font-weight: 500;
        }

        .status-indicator {
            position: absolute;
            top: 1rem;
            right: 1rem;
            background: rgba(0,0,0,0.8);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.875rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            backdrop-filter: blur(10px);
        }

        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #ef4444;
            animation: blink 2s infinite;
        }

        .status-dot.online {
            background: #22c55e;
            animation: none;
        }

        @keyframes blink {
            0%, 50% { opacity: 1; }
            51%, 100% { opacity: 0.3; }
        }

        .footer {
            text-align: center;
            margin-top: 2rem;
            padding: 1rem;
            color: rgba(255,255,255,0.8);
            font-size: 0.9rem;
        }

        @media (max-width: 768px) {
            .main-content {
                grid-template-columns: 1fr;
            }
            
            .header h1 {
                font-size: 1.8rem;
            }
            
            .camera-controls {
                flex-direction: column;
            }
            
            .btn {
                width: 100%;
                justify-content: center;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <h1><i class="fas fa-hands"></i> Sign Language Translator</h1>
            <p class="subtitle">Real-time ASL alphabet recognition for accessibility</p>
        </header>

        <main class="main-content">
            <section class="video-section">
                <div class="video-container">
                    <img id="video-feed" src="" alt="Camera feed" style="display: none;">
                    <div id="camera-placeholder" class="camera-placeholder">
                        <i class="fas fa-video"></i>
                        <p>Click "Start Camera" to begin recognition</p>
                    </div>
                    <div class="status-indicator">
                        <span id="status-dot" class="status-dot"></span>
                        <span id="status-text">Offline</span>
                    </div>
                </div>
                
                <div class="camera-controls">
                    <button id="start-btn" class="btn btn-primary">
                        <i class="fas fa-play"></i> Start Camera
                    </button>
                    <button id="stop-btn" class="btn btn-secondary" disabled>
                        <i class="fas fa-stop"></i> Stop Camera
                    </button>
                </div>
            </section>

            <section class="recognition-section">
                <div class="current-gesture">
                    <h2><i class="fas fa-hand-paper"></i> Current Recognition</h2>
                    <div id="current-letter" class="letter-display">-</div>
                    <div id="current-timestamp" class="timestamp">Ready</div>
                </div>
            </section>

            <section class="history-section">
                <div class="history-header">
                    <h3><i class="fas fa-history"></i> Recognition History</h3>
                    <button id="clear-history" class="btn btn-small btn-secondary">
                        <i class="fas fa-trash"></i> Clear
                    </button>
                </div>
                <div id="history-list" class="history-list">
                    <div class="history-placeholder">No gestures recognized yet</div>
                </div>
            </section>
        </main>

        <footer class="footer">
            <p>&copy; 2024 Sign Language Translator - Built for Accessibility & NGO Use</p>
        </footer>
    </div>

    <script>
        let updateInterval = null;
        let isActive = false;

        const videoFeed = document.getElementById('video-feed');
        const cameraPlaceholder = document.getElementById('camera-placeholder');
        const startBtn = document.getElementById('start-btn');
        const stopBtn = document.getElementById('stop-btn');
        const statusDot = document.getElementById('status-dot');
        const statusText = document.getElementById('status-text');
        const currentLetter = document.getElementById('current-letter');
        const currentTimestamp = document.getElementById('current-timestamp');
        const historyList = document.getElementById('history-list');
        const clearHistoryBtn = document.getElementById('clear-history');

        startBtn.addEventListener('click', startCamera);
        stopBtn.addEventListener('click', stopCamera);
        clearHistoryBtn.addEventListener('click', clearHistory);

        function updateStatus(online) {
            if (online) {
                statusDot.classList.add('online');
                statusText.textContent = 'Connected';
            } else {
                statusDot.classList.remove('online');
                statusText.textContent = 'Offline';
            }
        }

        async function startCamera() {
            try {
                startBtn.disabled = true;
                startBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Starting...';
                
                const response = await fetch('/start_camera');
                const data = await response.json();
                
                if (data.status === 'started') {
                    videoFeed.src = '/video_feed';
                    videoFeed.style.display = 'block';
                    cameraPlaceholder.style.display = 'none';
                    
                    startBtn.style.display = 'none';
                    stopBtn.style.display = 'inline-flex';
                    stopBtn.disabled = false;
                    
                    updateStatus(true);
                    isActive = true;
                    startUpdating();
                }
            } catch (error) {
                console.error('Error starting camera:', error);
                alert('Failed to start camera');
            } finally {
                startBtn.disabled = false;
                startBtn.innerHTML = '<i class="fas fa-play"></i> Start Camera';
            }
        }

        async function stopCamera() {
            try {
                stopBtn.disabled = true;
                stopBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Stopping...';
                
                const response = await fetch('/stop_camera');
                const data = await response.json();
                
                if (data.status === 'stopped') {
                    videoFeed.style.display = 'none';
                    cameraPlaceholder.style.display = 'flex';
                    videoFeed.src = '';
                    
                    startBtn.style.display = 'inline-flex';
                    stopBtn.style.display = 'none';
                    startBtn.disabled = false;
                    
                    updateStatus(false);
                    isActive = false;
                    stopUpdating();
                    
                    currentLetter.textContent = '-';
                    currentLetter.classList.remove('active');
                    currentTimestamp.textContent = 'Ready';
                }
            } catch (error) {
                console.error('Error stopping camera:', error);
                alert('Failed to stop camera');
            } finally {
                stopBtn.disabled = false;
                stopBtn.innerHTML = '<i class="fas fa-stop"></i> Stop Camera';
            }
        }

        function startUpdating() {
            updateInterval = setInterval(async () => {
                if (!isActive) return;
                
                try {
                    // Get current gesture
                    const gestureResponse = await fetch('/get_current_gesture');
                    const gestureData = await gestureResponse.json();
                    
                    const newGesture = gestureData.gesture || '-';
                    if (newGesture !== currentLetter.textContent) {
                        currentLetter.textContent = newGesture;
                        currentLetter.classList.add('active');
                        setTimeout(() => currentLetter.classList.remove('active'), 1000);
                    }
                    currentTimestamp.textContent = gestureData.timestamp;
                    
                    // Get history
                    const historyResponse = await fetch('/get_gesture_history');
                    const historyData = await historyResponse.json();
                    
                    updateHistory(historyData.history);
                    
                } catch (error) {
                    console.error('Error updating data:', error);
                }
            }, 500);
        }

        function stopUpdating() {
            if (updateInterval) {
                clearInterval(updateInterval);
                updateInterval = null;
            }
        }

        function updateHistory(history) {
            if (history.length === 0) {
                historyList.innerHTML = '<div style="text-align: center; color: #64748b; padding: 2rem;">No gestures recognized yet</div>';
                return;
            }
            
            historyList.innerHTML = '';
            history.slice(-10).reverse().forEach(item => {
                const historyItem = document.createElement('div');
                historyItem.className = 'history-item';
                historyItem.innerHTML = `
                    <span class="history-gesture">${item.gesture}</span>
                    <span class="history-time">${item.timestamp}</span>
                `;
                historyList.appendChild(historyItem);
            });
        }

        async function clearHistory() {
            try {
                const response = await fetch('/clear_history');
                const data = await response.json();
                
                if (data.status === 'cleared') {
                    historyList.innerHTML = '<div style="text-align: center; color: #64748b; padding: 2rem;">No gestures recognized yet</div>';
                }
            } catch (error) {
                console.error('Error clearing history:', error);
            }
        }

        // Check server health on page load
        window.addEventListener('load', async () => {
            try {
                const response = await fetch('/health');
                const data = await response.json();
                console.log('🚀 Sign Language Translator Ready!', data);
            } catch (error) {
                console.error('Server not responding:', error);
            }
        });
    </script>
</body>
</html>
'''

#==============================================================================
# MAIN APPLICATION
#==============================================================================

if __name__ == '__main__':
    try:
        print("🚀 " + "="*60)
        print("🤟 SIGN LANGUAGE TRANSLATOR - Complete Web Application")
        print("🚀 " + "="*60)
        print("📋 Features:")
        print("   ✅ Real-time ASL alphabet recognition")
        print("   ✅ Web-based interface (no installation needed)")
        print("   ✅ Mobile and desktop compatible")
        print("   ✅ Perfect for NGOs and accessibility use")
        print("🚀 " + "="*60)
        print("🌐 Access your application at:")
        print("   📱 Local:   http://localhost:5000")
        print("   🌍 Network: http://0.0.0.0:5000")
        print("🚀 " + "="*60)
        print("🎯 Ready for NGO demonstrations and accessibility assistance!")
        print("")
        
        # Use regular Flask development server for better compatibility
        app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
        
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        import traceback
        traceback.print_exc()