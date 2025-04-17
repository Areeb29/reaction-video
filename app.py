import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import openai
import time
import re
import os
from dotenv import load_dotenv
load_dotenv()


# ---- SETUP ---- #

assistant_id = "asst_7db5YXfZAUjQ8htf3PY7ZuDL"
client = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))

# Create a thread once
thread = client.beta.threads.create()
thread_id = thread.id

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

def get_assistant_response(content, instructions):
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role='user',
        content=content
    )

    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
        instructions=instructions
    )

    with st.spinner("Processing..."):
        while True:
            run_status = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
            if run_status.status == 'completed':
                break
            elif run_status.status == 'failed':
                raise Exception("Assistant run failed.")
            time.sleep(5)

    messages = client.beta.threads.messages.list(thread_id=thread_id)
    return messages.data[0].content[0].text.value

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
                    response = get_assistant_response(prompt, instructions)
                    st.subheader("🗣️ AI-Generated Script")
                    st.write(response)
            else:
                instructions = "Use the same tone as in the prompt. Reply like a human would."
                response = get_assistant_response(user_input, instructions)
                st.subheader("💬 Assistant Response")
                st.write(response)
        except Exception as e:
            st.error(f"Error: {e}")
