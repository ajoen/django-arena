from datetime import datetime
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from uuslug import slugify


class ForumCategory(models.Model):
    """Forum categories.

    Forum categories are used to group related forums.

    """
    name = models.CharField(_('name'), max_length=127,)
    slug = models.SlugField(_('slug'), max_length=146, unique=True,)
    order = models.IntegerField(_('order'), max_length=3, default=0,)
    created_at = models.DateTimeField(_('creation date'), auto_now_add=True,)
    updated_at = models.DateTimeField(_('change date'), auto_now=True,)

    class Meta:
        ordering = ['order']
        verbose_name = _('forum category')
        verbose_name_plural = _('forum categories')

    def __unicode__(self):
        return self.name


class Forum(models.Model):
    """Forums.

    Forums are used to store discussion threads.

    """
    STATUS_CHOICES = (
        ('P', _('Published')),
        ('U', _('Unpublished')),
    )
    category = models.ForeignKey(ForumCategory, verbose_name=_('category'), related_name='forums',)
    name = models.CharField(_('name'), max_length=127,)
    slug = models.SlugField(_('slug'), max_length=146, unique=True,)
    description = models.CharField(_('description'), max_length=127,)
    order = models.IntegerField(_('order'), max_length=3, default=0,)
    created_at = models.DateTimeField(_('creation date'), auto_now_add=True,)
    updated_at = models.DateTimeField(_('change date'), auto_now=True,)
    status = models.CharField(_('status'), max_length=1, choices=STATUS_CHOICES, default='U',)

    class Meta:
        verbose_name = _('forum')
        verbose_name_plural = _('forums')

    def __unicode__(self):
        return self.name

    def has_new_forum_posts(self, user):
        if not user:
            return True

        try:
            last_hit_of_user = ForumThreadHit.objects\
                .order_by('-created_at')\
                .filter(visitor=user, forum_thread__forum=self,)[:1]
            if last_hit_of_user:
                last_hit_of_user = last_hit_of_user[0]
                forum_posts_count = ForumPost.objects\
                    .filter(forum_thread__forum=self, created_at__gt=last_hit_of_user.created_at)\
                    .count()
            else:
                raise ForumThreadHit.DoesNotExist
        except ForumThreadHit.DoesNotExist:
            forum_posts_count = ForumPost.objects.filter(forum_thread__forum=self,).count()

        return forum_posts_count > 0

    def get_forum_posts_count(self):
        return ForumPost.objects.filter(forum_thread__forum=self,).count()

    def get_last_forum_post(self):
        last_forum_post = ForumPost.objects.filter(forum_thread__forum=self,).order_by('-id')[:1]
        if last_forum_post:
            return last_forum_post[0]
        else:
            return None


class ForumThread(models.Model):
    """Forum threads.

    Forum threads are discussion topics. Users post messages to these
    threads.

    """
    STATUS_CHOICES = (
        ('P', _('Published')),
        ('U', _('Unpublished')),
        ('L', _('Locked')),
    )
    TYPE_CHOICES = (
        ('N', _('Normal')),
        ('S', _('Sticky')),
        ('A', _('Announcement')),
    )
    forum = models.ForeignKey(Forum, verbose_name=_('forum'), related_name='forum_threads',)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('creator'), related_name='forum_threads',)
    visitors = models.ManyToManyField(settings.AUTH_USER_MODEL, through='ForumThreadHit',
                                      related_name='visited_forum_threads',)
    title = models.CharField(_('title'), max_length=127,)
    slug = models.CharField(_('slug'), max_length=150, unique=True,)
    created_at = models.DateTimeField(_('creation date'), auto_now_add=True,)
    updated_at = models.DateTimeField(_('change date'), auto_now=True,)
    last_post_date = models.DateTimeField(_('last post date'), blank=True, null=True,)
    status = models.CharField(_('status'), max_length=1, choices=STATUS_CHOICES, default='P',)
    thread_type = models.CharField(_('type'), max_length=1, choices=TYPE_CHOICES, default='N',)

    class Meta:
        ordering = ['-last_post_date', ]
        verbose_name = _('forum thread')
        verbose_name_plural = _('forum threads')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(ForumThread, self).save()

    def get_forum_posts(self, user):
        # flag the thread as read
        if user:
            forum_thread_hit = ForumThreadHit(visitor=user, forum_thread=self,)
        else:
            forum_thread_hit = ForumThreadHit(forum_thread=self,)
        forum_thread_hit.save()

        # return list of posts
        return self.forum_posts

    def get_last_forum_post(self):
        return self.forum_posts.all().order_by('-id')[0]

    @staticmethod
    def get_last_forum_threads_for_user():
        return ForumThread.objects.all().order_by('-id')[:5]

    def get_forum_posts_count(self):
        return self.forum_posts.count()

    def get_views_count(self):
        return self.hits.count()

    def has_new_forum_posts(self, user):
        if not user:
            return True

        # fetch the last hit time.
        last_hits = ForumThreadHit.objects.filter(visitor=user, forum_thread=self,).order_by('-id')

        if not last_hits:
            return True

        last_hit = last_hits[0]

        # fetch posts count made after last hit time.
        forum_posts_count = ForumPost.objects.filter(forum_thread=self, created_at__gt=last_hit.created_at).count()

        return forum_posts_count > 0


class ForumPost(models.Model):
    """Forum posts.

    Forum posts are user comments and each post is attached to a
    specific forum thread.

    """
    STATUS_CHOICES = (
        ('P', _('Published')),
        ('U', _('Unpublished')),
    )
    forum_thread = models.ForeignKey(ForumThread, verbose_name=_('forum thread'), related_name='forum_posts',)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('sender'), related_name='forum_posts',)
    content = models.TextField(_('content'),)
    ip_address = models.IPAddressField(_('ip address'),)
    user_agent = models.CharField(_('user agent'), max_length=255,)
    created_at = models.DateTimeField(_('creation date'), auto_now_add=True,)
    updated_at = models.DateTimeField(_('change date'), auto_now=True,)
    status = models.CharField(_('status'), max_length=1, choices=STATUS_CHOICES, default='P',)

    class Meta:
        verbose_name = _('forum post')
        verbose_name_plural = _('forum posts')

    def get_post_time(self):
        return self.created_at


def update_forum_thread_last_message_date(sender, instance=False, **kwargs):
    forum_thread = instance.forum_thread
    if forum_thread:
        forum_thread.last_post_date = datetime.now()
        forum_thread.save()
models.signals.post_save.connect(update_forum_thread_last_message_date, sender=ForumPost)


class ForumThreadHit(models.Model):
    """A user's forum thread visit history.

    Forum threads hits tell us when a user visited a forum thread. This
    information is used to determine which forums and forum threads
    have new messages since a user's last visit. Also, it's used in
    calculation of visits count for both forums and forum threads.

    """
    visitor = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('visitor'), null=True, blank=True,)
    forum_thread = models.ForeignKey(ForumThread, verbose_name=_('forum thread'), related_name='hits',)
    created_at = models.DateTimeField(_('creation date'), auto_now_add=True,)