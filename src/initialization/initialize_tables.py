'''Initialize the database with empty tables.'''

import numpy as np
import pandas as pd
from src import DATA_PATH, TABLES_PATH
import os

def initialize_tables():

    users = pd.DataFrame(columns=[
        'user_id',
        'user_name',
        'user_bed_time',
        'user_wake_time',
        'user_lunch_time',
        'user_dinner_time',
        'user_work_time',
        'user_free_from_work_time',
        'user_work_days',
        'user_age',
        'user_gender',
        'user_location',
        'user_language',
        'user_ocupation',
        'user_education',
        'user_video_watching_time',
        'user_video_retention_time',
        'user_channel_id',
        'user_admin_channel_id',
    ])
    users.to_parquet(os.path.join(DATA_PATH, 'users.parquet'), index=False)

    channels = pd.DataFrame(columns=[
        'channel_id',
        'channel_name',
        'channel_creation_date',
        'channel_description',
        'channel_language',
        'channel_location',
        'channel_category',
    ])
    channels.to_parquet(os.path.join(DATA_PATH, 'channels.parquet'), index=False)

    content = pd.DataFrame(columns=[
        'content_id',
        'channel_id',
        'content_title',
        'content_description',
        'content_status',
        'content_category',
        'content_language',
        'content_duration',
        'content_creation_date',
        'content_view_count',
        'content_like_count',
        'content_dislike_count',
        'content_comment_count',
        'content_ind_rating',
        'content_type',
        'content_is_live',
        'content_comments',
    ])
    content.to_parquet(os.path.join(DATA_PATH, 'content.parquet'), index=False)

    comments = pd.DataFrame(columns=[
        'content_id',
        'comment_og_id',
        'comment_id',
        'comment_text',
        'comment_creation_date',
        'comment_author',
        'comment_like_count',
        'comment_dislike_count',
        'comment_reply_count',
        'comment_replies',
    ])
    comments.to_parquet(os.path.join(DATA_PATH, 'comments.parquet'), index=False)

    user = pd.DataFrame(columns=[
        'UserID',
        'UserName',
        'UserEmail',
        'UserPassword',
        'UserPhoto',
    ])
    user.to_parquet(os.path.join(TABLES_PATH, 'USER.parquet'), index=False)

    channel = pd.DataFrame(columns=[
        'ChannelID',
        'ChannelURL',
        'CHCreationDate',
        'CHName',
        'CHDesc',
        'CHWelcomeVID',
        'CHBanner',
        'UserID',
    ])
    channel.to_parquet(os.path.join(TABLES_PATH, 'CHANNEL.parquet'), index=False)

    uadminch = pd.DataFrame(columns=[
        'UserID',
        'ChannelID',
    ])
    uadminch.to_parquet(os.path.join(TABLES_PATH, 'UADMINCH.parquet'), index=False)

    uinterestch = pd.DataFrame(columns=[
        'UisSubToCH',
        'UMemberLevelCH',
        'UisNotifiedByCH',
        'UserID',
        'ChannelID',
    ])
    uinterestch.to_parquet(os.path.join(TABLES_PATH, 'UINTERESTCH.parquet'), index=False)

    content = pd.DataFrame(columns=[
        'ContentID',
        'ContentURL',
        'CONTTitle',
        'CONTPubDateTime',
        'CONTStatus',
        'CONTCategory',
        'CONTLanguage',
        'CONTThumb',
        'CONTDesc',
        'CONTCaptionLanguage',
        'CONTIndRating',
        'ChannelID',
    ])
    content.to_parquet(os.path.join(TABLES_PATH, 'CONTENT.parquet'), index=False)

    uwatchingcont = pd.DataFrame(columns=[
        'UWatchDurationCONT',
        'UWatchCONTDateTime',
        'UIsWatchingCONTNow',
        'UWATCHCONTID',
        'UserID',
        'ContentID',
    ])
    uwatchingcont.to_parquet(os.path.join(TABLES_PATH, 'UWATCHINGCONT.parquet'), index=False)

    live = pd.DataFrame(columns=[
        'LIVEBody',
        'ContentID',
    ])
    live.to_parquet(os.path.join(TABLES_PATH, 'LIVE.parquet'), index=False)

    video = pd.DataFrame(columns=[
        'VIDEOBody',
        'ContentID',
    ])
    video.to_parquet(os.path.join(TABLES_PATH, 'VIDEO.parquet'), index=False)
    
    short = pd.DataFrame(columns=[
        'SHMusicLink',
        'SHORTBody',
        'ContentID',
    ])
    short.to_parquet(os.path.join(TABLES_PATH, 'SHORT.parquet'), index=False)

    comment = pd.DataFrame(columns=[
        'CommentID',
        'COMDateTime',
        'COMisEdited',
        'COMBody',
        'UserID',
    ])
    comment.to_parquet(os.path.join(TABLES_PATH, 'COMMENT.parquet'), index=False)

    livecomment = pd.DataFrame(columns=[
        'CommentID',
        'ContentID',
    ])
    livecomment.to_parquet(os.path.join(TABLES_PATH, 'LIVECOMMENT.parquet'), index=False)

    commentreply = pd.DataFrame(columns=[
        'CommentID',
        'COMisRepByCOMCommentID',
    ])
    commentreply.to_parquet(os.path.join(TABLES_PATH, 'COMMENTREPLY.parquet'), index=False)
    
    videocomment = pd.DataFrame(columns=[
        'CommentID',
        'ContentID',
    ])
    videocomment.to_parquet(os.path.join(TABLES_PATH, 'VIDEOCOMMENT.parquet'), index=False)

    pollcomment = pd.DataFrame(columns=[
        'CommentID',
        'POLLID',
    ])
    pollcomment.to_parquet(os.path.join(TABLES_PATH, 'POLLCOMMENT.parquet'), index=False)
    
    shortcomment = pd.DataFrame(columns=[
        'CommentID',
        'ContentID',
    ])
    shortcomment.to_parquet(os.path.join(TABLES_PATH, 'SHORTCOMMENT.parquet'), index=False)

    poll = pd.DataFrame(columns=[
        'POLLID',
        'POLLPubDateTime',
        'POLLURL',
        'POLLBody',
        'ChannelID',
    ])
    poll.to_parquet(os.path.join(TABLES_PATH, 'POLL.parquet'), index=False)

    playlist = pd.DataFrame(columns=[
        'PlayID',
        'PlayURL',
        'PLAYTitle',
        'PLAYDesc',
        'PLAYStatus',
        'PLAYThumb',
        'ChannelID',
    ])
    playlist.to_parquet(os.path.join(TABLES_PATH, 'PLAYLIST.parquet'), index=False)

    playlistcontent = pd.DataFrame(columns=[
        'CONTAddDateTimePL',
        'ContentID',
        'PlayID',
    ])
    playlistcontent.to_parquet(os.path.join(TABLES_PATH, 'PLAYLISTCONTENT.parquet'), index=False)

    userinteraction = pd.DataFrame(columns=[
        'UINTType',
        'UINTID',
        'UserID',
    ])
    userinteraction.to_parquet(os.path.join(TABLES_PATH, 'USERINTERACTION.parquet'), index=False)

    ucontint = pd.DataFrame(columns=[
        'UINTID',
        'ContentID',
    ])
    ucontint.to_parquet(os.path.join(TABLES_PATH, 'UCONTINT.parquet'), index=False)

    ucomint = pd.DataFrame(columns=[
        'UINTID',
        'CommentID',
    ])
    ucomint.to_parquet(os.path.join(TABLES_PATH, 'UCOMINT.parquet'), index=False)

    uplayint = pd.DataFrame(columns=[
        'UINTID',
        'PlayID',
    ])
    uplayint.to_parquet(os.path.join(TABLES_PATH, 'UPLAYINT.parquet'), index=False)

    notification = pd.DataFrame(columns=[
        'NotificationID',
        'NOTBody',
        'ChannelID',
    ])
    notification.to_parquet(os.path.join(TABLES_PATH, 'NOTIFICATION.parquet'), index=False)

    usernotified = pd.DataFrame(columns=[
        'NOTSentDateTime',
        'UserID',
        'NotificationID',
    ])
    usernotified.to_parquet(os.path.join(TABLES_PATH, 'USERNOTIFIED.parquet'), index=False)

    channel_chextlink = pd.DataFrame(columns=[
        'CHExtLink',
        'ChannelID',
    ])
    channel_chextlink.to_parquet(os.path.join(TABLES_PATH, 'CHANNEL_CHExtLink.parquet'), index=False)

    content_conttag = pd.DataFrame(columns=[
        'CONTTag',
        'ContentID',
    ])
    content_conttag.to_parquet(os.path.join(TABLES_PATH, 'CONTENT_CONTTag.parquet'), index=False)

    playlist_playtag = pd.DataFrame(columns=[
        'PLAYTag',
        'PlayID',
    ])
    playlist_playtag.to_parquet(os.path.join(TABLES_PATH, 'PLAYLIST_PLAYTag.parquet'), index=False)
    
    return

