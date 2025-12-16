import numpy as np
import librosa
import whisper
import tensorflow_hub as hub
import tensorflow as tf
import pandas as pd
from .config import *

# --- THỦ THUẬT FFMPEG (Giữ nguyên) ---
import os
import imageio_ffmpeg
os.environ["PATH"] += os.pathsep + os.path.dirname(imageio_ffmpeg.get_ffmpeg_exe())

# --- LOAD MODELS ---
_whisper_model = None
_yamnet_model = None
_yamnet_classes = None

def load_whisper_model():
    global _whisper_model
    if _whisper_model is None:
        print("⏳ Loading Whisper...")
        _whisper_model = whisper.load_model(WHISPER_MODEL_SIZE)
    return _whisper_model

def load_yamnet_model():
    global _yamnet_model, _yamnet_classes
    if _yamnet_model is None:
        print("⏳ Loading YAMNet...")
        # Tắt log warning
        tf.get_logger().setLevel('ERROR')
        _yamnet_model = hub.load('https://tfhub.dev/google/yamnet/1')
        class_path = _yamnet_model.class_map_path().numpy().decode('utf-8')
        _yamnet_classes = pd.read_csv(class_path)['display_name'].tolist()
    return _yamnet_model, _yamnet_classes

# --- LOGIC WHISPER ---
def run_whisper(audio_path):
    model = load_whisper_model()
    result = model.transcribe(audio_path)
    segments = []
    for s in result['segments']:
        segments.append({
            'start': s['start'] + SPEECH_OFFSET,
            'end': s['end'] + SPEECH_OFFSET,
            'text': s['text'].strip(),
            'type': 'speech'
        })
    return segments

# --- LOGIC YAMNET (Đã fix lỗi đa nhãn) ---
def run_yamnet(audio_path):
    print("\n🔍 [YAMNET ANALYSIS] Scanning audio events...")
    model, classes = load_yamnet_model()
    
    try:
        wav_data, sr = librosa.load(audio_path, sr=YAMNET_SR, mono=True)
    except Exception as e:
        return []

    scores, embeddings, spectrogram = model(wav_data)
    scores_np = scores.numpy()
    
    events = []
    step_sec = 0.48
    target_indices = {name: i for i, name in enumerate(classes) if name in TARGET_EVENTS}
    
    for i, frame_scores in enumerate(scores_np):
        time_start = i * step_sec
        time_end = time_start + step_sec
        
        detected_in_frame = []
        for label, idx in target_indices.items():
            score = frame_scores[idx]
            if score >= CONFIDENCE_THRESHOLD:
                detected_in_frame.append((label, score))
        
        detected_in_frame.sort(key=lambda x: x[1], reverse=True)
        
        if detected_in_frame:
            top_label, top_score = detected_in_frame[0]
            text = f"[{top_label}]"
            
            if events and events[-1]['text'] == text and (time_start - events[-1]['end'] < 0.5):
                events[-1]['end'] = time_end
            else:
                events.append({'start': time_start, 'end': time_end, 'text': text, 'type': 'sound'})

    final_events = [e for e in events if (e['end'] - e['start']) >= MIN_EVENT_DURATION]
    print(f"✅ Found {len(final_events)} sound events.")
    return final_events

def merge_subtitles(speech_subs, sound_subs):
    return sorted(speech_subs + sound_subs, key=lambda x: x['start'])