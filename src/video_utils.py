from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import os

def format_time(seconds):
    """Chuyển giây sang định dạng SRT (00:00:00,000)"""
    ms = int((seconds - int(seconds)) * 1000)
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

def create_srt_file(subtitles, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        for i, sub in enumerate(subtitles):
            start = format_time(sub['start'])
            end = format_time(max(sub['start'] + 0.5, sub['end']))
            text = sub['text']
            f.write(f"{i+1}\n{start} --> {end}\n{text}\n\n")
    print(f"📄 Đã tạo file SRT: {output_path}")

def overlay_subtitles(video_path, subtitles, output_path):
    print(f"🎬 Đang render video: {output_path}...")
    try:
        video = VideoFileClip(video_path)
        clips = [video]
        W, H = video.size
        
        for sub in subtitles:
            start = sub['start']
            duration = max(0.5, sub['end'] - sub['start'])
            text = sub['text']
            
            # Style
            is_sound = text.startswith('[')
            fontsize = 28 if not is_sound else 24
            color = 'yellow' if is_sound else 'white'
            position = ('center', 0.85) if is_sound else ('center', 0.9)
            
            # Lưu ý: Trên Windows dùng font='Arial', Linux dùng 'Liberation-Sans'
            # Để auto, ta dùng None hoặc 'Arial'
            txt_clip = TextClip(
                text, 
                fontsize=fontsize, 
                color=color, 
                font='Arial', 
                stroke_color='black', 
                stroke_width=1,
                size=(W*0.9, None), 
                method='caption'
            ).set_position(position).set_start(start).set_duration(duration)
            
            clips.append(txt_clip)
            
        final = CompositeVideoClip(clips)
        final.write_videofile(output_path, codec='libx264', audio_codec='aac', fps=24, logger=None)
        print("✅ Render hoàn tất!")
        
    except Exception as e:
        print(f"❌ Lỗi overlay video: {e}")
        print("👉 Gợi ý: Kiểm tra xem đã cài ImageMagick chưa?")