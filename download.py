from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import yt_dlp

app = Flask(__name__)
CORS(app)

# Caminho para o ffmpeg
FFMPEG_PATH = 'C:\\ProgramData\\chocolatey\\lib\\ffmpeg\\tools\\ffmpeg\\bin\\ffmpeg.exe'

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    youtube_url = data.get('url')
    output_dir = data.get('outputDir')  # Define 'downloads' como diretório padrão

    if not youtube_url:
        return jsonify({"status": "error", "message": "URL não fornecida."}), 400
    if not output_dir:
        return jsonify({"status": "error", "message": "Diretório de saída não fornecido."}), 400
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'ffmpeg_location': FFMPEG_PATH,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
        return jsonify({"status": "completed"})
    except yt_dlp.utils.DownloadError as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
