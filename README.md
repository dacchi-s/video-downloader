# YouTube Video/Audio Downloader

A powerful command-line tool for downloading high-quality videos and audio from YouTube. This downloader features a simple interface, batch download capabilities, and flexible format options to meet various use cases.

## Key Features

- **High-Quality Downloads**: Support for video resolutions up to 1080p
- **Audio Extraction**: Download audio-only in multiple formats (MP3, M4A, WAV, etc.)
- **Batch Processing**: Download multiple videos from a CSV file at once
- **Time-Based Clipping**: Extract specific segments of videos using start and end times
- **Progress Tracking**: Real-time download progress visualization with progress bars
- **Robust Error Handling**: Automatic retry mechanism ensures reliable downloads

## System Requirements

- Python 3.7 or higher
- FFmpeg (required for audio conversion)
- Stable internet connection

## Installation

### Method 1: Using Conda (Recommended)

#### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/youtube-downloader.git
cd youtube-downloader
```

#### 2. Create Conda Environment

```bash
conda env create -f environment.yml
conda activate video_downloader
```

#### 3. Install FFmpeg

```bash
conda install -c conda-forge ffmpeg
```

### Method 2: Using pip

#### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/youtube-downloader.git
cd youtube-downloader
```

#### 2. Install Required Packages

```bash
pip install -r requirements.txt
```

#### 3. Install FFmpeg

FFmpeg is essential for audio conversion and video processing.

**If using Conda** (already installed in step 2):
```bash
# FFmpeg is included in the environment.yml
```

**If using pip or system-wide installation**:

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install ffmpeg
```

#### macOS
```bash
brew install ffmpeg
```

#### Windows
Download FFmpeg from the [official website](https://ffmpeg.org/download.html) and add it to your system PATH.

### 4. Verify Installation

```bash
python youtube_downloader.py --help
```

If the help message appears, you're ready to start downloading!

## Usage

### Basic Usage

#### Download a Video (Default: 1080p, MP4 format)

```bash
python youtube_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

#### Download with Specific Quality

```bash
python youtube_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID" -q 720
```

#### Download Audio Only (MP3 format)

```bash
python youtube_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID" --audio-only -f mp3
```

#### Download High-Quality Audio

```bash
python youtube_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID" --audio-only -f mp3 --audio-quality 320
```

#### Specify Output Directory

```bash
python youtube_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID" -o ./downloads
```

### Advanced Usage

#### Download a Video Segment

```bash
python youtube_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID" --start-time 00:01:30 --end-time 00:05:45
```

#### Batch Download from CSV File

1. Create a CSV file (e.g., `urls.csv`):
```csv
https://www.youtube.com/watch?v=VIDEO_ID1
https://www.youtube.com/watch?v=VIDEO_ID2
https://www.youtube.com/watch?v=VIDEO_ID3
```

2. Execute batch download:
```bash
python youtube_downloader.py --file urls.csv -o ./downloads
```

#### Download in Various Formats

```bash
# Download video in WebM format
python youtube_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID" -f webm

# Download audio in M4A format
python youtube_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID" --audio-only -f m4a
```

## Command-Line Options

### Basic Syntax

```
usage: youtube_downloader.py [-h] [-q {1080,720,480,360}] [-f FORMAT] 
                              [-o OUTPUT] [--audio-only] 
                              [--audio-quality AUDIO_QUALITY]
                              [--start-time START_TIME] [--end-time END_TIME]
                              [--file FILE] [url]
```

### Positional Arguments

- `url`: YouTube video URL (not required when using --file option)

### Optional Arguments

#### `-q, --quality {1080,720,480,360}`
Maximum video quality (height in pixels)
- Default: 1080
- Available options: 1080, 720, 480, 360
- Downloads the highest quality not exceeding this value
- Ignored when --audio-only is used

#### `-f, --format FORMAT`
Desired media format
- Default: mp4
- Video formats: mp4, webm, mkv
- Audio formats (with --audio-only): mp3, m4a, wav, etc.

#### `-o, --output OUTPUT`
Output directory path
- Default: Current directory (.)
- Automatically created if it doesn't exist

#### `--audio-only`
Extract audio only
- When this flag is set, only audio is downloaded and extracted

#### `--audio-quality AUDIO_QUALITY`
Audio bitrate in kbps
- Default: 192
- Common values: 128, 192, 256, 320
- Only applicable when --audio-only is used

#### `--start-time START_TIME`
Video start time
- Format: HH:MM:SS
- Example: 00:01:30 (starts from 1 minute 30 seconds)

#### `--end-time END_TIME`
Video end time
- Format: HH:MM:SS
- Example: 00:05:45 (ends at 5 minutes 45 seconds)

#### `--file FILE`
Path to CSV file containing YouTube URLs
- URLs should be in the first column of each row
- Used for batch downloads

## Practical Examples

### Example 1: Download Standard Quality Video

```bash
python youtube_downloader.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -q 720 -o ./my_videos
```

### Example 2: Extract Audio from Playlist

1. Create `playlist.csv`:
```csv
https://www.youtube.com/watch?v=VIDEO_ID1
https://www.youtube.com/watch?v=VIDEO_ID2
https://www.youtube.com/watch?v=VIDEO_ID3
```

2. Execute:
```bash
python youtube_downloader.py --file playlist.csv --audio-only -f mp3 --audio-quality 320 -o ./music
```

### Example 3: Download Lecture Segment

```bash
python youtube_downloader.py "https://www.youtube.com/watch?v=LECTURE_ID" \
    --start-time 00:10:00 \
    --end-time 00:30:00 \
    -q 480 \
    -o ./lectures
```

### Example 4: Quick Low-Quality Download

```bash
python youtube_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID" -q 360 -o ./quick_downloads
```

## Output File Format

Downloaded files are saved using the following naming convention:

```
{output_directory}/{video_title}.{extension}
```

Examples:
```
./downloads/Amazing Video Title.mp4
./music/Great Song.mp3
```