TABLE_PATHS = {
    # DATA_PATH
    "users": os.path.join(DATA_PATH, 'users.parquet'),
    "channels": os.path.join(DATA_PATH, 'channels.parquet'),
    "content": os.path.join(DATA_PATH, 'content.parquet'),
    "comments": os.path.join(DATA_PATH, 'comments.parquet'),

    # TABLES_PATH
    "USER": os.path.join(TABLES_PATH, 'USER.parquet'),
    "CHANNEL": os.path.join(TABLES_PATH, 'CHANNEL.parquet'),
    "UADMINCH": os.path.join(TABLES_PATH, 'UADMINCH.parquet'),
    "UINTERESTCH": os.path.join(TABLES_PATH, 'UINTERESTCH.parquet'),
    "CONTENT": os.path.join(TABLES_PATH, 'CONTENT.parquet'),
    "UWATCHINGCONT": os.path.join(TABLES_PATH, 'UWATCHINGCONT.parquet'),
    "LIVE": os.path.join(TABLES_PATH, 'LIVE.parquet'),
    "VIDEO": os.path.join(TABLES_PATH, 'VIDEO.parquet'),
    "SHORT": os.path.join(TABLES_PATH, 'SHORT.parquet'),
    "COMMENT": os.path.join(TABLES_PATH, 'COMMENT.parquet'),
    "LIVECOMMENT": os.path.join(TABLES_PATH, 'LIVECOMMENT.parquet'),
    "COMMENTREPLY": os.path.join(TABLES_PATH, 'COMMENTREPLY.parquet'),
    "VIDEOCOMMENT": os.path.join(TABLES_PATH, 'VIDEOCOMMENT.parquet'),
    "POLLCOMMENT": os.path.join(TABLES_PATH, 'POLLCOMMENT.parquet'),
    "SHORTCOMMENT": os.path.join(TABLES_PATH, 'SHORTCOMMENT.parquet'),
    "POLL": os.path.join(TABLES_PATH, 'POLL.parquet'),
    "PLAYLIST": os.path.join(TABLES_PATH, 'PLAYLIST.parquet'),
    "PLAYLISTCONTENT": os.path.join(TABLES_PATH, 'PLAYLISTCONTENT.parquet'),
    "USERINTERACTION": os.path.join(TABLES_PATH, 'USERINTERACTION.parquet'),
    "UCONTINT": os.path.join(TABLES_PATH, 'UCONTINT.parquet'),
    "UCOMINT": os.path.join(TABLES_PATH, 'UCOMINT.parquet'),
    "UPLAYINT": os.path.join(TABLES_PATH, 'UPLAYINT.parquet'),
    "NOTIFICATION": os.path.join(TABLES_PATH, 'NOTIFICATION.parquet'),
    "USERNOTIFIED": os.path.join(TABLES_PATH, 'USERNOTIFIED.parquet'),
    "CHANNEL_CHExtLink": os.path.join(TABLES_PATH, 'CHANNEL_CHExtLink.parquet'),
    "CONTENT_CONTTag": os.path.join(TABLES_PATH, 'CONTENT_CONTTag.parquet'),
    "PLAYLIST_PLAYTag": os.path.join(TABLES_PATH, 'PLAYLIST_PLAYTag.parquet'),
    }


if __name__ == "__main__":
    initialize_tables()
    print("Tables initialized successfully.")