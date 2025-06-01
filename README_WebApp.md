# Real-Time Sign Language Translation Web Application

A web-based platform that translates American Sign Language (ASL) alphabet gestures into live text captions in real-time, enabling effective communication for hearing-impaired individuals and supporting NGOs in accessibility initiatives.

## 🌟 Features

### Real-Time Recognition
- **Live gesture detection** using MediaPipe and OpenCV
- **Instant text captions** displayed on web interface
- **Single or multiple hand** tracking support
- **Real-time video streaming** with gesture overlay

### Web-Based Interface
- **Browser-accessible** - no additional software required
- **Mobile-friendly** responsive design
- **Live webcam feed** embedded in browser
- **Cross-platform compatibility**

### Accessibility Features
- **Adjustable text size** (small, medium, large)
- **High contrast mode** for visual impairment
- **Gesture history** with timestamps
- **Auto-scroll functionality**
- **Keyboard shortcuts** for power users

### User Experience
- **Start/stop camera** controls
- **Live caption building** with gesture hold-time logic
- **Recognition history** with manual clearing
- **Connection status** indicators
- **Toast notifications** for user feedback

## 🛠️ Technology Stack

### Backend
- **Flask** - Web framework and API server
- **Flask-SocketIO** - Real-time WebSocket communication
- **OpenCV** - Video capture and image processing
- **MediaPipe** - Hand landmark detection
- **NumPy** - Mathematical operations

### Frontend
- **HTML5** - Semantic markup structure
- **CSS3** - Responsive styling with custom properties
- **JavaScript (ES6+)** - Interactive functionality
- **Socket.IO** - Real-time client communication
- **Font Awesome** - Icons and visual elements

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- Webcam/camera device
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Sign-Language
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:5000`

### First Use
1. Click "Start Camera" to begin recognition
2. Position your hand clearly in front of the camera
3. Form ASL alphabet gestures (refer to reference image)
4. Watch live captions build as you spell words
5. Use accessibility panel to customize your experience

## 📋 API Reference

### REST Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main application interface |
| `/start_camera` | GET | Initialize camera and begin recognition |
| `/stop_camera` | GET | Stop camera and end session |
| `/video_feed` | GET | Server-Sent Events video stream |
| `/get_current_gesture` | GET | Current gesture and timestamp |
| `/get_gesture_history` | GET | Complete recognition history |
| `/clear_history` | GET | Clear stored gesture history |

### WebSocket Events

| Event | Direction | Description |
|-------|-----------|-------------|
| `connect` | Client→Server | Connection established |
| `disconnect` | Client→Server | Client disconnection |
| `new_gesture` | Server→Client | Real-time gesture updates |
| `connection_response` | Server→Client | Connection confirmation |

## ⌨️ Keyboard Shortcuts

- **Ctrl/Cmd + Space** - Toggle camera on/off
- **Ctrl/Cmd + Delete** - Clear live caption
- **Ctrl/Cmd + H** - Clear recognition history

## 🎯 Usage Scenarios

### For NGOs and Accessibility Organizations
- **Educational workshops** on sign language
- **Communication assistance** in service centers
- **Awareness campaigns** for hearing impairment
- **Training tools** for staff and volunteers

### For Schools and Educational Institutions
- **ASL learning** support for students
- **Inclusive classroom** communication
- **Language therapy** assistance
- **Interactive learning** experiences

### For Individual Users
- **Personal learning** of ASL alphabet
- **Communication practice** with real-time feedback
- **Accessibility tool** for hearing-impaired individuals
- **Family communication** enhancement

## 🔧 Configuration and Customization

### Gesture Recognition Settings
Modify recognition sensitivity in `Function.py`:
```python
# Adjust distance thresholds for better accuracy
if distance(hand_coordinates[...]) < custom_threshold:
    # Recognition logic
```

### Video Processing Parameters
Customize MediaPipe settings in `app.py`:
```python
self.hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,  # Change to 2 for both hands
    min_detection_confidence=0.5,  # Adjust sensitivity
    min_tracking_confidence=0.5
)
```

### Frontend Behavior
Adjust gesture hold time in `script.js`:
```javascript
let gestureHoldTime = 1000; // Milliseconds to hold gesture
```

## 📱 Mobile Optimization

The application is fully responsive and optimized for mobile devices:
- **Touch-friendly** button sizes
- **Responsive grid** layout
- **Mobile-optimized** video container
- **Accessible** font sizes and contrast
- **Portrait and landscape** orientation support

## 🚢 Deployment

### Development Server
```bash
python app.py
# Access at http://localhost:5000
```

### Production Deployment
1. **Use a WSGI server** (Gunicorn recommended)
   ```bash
   pip install gunicorn
   gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:5000 app:app
   ```

2. **Configure HTTPS** for camera access in browsers
3. **Set up reverse proxy** (Nginx recommended)
4. **Implement rate limiting** for API endpoints
5. **Configure CORS** for cross-origin requests

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

## 🔍 Troubleshooting

### Camera Issues
- Ensure camera permissions in browser
- Check if camera is being used by other applications
- Verify camera index in `VideoCamera` class

### Performance Issues
- Reduce video resolution for better performance
- Adjust MediaPipe confidence thresholds
- Optimize frame processing rate

### Browser Compatibility
- Use HTTPS for camera access in modern browsers
- Enable WebSocket support
- Check for ad-blocker interference

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Development Setup
```bash
# Install development dependencies
pip install -r requirements.txt

# Run with debug mode
export FLASK_ENV=development
python app.py
```

## 📄 License

This project is designed for accessibility and educational purposes. Please refer to the LICENSE file for usage terms.

## 🙏 Acknowledgments

- **MediaPipe** team for hand tracking technology
- **OpenCV** community for computer vision tools
- **Flask** and **Socket.IO** for web framework
- **ASL community** for gesture reference materials

## 📞 Support

For issues, feature requests, or questions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review the API documentation
- Test with the desktop version for comparison

---

**Built with ❤️ for accessibility and inclusive communication**