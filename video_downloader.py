import argparse
import os
import yt_dlp
import csv
from tqdm import tqdm

class DownloadProgress:
    def __init__(self):
        self.pbar = None

    def download_hook(self, d):
        if d['status'] == 'downloading':
            if self.pbar is None:
                total = d.get('total_bytes') or d.get('total_bytes_estimate')
                self.pbar = tqdm(total=total, unit='B', unit_scale=True, desc=d['filename'])
            downloaded = d.get('downloaded_bytes', 0)
            self.pbar.update(downloaded - self.pbar.n)
        elif d['status'] == 'finished':
            if self.pbar is not None:
                self.pbar.close()
            print(f"Download completed. Converting...")

def download_media(url, quality, format, audio_only, audio_quality, output_dir, start_time, end_time):
    progress = DownloadProgress()
    if audio_only:
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': format,
                'preferredquality': str(audio_quality),
            }],
            'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
            'progress_hooks': [progress.download_hook],
        }
    else:
        ydl_opts = {
            'format': f'{format}[height<={quality}]' if quality else f'{format}/bestvideo+bestaudio/best',
            'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
            'progress_hooks': [progress.download_hook],
        }

    # Add time range options if specified
    if start_time or end_time:
        ydl_opts['download_ranges'] = download_range_func(start_time, end_time)
        ydl_opts['force_generic_extractor'] = True

    # Error handling options
    ydl_opts.update({
        'ignoreerrors': True,
        'no_color': True,
        'geo_bypass': True,
        'nocheckcertificate': True,
        'extractor_args': {'youtube': {'skip': ['dash', 'hls']}},
    })

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
            print(f"Media saved in {output_dir}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            print("Trying alternative method...")
            try:
                ydl_opts['format'] = 'bestvideo+bestaudio/best'
                ydl.download([url])
                print(f"Media saved in {output_dir} using alternative method")
            except Exception as e:
                print(f"Alternative method also failed: {str(e)}")
                print("Please try updating yt-dlp or check if the video is available in your region.")

def download_range_func(start_time, end_time):
    start_seconds = time_to_seconds(start_time)
    end_seconds = time_to_seconds(end_time)

    def func(info_dict, ydl_obj):
        return [{
            'start_time': start_seconds,
            'end_time': end_seconds,
        }]
    return func

def time_to_seconds(time_str):
    if time_str:
        h, m, s = map(int, time_str.split(':'))
        return h * 3600 + m * 60 + s
    return None

def read_urls_from_csv(file_path):
    """Reads a CSV file and extracts URLs from it."""
    urls = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row:  # Check if row is not empty
                urls.append(row[0])  # Assuming URLs are in the first column
    return urls

def main():
    parser = argparse.ArgumentParser(description="YouTube Video/Audio Downloader")
    parser.add_argument("url", nargs='?', help="URL of the YouTube video (if not using --file)")
    parser.add_argument("-q", "--quality", type=int, default=1080, 
                        choices=[1080, 720, 480, 360],
                        help="Maximum video quality (height in pixels). "
                             "Choices are 1080 (default), 720, 480, or 360. "
                             "The highest available quality not exceeding "
                             "this value will be downloaded. "
                             "Ignored if --audio-only is used.")
    parser.add_argument("-f", "--format", default="mp4",
                        help="Desired media format (default: mp4). "
                             "For video: mp4, webm, mkv. "
                             "For audio (with --audio-only): mp3, m4a, wav, etc.")
    parser.add_argument("-o", "--output", default=".", 
                        help="Output directory (default: current directory)")
    parser.add_argument("--audio-only", action="store_true",
                        help="Download audio only")
    parser.add_argument("--audio-quality", type=int, default=192,
                        help="Audio bitrate in kbps (default: 192). "
                             "Common values: 128, 192, 256, 320. "
                             "Only applicable with --audio-only.")
    parser.add_argument("--start-time", type=str, 
                        help="Start time of the video (format: HH:MM:SS)")
    parser.add_argument("--end-time", type=str, 
                        help="End time of the video (format: HH:MM:SS)")
    parser.add_argument("--file", type=str, 
                        help="Path to a CSV file containing URLs of YouTube videos to download")

    args = parser.parse_args()

    if not os.path.exists(args.output):
        os.makedirs(args.output)

    if args.file:
        # If a file is specified, read URLs from the file and download each video
        urls = read_urls_from_csv(args.file)
        for url in urls:
            download_media(url, args.quality, args.format, args.audio_only, args.audio_quality, 
                           args.output, args.start_time, args.end_time)
    elif args.url:
        # If a URL is specified, download the single video
        download_media(args.url, args.quality, args.format, args.audio_only, args.audio_quality, 
                       args.output, args.start_time, args.end_time)
    else:
        print("Error: You must provide either a URL or a CSV file with the --file option.")
        parser.print_help()

if __name__ == "__main__":
    main()
