import os

# --- ĐƯỜNG DẪN DỰ ÁN ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_RAW_DIR = os.path.join(BASE_DIR, 'data', 'raw')
MODELS_DIR = os.path.join(BASE_DIR, 'models', 'saved')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- THAM SỐ VIDEO & AUDIO ---
SAMPLE_RATE = 44100 
YAMNET_SR = 16000   
HOP_LENGTH = 347    
N_MELS = 128
TIME_STEPS = 432    

# --- THAM SỐ AI ---
WHISPER_MODEL_SIZE = "base"
SPEECH_OFFSET = 0.2

# ⚠️ HẠ THRESHOLD XUỐNG THẤP ĐỂ BẮT NHẠY HƠN
CONFIDENCE_THRESHOLD = 0.05  # Để 0.05 hoặc 0.1
MIN_EVENT_DURATION = 0.1     # Sự kiện ngắn cũng lấy

# --- DANH SÁCH MỤC TIÊU (MỞ RỘNG) ---
TARGET_EVENTS = [
    # Tiếng cười (Quan trọng nhất)
    'Laughter', 'Giggle', 'Snicker', 'Chuckle', 'Belly laugh', 'Baby laughter', 'Chatter',
    
    # Cảm xúc con người
    'Clap', 'Clapping', 'Applause', 'Cheering', 'Crowd', 'Screaming', 'Crying, sobbing',
    'Whistling', 'Breathing', 'Gasp', 'Cough',
    
    # Động vật & Thiên nhiên
    'Bird', 'Bird vocalization, bird call, bird song', 'Animal', 'Dog', 'Bark', 'Cat', 'Meow',
    'Rain', 'Thunder', 'Wind', 'Water', 
    
    # Âm nhạc
    'Music', 'Musical instrument', 'Plucked string instrument', 'Guitar', 'Piano',
    
    # Tác động
    'Knock', 'Door', 'Glass', 'Breaking', 'Crash', 'Impact',
    
    # Xe cộ
    'Vehicle', 'Car', 'Siren', 'Horn', 'Traffic noise'
]

# (Phần Custom Model giữ nguyên nếu không dùng)
CUSTOM_MODEL_PATHS = [os.path.join(MODELS_DIR, f'best_esc50_cnn_model_fold_{i}.keras') for i in range(1, 6)]