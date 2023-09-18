def comments(response):
    '''
    Gets the comments of the video.

    We are looping through the object response and getting comments and author names. Once it is fetched it is been
    appended to the lists and then a dictionary has been made.

    :param response:This is an instance using each video ids which would help us to extract the comments
    :return:Dictionary of author and comment
    '''
    authors = []
    comment_texts = []
    for item in response['items']:
        comment = item['snippet']['topLevelComment']
        author = comment['snippet']['authorDisplayName']
        authors.append(author)
        comment_text = comment['snippet']['textDisplay']
        comment_texts.append(comment_text)
    comment_dict = {"Author":authors,
                    "Comment":comment_texts}
    return comment_dict











