Video Analyser with Transcription and Summary Generation
Project Overview
This project is a web application that allows users to upload a video file, extracts audio from the video, transcribes the audio using OpenAI's Whisper model, 
and generates a summary of the video content based on the transcription. The application is built using Streamlit for the frontend and OpenAI API for the transcription and summary generation.

Table of Contents
Installation
Project Structure
How It Works
Usage
Customization
Dependencies
License

Installation
Clone the Repository
Open your terminal and run:
git clone <repository_url>
cd <repository_directory>

Install Dependencies
Make sure you have Python installed. Install the required packages using:
pip install -r requirements.txt

Environment Variables
Create a .env file in the project root and add your OpenAI API key:
OPENAI_API_KEY=<Your_OpenAI_API_Key>

Project Structure
.
├── app.py                     # Main Streamlit application for video analysis
├── requirements.txt           # List of project dependencies
└── .env                       # API key for OpenAI


How It Works
Video Upload: The user uploads a video file (mp4, mov, avi) using the Streamlit file uploader.
Video Processing: The application uses OpenCV to process the video, extracting frames at specified intervals and converting the audio to an MP3 file.
Audio Transcription: The extracted audio is sent to OpenAI's Whisper model to generate a text transcription of the audio content.
Summary Generation: The application generates a summary of the video based on the transcription text using the OpenAI chat model.
Output Display: The transcribed text and summary are displayed on the Streamlit app.
Usage

Run the Application
Start the Streamlit application with:
streamlit run app.py
Upload a Video
Use the file uploader to select and upload a video file. The app will process the video and display the transcription and summary.

View Results
After processing, the application will display the audio transcription and the generated summary.
Customization
Change Frame Extraction Interval: Adjust the seconds_per_frame parameter in the process_video function to modify how frequently frames are extracted from the video.
Model Selection: You can switch the OpenAI model used for transcription and summarization by modifying the MODEL variable.

Styling the UI: Customize the UI by modifying the Streamlit components and layout.

Dependencies
The application requires the following libraries:

Streamlit: For the web interface.
OpenAI: For transcription and summary generation.
OpenCV: For video processing.
MoviePy: For audio extraction from video.
python-dotenv: To load environment variables from the .env file.

To install the dependencies, run:
pip install -r requirements.txt

License
This project is licensed under the MIT License. You are free to use, modify, and distribute this project.

