import os
import subprocess
import sys
import requests
import zipfile
import shutil
import platform

try:
    import ffmpeg
except ImportError:
    print("FFmpeg-python module not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "ffmpeg-python"])
    import ffmpeg

def install_ffmpeg():
    system = platform.system().lower()
    if system == "windows":
        url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
        zip_path = "ffmpeg.zip"
        extract_path = "ffmpeg"
        try:
            print("Downloading ffmpeg...")
            response = requests.get(url)
            response.raise_for_status()
            with open(zip_path, "wb") as file:
                file.write(response.content)
        except requests.RequestException as e:
            print(f"Failed to download ffmpeg: {e}")
            return False
        try:
            print("Extracting ffmpeg...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_path)
        except zipfile.BadZipFile as e:
            print(f"Failed to extract ffmpeg: {e}")
            return False
        ffmpeg_bin = None
        for root, dirs, files in os.walk(extract_path):
            if "ffmpeg.exe" in files:
                ffmpeg_bin = root
                break
        if ffmpeg_bin:
            ffmpeg_path = os.path.join(ffmpeg_bin, "ffmpeg.exe")
            os.environ["PATH"] += os.pathsep + ffmpeg_bin
            print(f"ffmpeg installed and added to PATH: {ffmpeg_path}")
        else:
            print("Failed to install ffmpeg.")
            return False
        os.remove(zip_path)
        shutil.rmtree(extract_path)
    elif system in ["linux", "darwin"]:
        print("For Linux and macOS, please install FFmpeg using your system's package manager.")
        print("For example, on Ubuntu or Debian: sudo apt-get install ffmpeg")
        print("On macOS with Homebrew: brew install ffmpeg")
        return False
    else:
        print(f"Unsupported operating system: {system}")
        return False
    return True

def check_ffmpeg_installed():
    try:
        subprocess.run(['ffmpeg', '-version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def convert_mp3_to_m4b(input_mp3, output_m4b):
    try:
        ffmpeg.input(input_mp3).output(output_m4b, format='ipod', audio_bitrate='128k', acodec='aac').run(overwrite_output=True)
        print(f"Successfully converted {input_mp3} to {output_m4b}")
    except ffmpeg.Error as e:
        print(f"Error occurred while converting {input_mp3}: {e.stderr.decode()}")

if __name__ == "__main__":
    try:
        import requests
    except ImportError:
        print("Requests module not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
        import requests

    if not check_ffmpeg_installed():
        print("FFmpeg is not installed. Installing now...")
        if not install_ffmpeg():
            print("Failed to install FFmpeg. Please install it manually.")
            sys.exit(1)

    current_directory = os.getcwd()
    files = os.listdir(current_directory)
    mp3_files = [file for file in files if file.lower().endswith('.mp3')]

    if not mp3_files:
        print("No MP3 files found in the current directory.")
        sys.exit(1)

    for mp3_file in mp3_files:
        m4b_file = os.path.splitext(mp3_file)[0] + '.m4b'
        try:
            convert_mp3_to_m4b(mp3_file, m4b_file)
        except Exception as e:
            print(f"An error occurred while processing {mp3_file}: {str(e)}")

    print("Conversion process completed.")
