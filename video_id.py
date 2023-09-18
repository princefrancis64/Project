from pprint import pprint
video_ids=[]
def video_id(response,youtube):
    '''
    Gets the response instance for each video_id.

    First we are getting the response instance fetched from the videos list. Iterating through it we will get the
    video_Id and then append it to the lists video_ids. Once the list has been generated a instance is made for each
    video_Id

    :param response: Instance of the video
    :param youtube: Instance made using the build method
    :return: Instance of response
    '''

    for item in response['items']:
        title = item['snippet']['title']
        video_Id = item['id']['videoId']
        video_ids.append(video_Id)
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_Id)
        response = request.execute()
    return response


# pprint(video_id())


