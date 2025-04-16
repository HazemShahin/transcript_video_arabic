
# #https://youtu.be/FQBdpPrLj9k?list=PLnFJTGgdQYTNJLSn8ENSzD9qaPz3LypyW
# from youtube_transcript_api import YouTubeTranscriptApi
# from youtube_transcript_api.formatters import TextFormatter
# import re

# def extract_video_id(url: str) -> str:
#     match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", url)
#     if match:
#         return match.group(1)
#     raise ValueError("Invalid YouTube URL")

# def get_youtube_transcript(url: str, language: str = "ar") -> str:
#     video_id = extract_video_id(url)
#     ytt_api = YouTubeTranscriptApi()
#     transcript_list = ytt_api.list(video_id)
#     for transcript in transcript_list:
#         if transcript.language_code == 'ar':
#             arabic_tr =transcript.fetch()
#             for snippet in arabic_tr:
#                 print(snippet.text)
# get_youtube_transcript("https://youtu.be/FQBdpPrLj9k?list=PLnFJTGgdQYTNJLSn8ENSzD9qaPz3LypyW")



import re
import os
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled
from youtube_transcript_api.formatters import TextFormatter

def extract_video_id(url: str) -> str:
    """Extracts the YouTube video ID from various URL formats."""
    # Regex patterns to find the video ID in common YouTube URL formats
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', # Standard "?v=" or "/v/" links
        r'(?:embed\/|v\/|youtu\.be\/)([0-9A-Za-z_-]{11})' # Embed, short "/v/", and youtu.be links
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    raise ValueError("Could not extract video ID from URL. Invalid or unsupported YouTube URL format.")

def get_and_save_transcript(url: str, language: str = "ar", filename: str = None):
    """
    Fetches a YouTube video transcript for a specific language,
    formats it as plain text, and saves it to a file.
    """
    try:
        # 1. Extract Video ID
        video_id = extract_video_id(url)
        print(f"Extracted Video ID: {video_id}")

        # 2. Get Transcript List and Find Specific Language
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            transcript = transcript_list.find_transcript([language])
            print(f"Found transcript: Language='{transcript.language}', Code='{transcript.language_code}'")

            # Fetch the transcript data (list of dictionaries)
            transcript_data = transcript.fetch()
            print("Transcript data fetched successfully.")

        # Handle common errors when fetching transcripts
        except NoTranscriptFound:
            print(f"Error: No transcript found for language code '{language}' for video ID '{video_id}'.")
            try:
                # List available languages for user information
                available_langs = ", ".join([t.language_code for t in transcript_list])
                print(f"Available language codes for this video: {available_langs}")
            except Exception:
                 print("Could not retrieve list of available languages.") # Handle error if listing fails too
            return # Stop execution if transcript not found
        except TranscriptsDisabled:
            print(f"Error: Transcripts are disabled for video ID '{video_id}'.")
            return # Stop execution
        except Exception as e:
            print(f"An error occurred while getting the transcript list or data: {e}")
            return # Stop execution

        # 3. Format Transcript
        formatter = TextFormatter()
        formatted_text = formatter.format_transcript(transcript_data)
        print("Transcript formatted as plain text.")

        # 4. Define Output Filename
        if filename is None:
            # Fallback filename if none is provided
            filename = f"transcript_{video_id}_{language}.txt"
            print(f"No filename provided, using default: {filename}")
        else:
             # Basic sanitization: replace characters not typically allowed in filenames
             # You might want a more robust sanitization method depending on your OS
             filename = filename.replace('/', '-').replace('\\', '-').replace(':', '-').replace('*', '-').replace('?', '-').replace('"', "'").replace('<', '-').replace('>', '-').replace('|', '-')
             print(f"Using provided filename (sanitized): {filename}")


        # 5. Save to File
        try:
            # Use 'utf-8' encoding, crucial for Arabic and many other languages
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(formatted_text)
            print(f"Transcript successfully saved to: {os.path.abspath(filename)}")
        except IOError as e:
            print(f"Error: Could not write to file '{filename}'. Reason: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while saving the file: {e}")

    except ValueError as e:
        # Handle error from extract_video_id (invalid URL)
        print(f"Input Error: {e}")
    except Exception as e:
        # Catch any other unexpected errors during the process
        print(f"An unexpected error occurred: {e}")

# --- Main Execution ---
if __name__ == "__main__":
    # The URL of the YouTube video
    # Using the canonical URL found earlier
    video_url = "http://www.youtube.com/watch?v=FQBdpPrLj9k"

    # Desired language code ('ar' for Arabic)
    lang_code = "ar"

    # Desired filename (using the title identified earlier)
    # Adding .txt extension
    output_filename = "تأسيس وعي المسلم المعاصر ج5 - م أيمن عبد الرحيم.txt"

    print("-" * 20)
    print(f"Starting transcript retrieval for: {video_url}")
    print(f"Requested language: {lang_code}")
    print(f"Target filename: {output_filename}")
    print("-" * 20)

    get_and_save_transcript(video_url, language=lang_code, filename=output_filename)

    print("-" * 20)
    print("Script finished.")
    print("-" * 20)