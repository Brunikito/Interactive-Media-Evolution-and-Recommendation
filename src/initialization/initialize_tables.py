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
    users.to_csv(os.path.join(DATA_PATH, 'users.csv'), index=False)

    channels = pd.DataFrame(columns=[
        'channel_id',
        'channel_name',
        'channel_creation_date',
        'channel_description',
        'channel_language',
        'channel_location',
        'channel_category',
    ])
    channels.to_csv(os.path.join(DATA_PATH, 'channels.csv'), index=False)

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
    content.to_csv(os.path.join(DATA_PATH, 'content.csv'), index=False)

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
    comments.to_csv(os.path.join(DATA_PATH, 'comments.csv'), index=False)

    user = pd.DataFrame(columns=[
        'UserID',
        'UserName',
        'UserEmail',
        'UserPassword',
        'UserPhoto',
    ])
    user.to_csv(os.path.join(TABLES_PATH, 'USER.csv'), index=False)

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
    channel.to_csv(os.path.join(TABLES_PATH, 'CHANNEL.csv'), index=False)

    uadminch = pd.DataFrame(columns=[
        'UserID',
        'ChannelID',
    ])
    uadminch.to_csv(os.path.join(TABLES_PATH, 'UADMINCH.csv'), index=False)

    uinterestch = pd.DataFrame(columns=[
        'UisSubToCH',
        'UMemberLevelCH',
        'UisNotifiedByCH',
        'UserID',
        'ChannelID',
    ])
    uinterestch.to_csv(os.path.join(TABLES_PATH, 'UINTERESTCH.csv'), index=False)

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
    content.to_csv(os.path.join(TABLES_PATH, 'CONTENT.csv'), index=False)

    uwatchingcont = pd.DataFrame(columns=[
        'UWatchDurationCONT',
        'UWatchCONTDateTime',
        'UIsWatchingCONTNow',
        'UWATCHCONTID',
        'UserID',
        'ContentID',
    ])
    uwatchingcont.to_csv(os.path.join(TABLES_PATH, 'UWATCHINGCONT.csv'), index=False)

    live = pd.DataFrame(columns=[
        'LIVEBody',
        'ContentID',
    ])
    live.to_csv(os.path.join(TABLES_PATH, 'LIVE.csv'), index=False)

    video = pd.DataFrame(columns=[
        'VIDEOBody',
        'ContentID',
    ])
    video.to_csv(os.path.join(TABLES_PATH, 'VIDEO.csv'), index=False)

    comment = pd.DataFrame(columns=[
        'CommentID',
        'COMDateTime',
        'COMisEdited',
        'COMBody',
        'UserID',
    ])
    comment.to_csv(os.path.join(TABLES_PATH, 'COMMENT.csv'), index=False)

    livecomment = pd.DataFrame(columns=[
        'CommentID',
        'ContentID',
    ])
    livecomment.to_csv(os.path.join(TABLES_PATH, 'LIVECOMMENT.csv'), index=False)

    commentreply = pd.DataFrame(columns=[
        'CommentID',
        'COMisRepByCOMCommentID',
    ])
    commentreply.to_csv(os.path.join(TABLES_PATH, 'COMMENTREPLY.csv'), index=False)
    
    videocomment = pd.DataFrame(columns=[
        'CommentID',
        'ContentID',
    ])
    videocomment.to_csv(os.path.join(TABLES_PATH, 'VIDEOCOMMENT.csv'), index=False)

    pollcomment = pd.DataFrame(columns=[
        'CommentID',
        'POLLID',
    ])
    pollcomment.to_csv(os.path.join(TABLES_PATH, 'POLLCOMMENT.csv'), index=False)
    
    shortcomment = pd.DataFrame(columns=[
        'CommentID',
        'ContentID',
    ])
    shortcomment.to_csv(os.path.join(TABLES_PATH, 'SHORTCOMMENT.csv'), index=False)

    poll = pd.DataFrame(columns=[
        'POLLID',
        'POLLPubDateTime',
        'POLLURL',
        'POLLBody',
        'ChannelID',
    ])
    poll.to_csv(os.path.join(TABLES_PATH, 'POLL.csv'), index=False)

    playlist = pd.DataFrame(columns=[
        'PlayID',
        'PlayURL',
        'PLAYTitle',
        'PLAYDesc',
        'PLAYStatus',
        'PLAYThumb',
        'ChannelID',
    ])
    playlist.to_csv(os.path.join(TABLES_PATH, 'PLAYLIST.csv'), index=False)

    playlistcontent = pd.DataFrame(columns=[
        'CONTAddDateTimePL',
        'ContentID',
        'PlayID',
    ])
    playlistcontent.to_csv(os.path.join(TABLES_PATH, 'PLAYLISTCONTENT.csv'), index=False)

    userinteraction = pd.DataFrame(columns=[
        'UINTType',
        'UINTID',
        'UserID',
    ])
    userinteraction.to_csv(os.path.join(TABLES_PATH, 'USERINTERACTION.csv'), index=False)

    ucontint = pd.DataFrame(columns=[
        'UINTID',
        'ContentID',
    ])
    ucontint.to_csv(os.path.join(TABLES_PATH, 'UCONTINT.csv'), index=False)

    ucomint = pd.DataFrame(columns=[
        'UINTID',
        'CommentID',
    ])
    ucomint.to_csv(os.path.join(TABLES_PATH, 'UCOMINT.csv'), index=False)

    uplayint = pd.DataFrame(columns=[
        'UINTID',
        'PlayID',
    ])
    uplayint.to_csv(os.path.join(TABLES_PATH, 'UPLAYINT.csv'), index=False)

    notification = pd.DataFrame(columns=[
        'NotificationID',
        'NOTBody',
        'ChannelID',
    ])
    notification.to_csv(os.path.join(TABLES_PATH, 'NOTIFICATION.csv'), index=False)

    usernotified = pd.DataFrame(columns=[
        'NOTSentDateTime',
        'UserID',
        'NotificationID',
    ])
    usernotified.to_csv(os.path.join(TABLES_PATH, 'USERNOTIFIED.csv'), index=False)

    channel_chextlink = pd.DataFrame(columns=[
        'CHExtLink',
        'ChannelID',
    ])
    channel_chextlink.to_csv(os.path.join(TABLES_PATH, 'CHANNEL_CHExtLink.csv'), index=False)

    content_conttag = pd.DataFrame(columns=[
        'CONTTag',
        'ContentID',
    ])
    content_conttag.to_csv(os.path.join(TABLES_PATH, 'CONTENT_CONTTag.csv'), index=False)

    playlist_playtag = pd.DataFrame(columns=[
        'PLAYTag',
        'PlayID',
    ])
    playlist_playtag.to_csv(os.path.join(TABLES_PATH, 'PLAYLIST_PLAYTag.csv'), index=False)

    short = pd.DataFrame(columns=[
        'SHMusicLink',
        'SHORTBody',
        'ContentID',
    ])
    short.to_csv(os.path.join(TABLES_PATH, 'SHORT.csv'), index=False)

if __name__ == "__main__":
    initialize_tables()
    print("Tables initialized successfully.")