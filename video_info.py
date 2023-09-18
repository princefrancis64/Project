def video_info(youtube,channel_id):
    '''50 video details are being fetched from a particular YouTube Channel.

    We are getting an instance named response which in turn would help us to fetch the video_Ids of 50 videos.

    :param youtube: youtube instance created using the build method
    :param channel_id: Channel id of a YouTube channel
    :return: Intance
    '''
    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        eventType="none",
        maxResults=50,
        order="date",
        publishedAfter="2023-03-26T00:00:00Z",
        publishedBefore="2023-09-01T00:00:00Z",
        type="video")
    response = request.execute()
    return response


# if __name__=="__main__":
#     pass
