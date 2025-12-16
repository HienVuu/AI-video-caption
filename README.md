# AI Video Captioning (Whisper + YAMNet)

This project is an automated video captioning tool that generates subtitles for both spoken dialogue and background environmental sounds. It leverages OpenAI's Whisper model for speech recognition and Google's YAMNet for sound event detection. The system merges these two outputs to create comprehensive subtitles and burns them directly into the video.

## Features

- Speech-to-Text: Uses OpenAI Whisper (base model) to transcribe spoken dialogue.
- Sound Event Detection: Uses Google YAMNet to detect environmental sounds like laughter, applause, vehicles, music, etc.
- Smart Filtering: Logic to prioritize sound events based on confidence thresholds.
- Automatic Overlay: Burns subtitles into the video using MoviePy and ImageMagick.
- Web Interface: Simple drag-and-drop interface built with Gradio.
- Offline execution: Runs entirely on your local machine.

## How it Works

1. The user uploads a video file (MP4).
2. The system extracts the audio track from the video.
3. Two AI models process the audio in parallel:
   - Whisper transcribes the speech.
   - YAMNet scans for sound events.
4. The system filters YAMNet results based on a confidence threshold and a target list of events.
5. Speech and sound subtitles are merged and sorted by timestamp.
6. The final subtitles are rendered onto the video using ImageMagick.

## Prerequisites

- Python 3.10 or higher
- FFmpeg (Required for audio processing)
- ImageMagick (Required for rendering text on video)

## Installation

1. Clone the repository:
   git clone https://github.com/HienVuu/AI-video-caption.git
   cd AI-video-caption

2. Create a virtual environment:
   python -m venv venv

3. Activate the virtual environment:
   - Windows: .\venv\Scripts\activate
   - Linux/Mac: source venv/bin/activate

4. Install dependencies:
   pip install -r requirements.txt

## Important: ImageMagick Configuration

This project uses MoviePy, which depends on ImageMagick to create text subtitles.

1. Download and install ImageMagick for your operating system.
2. During installation on Windows, you must check the box that says: "Install legacy utilities (e.g. convert)".
3. If the program fails with a "WinError 2" or cannot find the file, open app.py and manually update the path to your magick.exe file.

## Usage

1. Start the application:
   python app.py

2. Open your web browser and navigate to the local URL provided in the terminal.

3. Upload a video, adjust the settings if needed, and click Run.

## Configuration

You can customize the sensitivity of the AI in the src/config.py file:

- CONFIDENCE_THRESHOLD: Lower this value (e.g., to 0.1) to detect quieter background sounds.
- TARGET_EVENTS: Add or remove sound categories you want to detect (e.g., 'Dog', 'Rain', 'Siren').

## Project Structure

- app.py: Main entry point for the Gradio Web UI.
- src/inference.py: Logic for running Whisper and YAMNet.
- src/config.py: Configuration settings and target event list.
- src/video_utils.py: Functions for SRT creation and video overlay.
- data/: Directory for storing raw files (ignored by git).
- requirements.txt: Python dependencies.

