# AI Public Speaking Confidence Analyzer

A Django-based web application that analyzes uploaded speech (audio or video), calculates speech speed, counts filler words, detects pauses, scores voice volume consistency, and evaluates overall public speaking confidence.

## Features Built
1. **Upload Speech**: Upload `.wav`, `.mp3` or `.mp4` audio/video files.
2. **Analysis Engine**: Built using `SpeechRecognition` and `librosa` for audio transcription, pace analysis, structure, and dynamics.
3. **Confidence Scoring Engine**: Combines speed, fillers, stability, and pauses into a unified index (0-100).
4. **Intuitive UI with TailwindCSS & Chart.js**: Offers a sleek "glassmorphic" interface, beautiful graphs representing confidence components, history tracking graphs, and actionable improvement feedback.
5. **Score Breaking**: Explains how various aspects (like saying "um", varying pacing) contributed to the final score.

---

## 🛠️ Requirements & Setup

You will need **Python 3.10+** (or comparable).

### 1. Environment Activation
Depending on whether you run this in **VS Code** OR **Antigravity** directly:

**In VS Code** terminal (Powershell):
```powershell
# Open terminal (Ctrl+`)
cd "d:\pragna_repose\AI_Project"
python -m venv env
.\env\Scripts\activate
```

### 2. Install Dependencies
Ensure the environment is activated, then run:

```powershell
pip install -r requirements.txt
```
*Note: We included `Django`, `librosa`, `SpeechRecognition`, `numpy`, `scipy`, `opencv-python`, `matplotlib`, and `pydub` as requested.* 
*Note 2: If macOS or Linux, the command would be `pip install -r requirements.txt` after activating `source env/bin/activate`.*

### 3. Setup Database & Migrations
The database schema for keeping your Analysis History is built-in (SQLite). Apply the migrations:
```powershell
python manage.py makemigrations
python manage.py migrate
```

### 4. Running the Web App locally

Start the Django Development Server:
```powershell
python manage.py runserver
```

Now open a web browser and go to:
**http://127.0.0.1:8000/**

### Step-by-Step test
1. Navigate to the local server URL.
2. Click **Analyze New Speech**.
3. Put a title (e.g. "Pitch Practice 1") and attach an audio/video file. 
4. Click submit, then wait for the `loading...` screen to process the analysis logic. 
5. See your Detailed Metrics, Confidence Score out of 100, and feedback suggestions.
6. Return to Home or click **View History** to see your confidence chart over time.