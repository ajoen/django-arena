# -*- coding: utf-8 -*-
from django import template
from ..models import ForumThread
register = template.Library()

@register.assignment_tag
def forum_thread_has_new_forum_posts(forum_thread, user):
    return forum_thread.has_new_forum_posts(user=user)

@register.assignment_tag
def forum_has_new_forum_posts(forum, user):
    return forum.has_new_forum_posts(user=user)

@register.assignment_tag
def get_last_forum_threads(user):
    return ForumThread.get_last_forum_threads_for_user(user)