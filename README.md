📌 AI Real-Time Proctoring System

An AI-powered real-time proctoring system that monitors candidates during online assessments using computer vision. It detects suspicious activities such as mobile phone usage, multiple persons, face absence, and looking away, and assigns a dynamic risk score to ensure exam integrity.

🚀 Features
📷 Real-Time Monitoring using webcam
📱 Mobile Phone Detection (YOLOv8)
👥 Multiple Person Detection
👤 Face Detection & Tracking (MediaPipe)
👀 Looking Away Detection
⚠️ Live Alert System with timestamps
📊 Dynamic Risk Scoring System
❌ Auto Termination on repeated violations
🛠️ Technologies Used
Python
OpenCV
YOLOv8 (Ultralytics)
MediaPipe
NumPy
📂 Project Structure
RealTimeViolationAlert.py   # Main proctoring system script
⚙️ Installation
Clone the repository:
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
Install dependencies:
pip install opencv-python ultralytics mediapipe numpy
▶️ Usage

Run the script:

python RealTimeViolationAlert.py

Press 'q' to exit the system.

⚡ How It Works
YOLOv8 detects objects like persons and mobile phones.
MediaPipe Face Mesh tracks face presence and orientation.
The system:
Counts number of persons
Detects phone usage
Tracks face visibility
Monitors eye position (looking away)
Each violation increases a risk score.
If thresholds are exceeded, the system:
Triggers alerts
Terminates the session
🚨 Violation Rules
Violation	Action
Phone detected 3x	Session terminated
Multiple persons 3x	Session terminated
Face not visible	Risk score increased
Looking away	Risk score increased
Risk score ≥ 120	Session terminated
📸 Output
Live webcam feed with:
Bounding boxes (Person / Phone)
Risk score display
Violation counters
Console alerts with timestamps
🔮 Future Improvements
Audio-based cheating detection
Eye gaze tracking enhancement
Cloud logging & reporting
Web dashboard integration
👨‍💻 Author

Jeevan Gouda

📜 License

This project is open-source and available under the MIT License.
