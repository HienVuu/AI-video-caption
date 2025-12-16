import os
import shutil
from src.config import DATA_RAW_DIR, OUTPUT_DIR
from src.inference import run_whisper, run_yamnet, merge_subtitles
from src.video_utils import create_srt_file, overlay_subtitles
from moviepy.editor import VideoFileClip

def main():
    print("="*50)
    print("🎬 AI VIDEO CAPTIONING - CLI MODE")
    print("="*50)

    # 1. Cấu hình tên file đầu vào (Bạn sửa tên file video của bạn ở đây)
    INPUT_FILENAME = "input_video.mp4" 
    
    input_path = os.path.join(DATA_RAW_DIR, INPUT_FILENAME)
    output_video_path = os.path.join(OUTPUT_DIR, f"captioned_{INPUT_FILENAME}")
    output_srt_path = os.path.join(OUTPUT_DIR, f"subtitles_{INPUT_FILENAME}.srt")
    temp_audio_path = "temp_main_audio.wav"

    # 2. Kiểm tra file đầu vào
    if not os.path.exists(input_path):
        print(f"❌ Lỗi: Không tìm thấy file video tại: {input_path}")
        print(f"👉 Hãy copy video vào thư mục: {DATA_RAW_DIR}")
        return

    try:
        # 3. Tách âm thanh (Bắt buộc để chạy ổn định)
        print(f"\n🎧 Đang tách âm thanh từ: {INPUT_FILENAME}...")
        with VideoFileClip(input_path) as clip:
            clip.audio.write_audiofile(temp_audio_path, codec='pcm_s16le', logger=None)

        # 4. Chạy Whisper (Lời nói)
        print("\n🤖 Đang chạy Whisper (Speech Recognition)...")
        # Lưu ý: Whisper có thể nhận thẳng video, nhưng dùng audio wav sẽ nhanh và chuẩn hơn
        speech_subs = run_whisper(temp_audio_path)
        print(f"   -> Tìm thấy {len(speech_subs)} đoạn thoại.")

        # 5. Chạy YAMNet (Âm thanh môi trường)
        print("\n🔊 Đang chạy YAMNet (Sound Event Detection)...")
        sound_subs = run_yamnet(temp_audio_path)
        print(f"   -> Tìm thấy {len(sound_subs)} sự kiện âm thanh.")

        # 6. Gộp kết quả
        print("\n🔄 Đang tổng hợp phụ đề...")
        all_subs = merge_subtitles(speech_subs, sound_subs)

        # 7. Xuất file SRT
        create_srt_file(all_subs, output_srt_path)

        # 8. Xuất Video (Overlay)
        overlay_subtitles(input_path, all_subs, output_video_path)

        print("\n" + "="*50)
        print("✅ XỬ LÝ HOÀN TẤT!")
        print(f"📂 Video kết quả: {output_video_path}")
        print(f"📄 File phụ đề:   {output_srt_path}")
        print("="*50)

    except Exception as e:
        print(f"\n❌ Có lỗi xảy ra: {e}")
    
    finally:
        # Dọn dẹp file rác
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)
            print("🧹 Đã dọn dẹp file tạm.")

if __name__ == "__main__":
    main()