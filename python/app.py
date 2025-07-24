from flask import Flask, Response, render_template_string
from ultralytics import YOLO
import cv2

# Load YOLOv8 model
model = YOLO("trash_mbari_09072023_640imgsz_50epochs_yolov8.pt")

# Open webcam (or replace 0 with 'video.mp4' or a stream URL)
cap = cv2.VideoCapture(0)

app = Flask(__name__)

# HTML Template
html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Trash Detection System</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
            background: rgba(255, 255, 255, 0.95);
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
        }
        
        .header h1 {
            color: #2c3e50;
            font-size: 2.5rem;
            margin-bottom: 10px;
            font-weight: 700;
        }
        
        .header p {
            color: #7f8c8d;
            font-size: 1.1rem;
            line-height: 1.6;
        }
        
        .main-content {
            display: grid;
            grid-template-columns: 1fr 350px;
            gap: 30px;
            align-items: start;
        }
        
        .video-container {
            background: rgba(255, 255, 255, 0.95);
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
        }
        
        .video-feed {
            width: 100%;
            border-radius: 10px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        }
        
        .info-panel {
            background: rgba(255, 255, 255, 0.95);
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
            height: fit-content;
        }
        
        .info-section {
            margin-bottom: 25px;
        }
        
        .info-section h3 {
            color: #2c3e50;
            font-size: 1.3rem;
            margin-bottom: 15px;
            border-bottom: 2px solid #3498db;
            padding-bottom: 8px;
        }
        
        .info-section p {
            color: #555;
            line-height: 1.6;
            margin-bottom: 10px;
        }
        
        .feature-list {
            list-style: none;
            padding: 0;
        }
        
        .feature-list li {
            padding: 8px 0;
            color: #555;
            position: relative;
            padding-left: 25px;
        }
        
        .feature-list li:before {
            content: "✓";
            color: #27ae60;
            font-weight: bold;
            position: absolute;
            left: 0;
        }
        
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            background-color: #27ae60;
            border-radius: 50%;
            margin-right: 8px;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
        
        .tech-stack {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            padding: 15px;
            border-radius: 10px;
            margin-top: 15px;
        }
        
        .tech-stack h4 {
            margin-bottom: 10px;
            font-size: 1.1rem;
        }
        
        .tech-stack ul {
            list-style: none;
            padding: 0;
        }
        
        .tech-stack li {
            padding: 3px 0;
            font-size: 0.9rem;
        }
        
        @media (max-width: 768px) {
            .main-content {
                grid-template-columns: 1fr;
            }
            
            .header h1 {
                font-size: 2rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AI Trash Detection System</h1>
            <p>Real-time marine debris detection using YOLOv8 deep learning model</p>
        </div>
        
        <div class="main-content">
            <div class="video-container">
                <img src="{{ url_for('video_feed') }}" class="video-feed" alt="Live trash detection feed">
            </div>
            
            <div class="info-panel">
                <div class="info-section">
                    <h3>📊 System Status</h3>
                    <p><span class="status-indicator"></span>Live Detection Active</p>
                    <p>Model: YOLOv8 (trash_mbari_09072023)</p>
                    <p>Resolution: 640px optimized</p>
                    <p>Training: 50 epochs on marine dataset</p>
                </div>
                
                <div class="info-section">
                    <h3>🎯 Detection Capabilities</h3>
                    <ul class="feature-list">
                        <li>Real-time object detection</li>
                        <li>Marine debris identification</li>
                        <li>Multiple object tracking</li>
                        <li>Confidence scoring</li>
                        <li>Bounding box visualization</li>
                        <li>Frame-by-frame analysis</li>
                    </ul>
                </div>
                
                <div class="info-section">
                    <h3>🌊 Environmental Impact</h3>
                    <p>This system helps monitor and identify marine debris in real-time, supporting ocean cleanup efforts and environmental conservation initiatives.</p>
                    <p>The AI model has been trained on diverse marine waste datasets to accurately detect various types of floating debris.</p>
                </div>
                
                <div class="tech-stack">
                    <h4>🛠️ Technology Stack</h4>
                    <ul>
                        <li>• YOLOv8 (Ultralytics)</li>
                        <li>• Flask Web Framework</li>
                        <li>• OpenCV Computer Vision</li>
                        <li>• Real-time Video Processing</li>
                        <li>• HTML5/CSS3 Interface</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

def gen_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break
        results = model(frame)[0]
        annotated = results.plot()

        ret, buffer = cv2.imencode('.jpg', annotated)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return render_template_string(html)

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    print("🚀 Starting server at http://localhost:5000")
    app.run(host='0.0.0.0', port=5000)
