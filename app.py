from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

# Variabel untuk menyimpan proses streaming
stream_process = None

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/start_stream', methods=['POST'])
def start_stream():
    global stream_process
    if stream_process is not None:
        return "Streaming sudah berjalan!", 400

    data = request.get_json()
    video_file = data['video']
    
    # Ganti dengan path video Anda di Google Drive
    video_path = f'/content/drive/My Drive/{video_file}'
    
    # Ganti dengan kunci streaming YouTube Anda
    stream_key = 'YOUR_STREAM_KEY'
    
    # Jalankan FFMPEG untuk streaming
    stream_process = subprocess.Popen(['ffmpeg', '-re', '-i', video_path, '-c:v', 'libx264', '-preset', 'veryfast', '-maxrate', '3000k', '-bufsize', '6000k', '-c:a', 'aac', '-b:a', '128k', '-f', 'flv', f'rtmp://a.rtmp.youtube.com/live2/{stream_key}'])
    
    return "Streaming dimulai!", 200

@app.route('/stop_stream', methods=['POST'])
def stop_stream():
    global stream_process
    if stream_process is not None:
        stream_process.terminate()
        stream_process = None
        return "Streaming dihentikan!", 200
    return "Tidak ada streaming yang berjalan!", 400

if __name__ == '__main__':
    app.run(debug=True)