import os
import re
import requests
import subprocess


def ensure_downloads_folder(course_name: str) -> str:
    downloads_path = os.path.join(os.getcwd(), "courses", course_name)
    os.makedirs(downloads_path, exist_ok=True)
    return downloads_path


def download_video(video_url: str, downloads_path: str, output_file: str):
    print(f"Downloading video from {video_url}...")
    # Use ffmpeg to download the video
    output_file = os.path.join(
        os.getcwd(), downloads_path, output_file + ".mp4"
    )
    try:
        subprocess.run(
            [
                "ffmpeg",
                "-loglevel",
                "quiet",
                "-i",
                video_url,
                "-c",
                "copy",
                output_file,
            ],
            check=True,
        )
        print(f"Video downloaded successfully: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error downloading video: {e}")

    return output_file


def download_subtitles(
    playlist_url: str, downloads_path: str, output_file: str
):
    print(f"Fetching subtitles from {playlist_url}...")

    # Get the playlist content
    response = requests.get(playlist_url)
    response.raise_for_status()
    playlist_content = response.text

    # Extract subtitle URLs until the first occurrence of ".vtt"
    subtitle_urls = re.findall(r"(https?://[^\s]+?\.vtt)", playlist_content)
    if not subtitle_urls:
        print("No subtitle URLs found in the playlist.")
        return

    combined_subtitles_path = os.path.join(
        downloads_path, f"{output_file}_subtitles.srt"
    )

    # Download and combine subtitles
    subtitle_files: list[str] = []
    for i, subtitle_url in enumerate(subtitle_urls):
        print(
            f"Downloading subtitle {i + 1}/{len(subtitle_urls)}: {subtitle_url}"
        )

        subtitle_file = os.path.join(downloads_path, f"subtitle_{i}.vtt")
        try:
            # Use ffmpeg to download and convert VTT to SRT
            subprocess.run(
                [
                    "ffmpeg",
                    "-loglevel",
                    "quiet",
                    "-i",
                    subtitle_url,
                    "-map",
                    "0:s",
                    "-c:s",
                    "copy",
                    subtitle_file,
                ],
                check=True,
            )
            subtitle_files.append(subtitle_file)
        except subprocess.CalledProcessError as e:
            print(f"Error downloading subtitle {i + 1}: {e}")

    # Combine subtitles into a single file
    with open(combined_subtitles_path, "w", encoding="utf-8") as combined_file:
        for subtitle_file in subtitle_files:
            with open(subtitle_file, "r", encoding="utf-8") as file:
                combined_file.write(file.read())
                combined_file.write("\n")
            # Delete the individual subtitle file
            os.remove(subtitle_file)

    print(f"Combined subtitles saved to: {combined_subtitles_path}")
    return combined_subtitles_path


def download_course_video(course_name: str):
    # Video URL (replace with actual URL)
    video_name = input("Enter the video name: ")
    video_url = input("Enter the video URL (m3u8): ")

    downloads_path = ensure_downloads_folder(course_name)
    # Download the video
    download_video(video_url, downloads_path, video_name)

    # Subtitle playlist URL (replace with actual URL)
    if input("Do you want to download subtitles? (y/n): ") != "y":
        return
    # Subtitle playlist URL (replace with actual URL)
    subtitle_playlist_url = input("Enter the subtitles playlist URL: ")
    # Download and combine subtitles
    download_subtitles(subtitle_playlist_url, downloads_path, video_name)


def main():
    # Course name (for folder and video file names)
    course_name = input("Enter the course name: ")

    # Execute in loop for multiple videos
    while True:
        download_course_video(course_name)
        if input("Do you want to download another video? (y/n): ") != "y":
            break


if __name__ == "__main__":
    main()
