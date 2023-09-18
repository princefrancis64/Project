import pandas as pd



l_likes = []
l_title = []
l_number_of_comments = []
l_view_count = []
l_thumbnail_url = []
l_video_link = []
l_channel_title= []
def details(youtube,video_ids):
    '''
    Fetching all the details of the video.

    youtube instance is passed and then iterating through each of the video_ids we are getting likes,title,number_of_comments,
    view_count,thumbnail_url,video_link. Each of the values are appended to a list and then a dictionary is made.

    :param youtube: Youtube instance made using the build method
    :param video_ids: list of video_ids
    :return: Dictionary
    '''
    request = youtube.videos().list(
        part="snippet,statistics",
        id=[i for i in video_ids]
    )
    response = request.execute()
    for i in response['items']:
        channel_title = i['snippet']['channelTitle']
        l_channel_title.append(channel_title)
        likes = int(i['statistics']['likeCount'])
        l_likes.append(likes)
        title = i['snippet']['title']
        l_title.append(title)
        number_of_comments = int(i['statistics']['commentCount'])
        l_number_of_comments.append(number_of_comments)
        view_count = int(i['statistics']['viewCount'])
        l_view_count.append(view_count)
        thumbnail_url = i['snippet']['thumbnails']['high']['url']
        l_thumbnail_url.append(thumbnail_url)
        video_link = 'https://www.youtube.com/watch?v=' + i['id']
        l_video_link.append(video_link)

    video_details = {"Title": l_title,
                     "Views": l_view_count,
                     "Likes": l_likes,
                     "Comments": l_number_of_comments,
                     "Thumbnail url": l_thumbnail_url,
                     "Video link": l_video_link,
                     "Video ID": video_ids,
                     "Channel Title":l_channel_title}

    df = pd.DataFrame(video_details)
    return video_details

