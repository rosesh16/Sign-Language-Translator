# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is a Python-based American Sign Language (ASL) alphabet recognition system using computer vision. The project uses MediaPipe for hand landmark detection and OpenCV for camera capture and image processing to recognize ASL alphabet gestures in real-time.

## Dependencies and Setup

### Web Application Setup
```bash
# Install required dependencies
pip install -r requirements.txt

# Run the web application
python app.py

# Access the application at http://localhost:5000
```

### Desktop Application (Legacy)
```bash
# Install basic dependencies
pip install mediapipe opencv-python numpy

# Run the desktop application
python Main.py

# Exit the application by pressing 'x' key
```

## Code Architecture

### Web Application Components (Primary)

**app.py** - Flask web server with real-time gesture recognition
- Flask backend with SocketIO for real-time communication
- VideoCamera class handles MediaPipe processing and frame capture
- RESTful API endpoints for camera control and data retrieval
- WebSocket events for live gesture updates to frontend
- Base64 encoded video streaming for web display

**templates/index.html** - Responsive web interface
- Real-time video feed display with camera controls
- Live caption system with gesture-to-text conversion
- Accessibility panel with text size, contrast, and timestamp options
- Mobile-responsive design with touch-friendly controls
- Recognition history with auto-scroll functionality

**static/style.css** - Comprehensive styling with accessibility features
- CSS custom properties for consistent theming
- High contrast mode for visual accessibility
- Responsive grid layout for desktop and mobile
- Smooth animations and transitions

**static/script.js** - Frontend logic and real-time communication
- WebSocket connection management with SocketIO
- Event Source for video streaming
- Accessibility settings persistence in localStorage
- Keyboard shortcuts for power users
- Real-time gesture recognition and caption building

### Desktop Application Components (Legacy)

**Main.py** - Main application loop and camera interface
- Sets up MediaPipe hands detection with single hand configuration
- Captures video frames from default camera (index 0)
- Processes frames through the recognition pipeline
- Handles visual pointer effects for specific gestures (D, I, J)
- Displays results with horizontal flip for mirror effect

**Function.py** - Recognition engine with two main functions:

1. **persons_input()** - Core gesture recognition logic
   - Uses hand landmark coordinates to determine finger positions (up/down states)
   - Calculates distances between hand landmarks to identify gestures
   - Supports recognition of ASL letters: A-Z (excluding some complex gestures)
   - Uses boolean flags for finger states: thumbs_up, index_up, middel_up, ring_up, littel_up
   - Determines hand orientation (horizontal/vertical) for gesture context

2. **get_fram()** - Visual overlay and bounding box rendering
   - Calculates bounding rectangle around detected hand
   - Renders recognition results as text overlay
   - Handles coordinate transformations for mirrored display

### Hand Landmark System

The recognition system uses MediaPipe's 21-point hand landmark model:
- Landmark indices 0-20 represent specific points on the hand
- Distance calculations between landmarks determine finger positions
- Critical landmarks: 0 (wrist), 4 (thumb tip), 8 (index tip), 12 (middle tip), 16 (ring tip), 20 (pinky tip)
- Reference image: `HAND_CORD.png` shows landmark positions

### Recognition Logic Flow

1. **Frame Capture** - OpenCV captures camera frame
2. **Hand Detection** - MediaPipe processes frame for hand landmarks
3. **Coordinate Extraction** - 21 landmark coordinates extracted and normalized
4. **Gesture Classification** - Distance-based algorithm determines finger states
5. **Letter Recognition** - Combination of finger states maps to specific ASL letters
6. **Visual Feedback** - Bounding box and letter overlay rendered on frame

### Special Features

- **Pointer Trail Effect** - Letters D, I, J leave visual trails using fingertip coordinates
- **Mirror Display** - Horizontal flip provides natural selfie-view experience
- **Real-time Processing** - Optimized for live camera input with performance flags

## Development Notes

### Web Application Development

#### API Endpoints
- `GET /` - Main application interface
- `GET /start_camera` - Initialize camera and begin recognition
- `GET /stop_camera` - Stop camera and end recognition session
- `GET /video_feed` - Server-Sent Events stream for video frames
- `GET /get_current_gesture` - Current gesture and timestamp
- `GET /get_gesture_history` - Full recognition history
- `GET /clear_history` - Clear stored gesture history

#### WebSocket Events
- `connect` - Client connection established
- `disconnect` - Client disconnection
- `new_gesture` - Real-time gesture recognition updates
- `connection_response` - Server connection confirmation

#### Frontend Features
- Real-time video streaming via Server-Sent Events
- WebSocket communication for instant gesture updates
- Accessibility features: text sizing, high contrast, timestamps
- Responsive design for mobile and desktop
- Gesture history with auto-scroll and manual clearing
- Live caption building with gesture hold-time logic
- Keyboard shortcuts (Ctrl+Space: toggle camera, Ctrl+Del: clear caption)

### Testing Recognition
- Ensure good lighting conditions for accurate hand detection
- Position hand clearly within camera view
- Refer to `alphabet-numbers-American-Sign-Language.webp` for correct ASL gestures
- Test individual letters by forming gestures and observing recognition output
- Use browser developer tools to monitor WebSocket connections and API calls

### Modifying Recognition
- Adjust distance thresholds in `persons_input()` for improved accuracy
- Add new gesture patterns by extending the conditional logic
- Modify gesture hold time in `script.js` (gestureHoldTime variable)
- Customize video processing parameters in `app.py` VideoCamera class

### Deployment Considerations
- Configure Flask for production with WSGI server (Gunicorn, uWSGI)
- Set up HTTPS for camera access in modern browsers
- Consider WebRTC for more efficient video streaming
- Implement rate limiting and session management for production use
- Optimize MediaPipe processing for server deployment
