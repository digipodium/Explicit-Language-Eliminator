from youtube_transcript_api import YouTubeTranscriptApi
from better_profanity import profanity
from pytube import YouTube
import moviepy
import moviepy.editor as mp
import speech_recognition as sr 
import os

SAVE_VIDEO_PATH = "downloads_yt/videos"
SAVE_TRANSCRIPT_PATH="downloads_yt/transcripts"
SAVE_AUDIO_PATH="downloads_yt/audios"

def clean_transcript(link):
    video_id=gen_id(link)

    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    transcript = transcript_list.find_generated_transcript(['en'])
    transcript=transcript.fetch()
    profanity.load_censor_words()
    for i in transcript:
        i['text']=profanity.censor(i['text'])
        
    title=get_title(link)
    
    if not os.path.exists(((os.path.join(SAVE_TRANSCRIPT_PATH,title))+'.txt')):
        file1=open(((os.path.join(SAVE_TRANSCRIPT_PATH,title))+'.txt'),'a')
        for line in transcript:
            text=line['text']
            start=line['start']
            duration=line['duration']
            inf=[text,start,duration]
            file1.writelines(str(inf))
            file1.write('\n')
        file1.close()
        print('Transcript saved to',((os.path.join(SAVE_TRANSCRIPT_PATH,title))+'.txt'))
    else:
        print('File Already Exists!')
        print()
        
    return transcript

    
def explicit_language_timestamps(transcript):
    time_stamps=list()
    j=0
    for i in transcript:
        if '****' in i['text']:
            time_stamps.append(i)
            j+=1
    return time_stamps

def gen_id(link):
    return (link.split('=')[1])

def get_title(link):
    try: 
        #object creation using YouTube which was imported in the beginning 
        yt = YouTube(link) 
    except: 
        print("Connection Error")
    ori_title=yt.title
    title= [character for character in ori_title if character.isalnum() or character==' ']
    title = "".join(title)
    title=title.replace(' ','_')
    return title
    
def download_video(link):
    try: 
        #object creation using YouTube which was imported in the beginning 
        yt = YouTube(link) 
    except: 
        print("Connection Error")
    # mp4files = yt.streams.filter('mp4') 
    d_video = yt.streams.first()
    title=get_title(link)
    try: 
        #downloading the video 
        d_video.download(output_path=SAVE_VIDEO_PATH,filename=title) 
        print('Task Completed!') 
    except: 
        print("Some Error!") 
        

def audio_from_video(link):
    title=get_title(link)
    video = mp.VideoFileClip((os.path.join(SAVE_VIDEO_PATH,title))+'.mp4')
    audio = video.audio
    audio.write_audiofile(os.path.join(SAVE_AUDIO_PATH,title)+'.mp3')