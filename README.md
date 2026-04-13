🎯 AI Real-Time Proctoring System

An AI-powered proctoring system that monitors candidates during online exams using computer vision. It detects suspicious activities like mobile phone usage, multiple persons, face absence, and looking away in real time, and assigns a risk score to maintain exam integrity.

📌 Overview

This project uses YOLOv8 for object detection and MediaPipe for face tracking to continuously monitor a candidate through a webcam. If any violation is detected repeatedly, the system generates alerts and can automatically terminate the session.

🚀 Features
✅ Real-time webcam monitoring
📱 Detects mobile phone usage
👥 Detects multiple persons in frame
👤 Tracks face visibility
👀 Detects looking away behavior
⚠️ Live alerts with timestamps
📊 Risk score calculation system
❌ Auto termination on high risk or repeated violations

🛠️ Tech Stack
Python
OpenCV
YOLOv8 (Ultralytics)
MediaPipe

📂 File Structure
.
├── RealTimeViolationAlert.py   # Main application script
└── README.md     

# Project documentation
⚙️ Installation
Clone the repository
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

Install required libraries
pip install opencv-python ultralytics mediapipe

▶️ How to Run
python RealTimeViolationAlert.py
Press q to stop the program.

⚡ How It Works
YOLOv8 Model
Detects:
Person
Mobile Phone
MediaPipe Face Mesh
Detects face presence
Tracks eye position to identify "looking away"
System Logic
Counts number of persons
Detects phone usage
Checks if face is visible
Monitors head/eye movement
Each violation increases a risk score
System triggers alerts or terminates based on thresholds

🚨 Violation Rules
Violation	Result
Phone detected 3 times	❌ Terminate session
Multiple persons 3 times	❌ Terminate session
Face not visible	⚠️ Increase risk score
Looking away	⚠️ Increase risk score
Risk score ≥ 120	❌ Terminate session

📸 Output
Live video feed with:
Bounding boxes for detected objects
Risk score display
Violation counters
Console logs:
Alerts with timestamps
Violation messages

🔮 Future Improvements
🎤 Audio-based cheating detection
🌐 Web dashboard integration
☁️ Cloud-based logging system
🎯 Improved gaze tracking
👨‍💻 Author

Jeevan Gouda

📜 License

This project is licensed under the MIT License.
