import os
import sys
import shutil
from moviepy.config import change_settings # Import hàm cấu hình

# ==============================================================================
# 🔧 CẤU HÌNH MÔI TRƯỜNG (CHỈ ĐỊNH THỦ CÔNG)
# ==============================================================================
print("🔧 Đang cấu hình môi trường...")

# 1. CẤU HÌNH IMAGEMAGICK (QUAN TRỌNG NHẤT)
# 👇👇👇 DÁN ĐƯỜNG DẪN BẠN VỪA TÌM ĐƯỢC VÀO GIỮA HAI DẤU NHÁY DƯỚI ĐÂY 👇👇👇
magick_path = r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe" 


if os.path.exists(magick_path):
    # Ép MoviePy dùng đường dẫn này
    change_settings({"IMAGEMAGICK_BINARY": magick_path})
    print(f"✅ Đã trỏ ImageMagick vào: {magick_path}")
else:
    print(f"❌ CẢNH BÁO: Đường dẫn ImageMagick sai! File không tồn tại: {magick_path}")
    # Nếu sai đường dẫn mặc định, code sẽ thử tự tìm một lần nữa (fallback)
    
# 2. CẤU HÌNH FFMPEG (Giữ nguyên)
project_dir = os.getcwd()
os.environ["PATH"] += os.pathsep + project_dir

try:
    import imageio_ffmpeg
    ffmpeg_src = imageio_ffmpeg.get_ffmpeg_exe()
    ffmpeg_dir = os.path.dirname(ffmpeg_src)
    ffmpeg_local = os.path.join(project_dir, "ffmpeg.exe")
    
    if not os.path.exists(ffmpeg_local):
        print("   👉 Đang copy ffmpeg.exe...")
        shutil.copy(ffmpeg_src, ffmpeg_local)
        
    os.environ["PATH"] += os.pathsep + ffmpeg_dir
    print(f"✅ Đã cấu hình xong: FFmpeg")

except Exception as e:
    print(f"⚠️ Cảnh báo FFmpeg: {e}")

# ==============================================================================
# LOGIC APP
# ==============================================================================
import gradio as gr
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from src.inference import run_whisper, run_yamnet, merge_subtitles
from src.video_utils import create_srt_file, overlay_subtitles
import src.config as config

def pipeline_wrapper(video_file, threshold, offset):
    if video_file is None: return None, None
    print(f"\n🚀 Nhận yêu cầu xử lý video: {video_file}")
    
    temp_dir = "temp_gradio"
    if os.path.exists(temp_dir):
        try: shutil.rmtree(temp_dir)
        except: pass
    os.makedirs(temp_dir, exist_ok=True)
    
    input_path = video_file
    audio_path = os.path.join(temp_dir, "extracted_audio.wav")
    srt_path = os.path.join(temp_dir, "subtitles.srt")
    output_video_path = os.path.join(temp_dir, "output_video_captioned.mp4")

    try:
        config.CONFIDENCE_THRESHOLD = threshold
        config.SPEECH_OFFSET = offset

        print("🎧 Đang tách âm thanh...")
        with VideoFileClip(input_path) as clip:
            clip.audio.write_audiofile(audio_path, codec='pcm_s16le', logger=None)

        print("🤖 Đang chạy Whisper...")
        speech_subs = run_whisper(audio_path)
        
        print("🔊 Đang chạy YAMNet...")
        sound_subs = run_yamnet(audio_path)
        
        all_subs = merge_subtitles(speech_subs, sound_subs)
        create_srt_file(all_subs, srt_path)
        
        print("🎬 Đang render video (Overlay)...")
        overlay_subtitles(input_path, all_subs, output_video_path)

        if os.path.exists(output_video_path):
            print("✅ Xử lý hoàn tất!")
            return output_video_path, srt_path
        else:
            print("❌ Lỗi: File video không được tạo ra.")
            return None, srt_path

    except Exception as e:
        print(f"❌ LỖI: {str(e)}")
        import traceback
        traceback.print_exc()
        return None, None

with gr.Blocks(title="AI Video Captioning Pro", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🎬 AI Video Captioning (Force Config)")
    with gr.Row():
        with gr.Column():
            video_input = gr.Video(label="Input")
            btn = gr.Button("RUN", variant="primary")
        with gr.Column():
            video_output = gr.Video(label="Output")
            file_output = gr.File(label="SRT")
    btn.click(pipeline_wrapper, [video_input, gr.Number(0.15), gr.Number(0.2)], [video_output, file_output])

if __name__ == "__main__":
    demo.queue().launch(share=False)