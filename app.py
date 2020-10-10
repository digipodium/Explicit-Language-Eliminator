import streamlit as st 
import Youtube_functions as yf
from validators.url import url
import os
import Download_path as dp

st.title('Youtube Video and Audio Downloader!')

st.sidebar.title('You want Audio or Video:')
a_or_v=st.sidebar.radio("Select: ",("Audio","Video"))

link=st.text_input('Enter the URL of Youtube Video: ')
st.button('Check validity')
valid=url(link)
if valid and link:
    title=yf.get_title(link)
    streams=yf.get_streams(link)
    res ={}
    if a_or_v=='Video':
        for i in streams:
            res[i.resolution]=i.itag
        # print(type(res.values()))
        tag = st.selectbox("Select Resolution",list(res.keys()))
        if tag!=None:
            # path=st.text_input('Where do you want to download the video? Enter Path: ')
            home=st.text_input("Enter Name of home folder: ")
            if home:
                path=st.radio("Select",dp.download_paths(home))
                path=os.path.join(dp.get_home_path(home),path)
                if path:
                    if st.button('Download video'):
                        yf.download_video(link=link,vid_path=path,tag=res[tag])
                        st.balloons()
                        st.success('VIDEO DOWNLOAD COMPLETE!')
                else:
                    st.warning('Please Choose a Valid Path')
    else:
        # path=st.text_input('Where do you want to download the audio? Enter Path: ')
        home=st.text_input("Enter Name of home folder: ")
        if home:
            path=st.radio("Select",dp.download_paths(home))
            path=os.path.join(dp.get_home_path(home),path)
            if path:
                if st.button('Download Audio'):
                    yf.audio_from_video(link=link,aud_path=path)
                    st.balloons()
                    st.success('AUDIO DOWNLOAD COMPLETE!')
            else:
                st.warning('Please Choose a Valid Path')

else:
    st.warning("Please enter valid link")

 