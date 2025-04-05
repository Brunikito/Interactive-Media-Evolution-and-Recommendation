import pandas as pd

# Insert a user
def insert_user(user_id, user_name, user_email, user_password, user_photo):
    user = pd.read_csv('data/tables/USER.csv')
    user = user.append({
        'UserID': user_id,
        'UserName': user_name,
        'UserEmail': user_email,
        'UserPassword': user_password,
        'UserPhoto': user_photo
    }, ignore_index=True)
    user.to_csv('data/tables/USER.csv', index=False)

# User creating a channel
def create_channel(channel_id, channel_url, creation_date, name, desc, welcome_vid, banner, user_id):
    channel = pd.read_csv('data/tables/CHANNEL.csv')
    channel = channel.append({
        'ChannelID': channel_id,
        'ChannelURL': channel_url,
        'CHCreationDate': creation_date,
        'CHName': name,
        'CHDesc': desc,
        'CHWelcomeVID': welcome_vid,
        'CHBanner': banner,
        'UserID': user_id
    }, ignore_index=True)
    channel.to_csv('data/tables/CHANNEL.csv', index=False)

# Channel producing content
def produce_content(content_id, content_url, title, pub_date, status, category, language, thumb, desc, caption_lang, ind_rating, channel_id, content_type):
    content = pd.read_csv('data/tables/CONTENT.csv')
    content = content.append({
        'ContentID': content_id,
        'ContentURL': content_url,
        'CONTTitle': title,
        'CONTPubDateTime': pub_date,
        'CONTStatus': status,
        'CONTCategory': category,
        'CONTLanguage': language,
        'CONTThumb': thumb,
        'CONTDesc': desc,
        'CONTCaptionLanguage': caption_lang,
        'CONTIndRating': ind_rating,
        'ChannelID': channel_id
    }, ignore_index=True)
    content.to_csv('data/tables/CONTENT.csv', index=False)

    if content_type == 'video':
        video = pd.read_csv('data/tables/VIDEO.csv')
        video = video.append({'VIDEOBody': desc, 'ContentID': content_id}, ignore_index=True)
        video.to_csv('data/tables/VIDEO.csv', index=False)
    elif content_type == 'short':
        short = pd.read_csv('data/tables/SHORT.csv')
        short = short.append({'SHORTBody': desc, 'ContentID': content_id}, ignore_index=True)
        short.to_csv('data/tables/SHORT.csv', index=False)
    elif content_type == 'live':
        live = pd.read_csv('data/tables/LIVE.csv')
        live = live.append({'LIVEBody': desc, 'ContentID': content_id}, ignore_index=True)
        live.to_csv('data/tables/LIVE.csv', index=False)

# User commenting
def add_comment(comment_id, content_id, text, creation_date, author, like_count, dislike_count, reply_count, is_reply_to=None):
    comment = pd.read_csv('data/tables/COMMENT.csv')
    comment = comment.append({
        'CommentID': comment_id,
        'COMDateTime': creation_date,
        'COMisEdited': False,
        'COMBody': text,
        'UserID': author
    }, ignore_index=True)
    comment.to_csv('data/tables/COMMENT.csv', index=False)

    if is_reply_to:
        commentreply = pd.read_csv('data/tables/COMMENTREPLY.csv')
        commentreply = commentreply.append({'CommentID': comment_id, 'COMisRepByCOMCommentID': is_reply_to}, ignore_index=True)
        commentreply.to_csv('data/tables/COMMENTREPLY.csv', index=False)

    if content_id.startswith('VID'):
        videocomment = pd.read_csv('data/tables/VIDEOCOMMENT.csv')
        videocomment = videocomment.append({'CommentID': comment_id, 'ContentID': content_id}, ignore_index=True)
        videocomment.to_csv('data/tables/VIDEOCOMMENT.csv', index=False)
    elif content_id.startswith('SH'):
        shortcomment = pd.read_csv('data/tables/SHORTCOMMENT.csv')
        shortcomment = shortcomment.append({'CommentID': comment_id, 'ContentID': content_id}, ignore_index=True)
        shortcomment.to_csv('data/tables/SHORTCOMMENT.csv', index=False)
    elif content_id.startswith('LIVE'):
        livecomment = pd.read_csv('data/tables/LIVECOMMENT.csv')
        livecomment = livecomment.append({'CommentID': comment_id, 'ContentID': content_id}, ignore_index=True)
        livecomment.to_csv('data/tables/LIVECOMMENT.csv', index=False)
    elif content_id.startswith('POLL'):
        pollcomment = pd.read_csv('data/tables/POLLCOMMENT.csv')
        pollcomment = pollcomment.append({'CommentID': comment_id, 'POLLID': content_id}, ignore_index=True)
        pollcomment.to_csv('data/tables/POLLCOMMENT.csv', index=False)

