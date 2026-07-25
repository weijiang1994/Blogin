"""
# coding:utf-8
Models package — re-exports all model classes for backward compatibility.

Import order matters: core infrastructure models first, then dependent ones.
"""
# Infrastructure (no inter-model dependencies)
from blogin.models.mixins import TimeMixin, Mixin  # noqa: F401
from blogin.models.core import States, Role, ThirdParty  # noqa: F401
from blogin.models.statistics import BaseStatistics, VisitStatistics, CommentStatistics, LikeStatistics  # noqa: F401

# User (depends on core)
from blogin.models.user import User, LoginLog, Notification, VerifyCode  # noqa: F401

# Blog (depends on core + user relationships via strings)
from blogin.models.blog import (  # noqa: F401
    BlogType, Blog, BlogComment, BlogHistory, BlogBanner,
    PostContent, DraftBlog, Contribute, ContributeDetail,
    Plan, LoveMe, LoveInfo, update_contribution,
)

# Photo (depends on user relationships via strings)
from blogin.models.photo import Tag, tagging, Photo, PhotoComment, LikePhoto  # noqa: F401

# Poetry
from blogin.models.poetry import Dynasty, Poet, Poem, SongCiAuthor, SongCi  # noqa: F401

# Miscellaneous
from blogin.models.misc import Soul, Timeline, FriendLink, One, OneSentence, MessageBorder  # noqa: F401
