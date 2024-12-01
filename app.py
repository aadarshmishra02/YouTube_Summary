import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# Load environment variables
load_dotenv()


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

PROMPT = """
You are a YouTube video summarizer. You will take the transcript text and summarize the entire video,
providing the important summary in bullet points within 250 words.
Please provide the summary of the text given here:
"""

def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("v=")[1].split("&")[0]
        transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([item["text"] for item in transcript_data])
        return transcript
    except Exception as e:
        st.error(f"Error: {e}")
        return None

def generate_gemini_content(transcript_text, prompt):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt + transcript_text)
        return response.text
    except Exception as e:
        st.error(f"Error: {e}")
        return None

st.title("YouTube Summary to Detailed Notes Converter")

youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    try:
        video_id = youtube_link.split("v=")[1].split("&")[0]
        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)
    except IndexError:
        st.warning("Please enter a valid YouTube video link.")


if st.button("Get Detailed Notes"):
    if youtube_link:
        transcript_text = extract_transcript_details(youtube_link)
        if transcript_text:
            summary = generate_gemini_content(transcript_text, PROMPT)
            if summary:
                st.markdown("## Detailed Notes:")
                st.write(summary)