# User interaction
def add_interaction(interaction_type, interaction_id, user_id, target_id, target_type):
    userinteraction = pd.read_csv('data/tables/USERINTERACTION.csv')
    userinteraction = userinteraction.append({
        'UINTType': interaction_type,
        'UINTID': interaction_id,
        'UserID': user_id
    }, ignore_index=True)
    userinteraction.to_csv('data/tables/USERINTERACTION.csv', index=False)

    if target_type == 'content':
        ucontint = pd.read_csv('data/tables/UCONTINT.csv')
        ucontint = ucontint.append({'UINTID': interaction_id, 'ContentID': target_id}, ignore_index=True)
        ucontint.to_csv('data/tables/UCONTINT.csv', index=False)
    elif target_type == 'comment':
        ucomint = pd.read_csv('data/tables/UCOMINT.csv')
        ucomint = ucomint.append({'UINTID': interaction_id, 'CommentID': target_id}, ignore_index=True)
        ucomint.to_csv('data/tables/UCOMINT.csv', index=False)
    elif target_type == 'playlist':
        uplayint = pd.read_csv('data/tables/UPLAYINT.csv')
        uplayint = uplayint.append({'UINTID': interaction_id, 'PlayID': target_id}, ignore_index=True)
        uplayint.to_csv('data/tables/UPLAYINT.csv', index=False)

# Channel producing a poll
def produce_poll(poll_id, pub_date, url, body, channel_id):
    poll = pd.read_csv('data/tables/POLL.csv')
    poll = poll.append({
        'POLLID': poll_id,
        'POLLPubDateTime': pub_date,
        'POLLURL': url,
        'POLLBody': body,
        'ChannelID': channel_id
    }, ignore_index=True)
    poll.to_csv('data/tables/POLL.csv', index=False)

# User watching content
def user_watch_content(watch_duration, watch_datetime, is_watching_now, watch_id, user_id, content_id):
    uwatchingcont = pd.read_csv('data/tables/UWATCHINGCONT.csv')
    uwatchingcont = uwatchingcont.append({
        'UWatchDurationCONT': watch_duration,
        'UWatchCONTDateTime': watch_datetime,
        'UIsWatchingCONTNow': is_watching_now,
        'UWATCHCONTID': watch_id,
        'UserID': user_id,
        'ContentID': content_id
    }, ignore_index=True)
    uwatchingcont.to_csv('data/tables/UWATCHINGCONT.csv', index=False)

# Channel creating a playlist
def create_playlist(playlist_id, playlist_url, title, desc, status, thumb, channel_id):
    playlist = pd.read_csv('data/tables/PLAYLIST.csv')
    playlist = playlist.append({
        'PlayID': playlist_id,
        'PlayURL': playlist_url,
        'PLAYTitle': title,
        'PLAYDesc': desc,
        'PLAYStatus': status,
        'PLAYThumb': thumb,
        'ChannelID': channel_id
    }, ignore_index=True)
    playlist.to_csv('data/tables/PLAYLIST.csv', index=False)

# Playlist containing content
def add_content_to_playlist(add_datetime, content_id, playlist_id):
    playlistcontent = pd.read_csv('data/tables/PLAYLISTCONTENT.csv')
    playlistcontent = playlistcontent.append({
        'CONTAddDateTimePL': add_datetime,
        'ContentID': content_id,
        'PlayID': playlist_id
    }, ignore_index=True)
    playlistcontent.to_csv('data/tables/PLAYLISTCONTENT.csv', index=False)

# Channel creating a notification
def create_notification(notification_id, body, channel_id):
    notification = pd.read_csv('data/tables/NOTIFICATION.csv')
    notification = notification.append({
        'NotificationID': notification_id,
        'NOTBody': body,
        'ChannelID': channel_id
    }, ignore_index=True)
    notification.to_csv('data/tables/NOTIFICATION.csv', index=False)

# Notification sent to user
def send_notification_to_user(sent_datetime, user_id, notification_id):
    usernotified = pd.read_csv('data/tables/USERNOTIFIED.csv')
    usernotified = usernotified.append({
        'NOTSentDateTime': sent_datetime,
        'UserID': user_id,
        'NotificationID': notification_id
    }, ignore_index=True)
    usernotified.to_csv('data/tables/USERNOTIFIED.csv', index=False)

# Add admin to channel
def add_admin_to_channel(user_id, channel_id):
    uadminch = pd.read_csv('data/tables/UADMINCH.csv')
    uadminch = uadminch.append({
        'UserID': user_id,
        'ChannelID': channel_id
    }, ignore_index=True)
    uadminch.to_csv('data/tables/UADMINCH.csv', index=False)

# User interest in channel
def add_user_interest_in_channel(is_subscribed, member_level, is_notified, user_id, channel_id):
    uinterestch = pd.read_csv('data/tables/UINTERESTCH.csv')
    uinterestch = uinterestch.append({
        'UisSubToCH': is_subscribed,
        'UMemberLevelCH': member_level,
        'UisNotifiedByCH': is_notified,
        'UserID': user_id,
        'ChannelID': channel_id
    }, ignore_index=True)
    uinterestch.to_csv('data/tables/UINTERESTCH.csv', index=False)

# Modify user interest in channel
def modify_user_interest_in_channel(user_id, channel_id, is_subscribed=None, member_level=None, is_notified=None):
    uinterestch = pd.read_csv('data/tables/UINTERESTCH.csv')
    index = uinterestch[(uinterestch['UserID'] == user_id) & (uinterestch['ChannelID'] == channel_id)].index
    if not index.empty:
        if is_subscribed is not None:
            uinterestch.at[index, 'UisSubToCH'] = is_subscribed
        if member_level is not None:
            uinterestch.at[index, 'UMemberLevelCH'] = member_level
        if is_notified is not None:
            uinterestch.at[index, 'UisNotifiedByCH'] = is_notified
        uinterestch.to_csv('data/tables/UINTERESTCH.csv', index=False)
