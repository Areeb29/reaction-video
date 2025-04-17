import streamlit as st
import requests
import re
import time
from youtube_transcript_api import YouTubeTranscriptApi

# ---- AZURE OPENAI CONFIG ---- #
AZURE_OPENAI_ENDPOINT = "https://emailsender231.openai.azure.com/"
AZURE_OPENAI_KEY = "7ZN2Pw4PMttsHR3newyNxG99I7T4aI6s568SiCMnC2wMnNSKNJPgJQQJ99BDACHYHv6XJ3w3AAABACOGjt3s"
AZURE_OPENAI_DEPLOYMENT = "gpt-35-turbo"  # Example: "gpt-35-turbo"
AZURE_OPENAI_API_VERSION = "2023-12-01-preview"

# ---- FUNCTIONS ---- #
def extract_video_id(url):
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        raise ValueError("Invalid YouTube URL")

def get_transcript(video_url):
    try:
        video_id = extract_video_id(video_url)
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return ' '.join([entry['text'] for entry in transcript])
    except Exception as e:
        st.error(f"Transcript error: {e}")
        return None

def get_azure_openai_response(prompt, system_message="You are a helpful assistant."):
    url = f"{AZURE_OPENAI_ENDPOINT}openai/deployments/{AZURE_OPENAI_DEPLOYMENT}/chat/completions?api-version={AZURE_OPENAI_API_VERSION}"

    headers = {
        "Content-Type": "application/json",
        "api-key": AZURE_OPENAI_KEY
    }

    body = {
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 2000
    }

    response = requests.post(url, headers=headers, json=body)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise Exception(f"Azure OpenAI Error {response.status_code}: {response.text}")

# ---- STREAMLIT UI ---- #
st.set_page_config(page_title="YouTube Reaction Generator", layout="centered")
st.title("🎬 YouTube Reaction Video Script Generator")

user_input = st.text_input("🔗 Enter YouTube URL or custom message")
language = st.selectbox("🌐 Language", ["German", "English", "Spanish", "French"], index=0)
length = st.selectbox("📝 Summary Length", ["Short", "Medium", "To the point"], index=1)
style = st.selectbox("🎨 Style", ["Informative", "Funny", "Dramatic", "Debate style"], index=0)
add_info = st.text_input("🧠 Additional Instructions (optional)", value="")

if st.button("🚀 Generate"):
    if user_input.strip() == "":
        st.warning("Please enter a URL or message.")
    else:
        try:
            if user_input.startswith("https://yout"):
                st.video(user_input)
                transcript = get_transcript(user_input)

                if transcript:
                    prompt = (
                        f"Generate very detailed content for a YouTube reaction video in {language} using this transcript. "
                        f"Make it creative and engaging (speak like a person). Cover all names, events, dates, etc. "
                        f"The tone should be {style.lower()}. Make it at least 1500 words. "
                        f"Additional notes: {add_info or 'None'}\n\nTranscript:\n{transcript}"
                    )
                    instructions = "Follow the user's prompt strictly. Avoid any markdown or styling symbols like *, #, etc."
                    response = get_azure_openai_response(prompt, system_message=instructions)
                    st.subheader("🗣️ AI-Generated Script")
                    st.write(response)
            else:
                instructions = "Use the same tone as in the prompt. Reply like a human would."
                response = get_azure_openai_response(user_input, system_message=instructions)
                st.subheader("💬 Assistant Response")
                st.write(response)
        except Exception as e:
            st.error(f"Error: {e}")
