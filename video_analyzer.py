import streamlit as st
from dotenv import load_dotenv
import os
import base64
from openai import OpenAI
import cv2
from moviepy.editor import VideoFileClip


load_dotenv()

# Initialize OpenAI client
MODEL = 'gpt-4o'
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
key  = os.getenv('OPENAI_API_KEY')



# Function to process video
def process_video(video_path, seconds_per_frame=2):
    base64Frames = []
    base_video_path, _ = os.path.splitext(video_path)
    
    video = cv2.VideoCapture(video_path)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = video.get(cv2.CAP_PROP_FPS)
    frames_to_skip = int(fps * seconds_per_frame)
    curr_frame = 0

    while curr_frame < total_frames - 1:
        video.set(cv2.CAP_PROP_POS_FRAMES, curr_frame)
        success, frame = video.read()
        if not success:
            break
        _, buffer = cv2.imencode(".jpg", frame)
        base64Frames.append(base64.b64encode(buffer).decode("utf-8"))
        curr_frame += frames_to_skip

    video.release()

    # Extract audio from video
    audio_path = f"{base_video_path}.mp3"
    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path, bitrate="32k")
    clip.audio.close()
    clip.close()

    return base64Frames, audio_path


# Streamlit UI
st.title("Video Analyser")

uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    with open("uploaded_video.mp4", "wb") as f:
        f.write(uploaded_file.read())
    
    # resizing the video to be displayed
    st.markdown(
    """
    <style>
    video {
        width: 300px !important;
        height: 300px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,

)


    st.video(uploaded_file)
    # Process video
    base64Frames, audio_path = process_video("uploaded_video.mp4", seconds_per_frame=1)

    # st.write("Extracted Frames")
    # for frame in base64Frames:
    #     st.image(f"data:image/jpg;base64,{frame}", use_column_width=True)
       

    # Correctly accessing the transcription text
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=open(audio_path, "rb"),
    )
    transcription_text = transcription.text
    st.write("### Audio Transcription")
    st.text(transcription_text)

    # Generate a summary
    # st.title("Video Summary")
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are generating a video summary. Create a summary of the provided video and its transcript. Respond in Markdown. Return Overall Frames Description, Audio Transcription and the summary"},
            {"role": "user", "content": [
                "These are the frames from the video.",
                *map(lambda x: {"type": "image_url", "image_url": {"url": f'data:image/jpg;base64,{x}', "detail": "low"}}, base64Frames),
                {"type": "text", "text": f"The audio transcription is: {transcription_text}"}
            ]}
        ],
        temperature=0,
    )
    st.markdown(response.choices[0].message.content)
    