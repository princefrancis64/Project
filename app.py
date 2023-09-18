import pandas as pd
from googleapiclient.discovery import build
from pytube import YouTube
from flask import Flask,render_template,request,redirect,url_for
from video_info import video_info
from video_id import video_ids,video_id
from video_details import details
from sqlalchemy import create_engine
from comments import comments
import os
import requests
import base64
from pymongo.mongo_client import MongoClient
import logging


app = Flask(__name__)
logging.basicConfig(filename="test.log",level = logging.DEBUG,format = "%(levelname)s %(name)s %(asctime)s %(message)s")

username = "root"
password ="Letsgo1247"
database ="ineuron"
host = "localhost"
port = "3306"
database_name = "ineuron"
engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}:{port}/{database_name}?charset=utf8mb4")
conn = engine.connect()

#getting the youtube instance
def get_youtube():
    ''' instance using build module.

    This would get an instance of the build which would help us to get the video details from YouTube

    :return: object'''
    YOUTUBE_API_SERVICE_NAME = 'youtube'
    YOUTUBE_API_VERSION = 'v3'
    DEVELOPER_KEY = 'Enter API'
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)
    return youtube

#rendering our index page
@app.route('/',methods = ['GET'])
def home():
    '''Render Home page.

    This route renders the home page of the web applicatoin which is index.html

     :return:HTML content of webpage
     :rtype:str'''
    try:
        return render_template("index.html")
    except Exception as e:
        logging.error(e)

#getting the url from the html page
channel_id=''
@app.route('/request',methods=['POST'])
def url():
    '''Function will get the url entered and then redirect to another route.

    The function would first read the entered url from the user and then gets an instance using pytube module.
    This instance is used to get the channel id of the entered url which inturn is used to get a list of videos
    from particular channel

    :return:HTML page content for the route linked to function id'''
    try:
        youtube_url = request.form['y_url']
        yt = YouTube(youtube_url)
        CHANNEL_ID = str(yt.channel_id)
        channel_id = CHANNEL_ID
        logging.info("Channel ID of the youtube channel is %s",channel_id)
        return redirect(url_for('id', channel_id=CHANNEL_ID))
    except Exception as e:
        logging.error(e)



@app.route('/channelid')
def id():
    '''Loads the details of the video and loads it to MYSQL and shows it as an HTML page.

    The function would first read the passed on value from the route '/request' and store it in a variable.
    video_info is called to get an instance which in turn is passed down to videos_with_id to help us to get a
    list of video_ids. Once the video_ids list has been generated details of each video is generated which is
    converted into a dictionary df. This dictionary is passed to the table.html which displays the content. We also
    convert the dictionary df to a dataframe and then load it to mysql using sqlalchemy

    :return:HTML page with a list of videos in the channel and video details
    :rtype:str:'''
    try:
        channel_id = request.args.get('channel_id')
        response = video_info(get_youtube(), channel_id)
        videos_with_id = video_id(response, get_youtube())
        df = details(get_youtube(), video_ids)
        logging.info("We have got our Dictionary of the values which needs to be the table ")
        # converting to dataframe
        Data = pd.DataFrame(df)
        Data.to_sql("youtube_scrapper", conn, if_exists="replace")
        logging.info("Dataframe successfully loaded to mysql database")
        return render_template("table.html", df=df)
    except Exception as e:
        logging.error(e)

@app.route('/details/<id>')
def details1(id):
    '''Render the page where video will be streamed.

    Using the function we first get the passed on values from the route '/channelid' and then return a page
    Stream_video.html

    :param id:Video Id of each video
    :return:HTML page content to stream the video ,download it and see the comment section'''
    try:
        url1 = request.args.get("url1")
        img = request.args.get("img")
        logging.info("url1 and img has been sucessfully read")
        return render_template("Stream_video.html", id=id, url1=url1, img=img)
    except Exception as e:
        logging.error(e)




@app.route('/download')
def download():
    '''Downloads the video to the folder.

    The link helps us to read down the video url link. Once the link has been read it can be used to download
    the particular video using the download button in the page Stream_video.html. If the Downloads folder is not
    there the os module will create it and download the video into the folder

    :return: HTML page with download message
    :rtype:str
    '''
    try:
        link = request.args.get("homepage")
        yt = YouTube(link)
        streams = yt.streams.filter(progressive=True, file_extension="mp4")
        stream = yt.streams.get_by_itag(22)
        Folder_name = "Downloads"
        if not os.path.exists(Folder_name):
            os.makedirs(Folder_name)
        stream.download(output_path=r".\Downloads")
        logging.info("File has been successfully downloaded to Downloads folder!!")
        return render_template("download.html")
    except Exception as e:
        logging.error(e)

@app.route('/comments/<id>')
def comments1(id):
    '''
    Comments of the particular video is been fetched.

    video id of each videos have been passed down and we create an instance response. comments() is used to
    return a table with author name and comments underneath the video
    :param id: Video ID of each video
    :return: HTML page with comments
    :rtype:str
    '''
    try:
        request = get_youtube().commentThreads().list(
            part="snippet",
            videoId=id)
        response = request.execute()
        request1 = get_youtube().videos().list(
            part="snippet,statistics",
            id=id
        )
        response = request.execute()
        response1 = request1.execute()
        comment_each_video = comments(response)
        for i in response1['items']:
            channel_title = i['snippet']['channelTitle']
            thumbnail = i['snippet']['thumbnails']['high']['url']
            # comment_each_video['YouTuber Name':channel_title]
        comment_each_video['YouTuber Name'] = channel_title
        logging.info("encoding thumbnail into base64")
        response = requests.get(thumbnail)
        base64_image = base64.b64encode(response.content).decode('utf-8')
        comment_each_video['base64 thumbnail'] = base64_image
        logging.info("We have successfully converted the image to base64 format and appended to our dictionary")
        uri = "mongodb+srv://princefrancis64:Oejb2e2l74Gz4NAK@cluster0.o5qm0dq.mongodb.net/?retryWrites=true&w=majority"
        client = MongoClient(uri)
        database = client['YouTube_scrapper']
        collection = database['comments']
        collection.insert_one(comment_each_video)
        logging.info("Successfully inserted Author Name,Comments,Youtuber Name,thumbnail image in base64 to MongoDB")
        return render_template("comments.html", comment=comment_each_video)
    except Exception as e:
        logging.error(e)



if __name__=='__main__':
    app.run(debug=True)
