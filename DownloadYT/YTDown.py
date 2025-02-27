import os
import subprocess
import sys
from urllib.parse import urlparse, parse_qs

def check_ffmpeg():
    """Verifica se o FFmpeg está instalado e acessível."""
    try:
        subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        print("FFmpeg não está instalado ou não está no PATH.")
        return False

def get_youtube_id(url):
    """Extrai o ID do vídeo do YouTube a partir da URL."""
    parsed = urlparse(url)
    if parsed.hostname == 'www.youtube.com' and parsed.path == '/watch':
        query = parse_qs(parsed.query)
        return query.get('v', [None])[0]
    return None

def download_video(video_url, output_dir):
    """Baixa o vídeo do YouTube e extrai o áudio."""
    youtube_id = get_youtube_id(video_url)
    if youtube_id is None:
        print(f"URL inválida: {video_url}")
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    video_file = os.path.join(output_dir, f"{youtube_id}.mp4")
    audio_file = os.path.join(output_dir, f"{youtube_id}.mp3")

    # Comando para baixar o vídeo usando cookies
    cmd_download_video = [
        'yt-dlp', '--cookies', 'cookies.txt', '-o', video_file, video_url
    ]

    try:
        print(f"Baixando vídeo de: {video_url}")
        subprocess.run(cmd_download_video, check=True)
        print(f"Vídeo baixado com sucesso: {video_file}")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao baixar o vídeo: {e}")
        return

    try:
        cmd_extract_audio = [
            'ffmpeg', '-i', video_file, '-q:a', '0', '-map', 'a', audio_file
        ]
        subprocess.run(cmd_extract_audio, check=True)
        print(f"Áudio extraído com sucesso: {audio_file}")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao extrair áudio: {e}")

def main():
    # Verifica se há argumentos na linha de comando
    if len(sys.argv) < 2:
        print("Uso: python3 DownloadYT.py <URL1> <URL2> ...")
        print("Exemplo: python3 DownloadYT.py https://www.youtube.com/watch?v=Rl5o5_LFn1g")
        return

    # Pega as URLs da linha de comando
    video_urls = sys.argv[1:]
    output_dir = 'YouTubeDownloaded'

    if not check_ffmpeg():
        return

    for url in video_urls:
        download_video(url, output_dir)

if __name__ == "__main__":
    main()
