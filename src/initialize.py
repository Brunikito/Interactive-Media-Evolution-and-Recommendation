'''Initialize the database with empty tables.'''

import numpy as np
import pandas as pd

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
    users.to_csv('data/users.csv', index=False)

    channels = pd.DataFrame(columns=[
        'channel_id',
        'channel_name',
        'channel_creation_date',
        'channel_description',
        'channel_language',
        'channel_location',
        'channel_category',
    ])
    channels.to_csv('data/channels.csv', index=False)

    content = pd.DataFrame(columns=[
        'content_id',
        'content_title',
        'content_description',
        'content_status'
        'content_category',
        'content_tags',
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
        'content_comments_count',
    ])
    content.to_csv('data/content.csv', index=False)

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
    comments.to_csv('data/comments.csv', index=False)

    user = pd.DataFrame(columns=[
        'UserID',
        'UserName',
        'UserEmail',
        'UserPassword',
        'UserPhoto',
    ])
    user.to_csv('data/tables/USER.csv', index=False)

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
    channel.to_csv('data/tables/CHANNEL.csv', index=False)

    uadminch = pd.DataFrame(columns=[
        'UserID',
        'ChannelID',
    ])
    uadminch.to_csv('data/tables/UADMINCH.csv', index=False)

    uinterestch = pd.DataFrame(columns=[
        'UisSubToCH',
        'UMemberLevelCH',
        'UisNotifiedByCH',
        'UserID',
        'ChannelID',
    ])
    uinterestch.to_csv('data/tables/UINTERESTCH.csv', index=False)

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
    content.to_csv('data/tables/CONTENT.csv', index=False)

    uwatchingcont = pd.DataFrame(columns=[
        'UWatchDurationCONT',
        'UWatchCONTDateTime',
        'UIsWatchingCONTNow',
        'UWATCHCONTID',
        'UserID',
        'ContentID',
    ])
    uwatchingcont.to_csv('data/tables/UWATCHINGCONT.csv', index=False)

    live = pd.DataFrame(columns=[
        'LIVEBody',
        'ContentID',
    ])
    live.to_csv('data/tables/LIVE.csv', index=False)

    video = pd.DataFrame(columns=[
        'VIDEOBody',
        'ContentID',
    ])
    video.to_csv('data/tables/VIDEO.csv', index=False)

    comment = pd.DataFrame(columns=[
        'CommentID',
        'COMDateTime',
        'COMisEdited',
        'COMBody',
        'UserID',
    ])
    comment.to_csv('data/tables/COMMENT.csv', index=False)

    livecomment = pd.DataFrame(columns=[
        'CommentID',
        'ContentID',
    ])
    livecomment.to_csv('data/tables/LIVECOMMENT.csv', index=False)

    commentreply = pd.DataFrame(columns=[
        'CommentID',
        'COMisRepByCOMCommentID',
    ])
    commentreply.to_csv('data/tables/COMMENTREPLY.csv', index=False)

    poll = pd.DataFrame(columns=[
        'POLLID',
        'POLLPubDateTime',
        'POLLURL',
        'POLLBody',
        'ChannelID',
    ])
    poll.to_csv('data/tables/POLL.csv', index=False)

    playlist = pd.DataFrame(columns=[
        'PlayID',
        'PlayURL',
        'PLAYTitle',
        'PLAYDesc',
        'PLAYStatus',
        'PLAYThumb',
        'ChannelID',
    ])
    playlist.to_csv('data/tables/PLAYLIST.csv', index=False)

    playlistcontent = pd.DataFrame(columns=[
        'CONTAddDateTimePL',
        'ContentID',
        'PlayID',
    ])
    playlistcontent.to_csv('data/tables/PLAYLISTCONTENT.csv', index=False)

    videocomment = pd.DataFrame(columns=[
        'CommentID',
        'ContentID',
    ])
    videocomment.to_csv('data/tables/VIDEOCOMMENT.csv', index=False)

    pollcomment = pd.DataFrame(columns=[
        'CommentID',
        'POLLID',
    ])
    pollcomment.to_csv('data/tables/POLLCOMMENT.csv', index=False)

    userinteraction = pd.DataFrame(columns=[
        'UINTType',
        'UINTID',
        'UserID',
    ])
    userinteraction.to_csv('data/tables/USERINTERACTION.csv', index=False)

    ucontint = pd.DataFrame(columns=[
        'UINTID',
        'ContentID',
    ])
    ucontint.to_csv('data/tables/UCONTINT.csv', index=False)

    ucomint = pd.DataFrame(columns=[
        'UINTID',
        'CommentID',
    ])
    ucomint.to_csv('data/tables/UCOMINT.csv', index=False)

    uplayint = pd.DataFrame(columns=[
        'UINTID',
        'PlayID',
    ])
    uplayint.to_csv('data/tables/UPLAYINT.csv', index=False)

    notification = pd.DataFrame(columns=[
        'NotificationID',
        'NOTBody',
        'ChannelID',
    ])
    notification.to_csv('data/tables/NOTIFICATION.csv', index=False)

    usernotified = pd.DataFrame(columns=[
        'NOTSentDateTime',
        'UserID',
        'NotificationID',
    ])
    usernotified.to_csv('data/tables/USERNOTIFIED.csv', index=False)

    channel_chextlink = pd.DataFrame(columns=[
        'CHExtLink',
        'ChannelID',
    ])
    channel_chextlink.to_csv('data/tables/CHANNEL_CHExtLink.csv', index=False)

    content_conttag = pd.DataFrame(columns=[
        'CONTTag',
        'ContentID',
    ])
    content_conttag.to_csv('data/tables/CONTENT_CONTTag.csv', index=False)

    playlist_playtag = pd.DataFrame(columns=[
        'PLAYTag',
        'PlayID',
    ])
    playlist_playtag.to_csv('data/tables/PLAYLIST_PLAYTag.csv', index=False)

    short = pd.DataFrame(columns=[
        'SHMusicLink',
        'SHORTBody',
        'ContentID',
    ])
    short.to_csv('data/tables/SHORT.csv', index=False)

    shortcomment = pd.DataFrame(columns=[
        'CommentID',
        'ContentID',
    ])
    shortcomment.to_csv('data/tables/SHORTCOMMENT.csv', index=False)

if __name__ == "__main__":
    initialize_tables()
    print("Tables initialized successfully.")