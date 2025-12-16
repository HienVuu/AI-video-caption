import os
import requests
import zipfile
import io
import shutil

def download_and_extract(url, target_file):
    print(f"⬇ Đang tải: {target_file}...")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with zipfile.ZipFile(io.BytesIO(response.content)) as z:
                
                for filename in z.namelist():
                    if filename.endswith(target_file):
                        with z.open(filename) as source, open(target_file, "wb") as target:
                            shutil.copyfileobj(source, target)
                        print(f"✅ Đã cài đặt thành công: {target_file}")
                        return
        else:
            print(f"❌ Lỗi tải file (Status code: {response.status_code})")
    except Exception as e:
        print(f"❌ Lỗi: {e}")

def main():
    print("="*40)
    print("🛠️  AUTO SETUP FFMPEG & FFPROBE")
    print("="*40)

    
    ffprobe_url = "https://github.com/ffbinaries/ffbinaries-prebuilt/releases/download/v6.1/ffprobe-6.1-win-64.zip"
    ffmpeg_url = "https://github.com/ffbinaries/ffbinaries-prebuilt/releases/download/v6.1/ffmpeg-6.1-win-64.zip"

    
    if not os.path.exists("ffprobe.exe"):
        download_and_extract(ffprobe_url, "ffprobe.exe")
    else:
        print("✅ ffprobe.exe đã có sẵn.")

    if not os.path.exists("ffmpeg.exe"):
        download_and_extract(ffmpeg_url, "ffmpeg.exe")
    else:
        print("✅ ffmpeg.exe đã có sẵn.")

    print("\n Cài đặt hoàn tất!")

if __name__ == "__main__":
    main()