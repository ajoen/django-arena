from django.conf.urls import patterns, include, url
from django.utils.translation import ugettext_lazy as _

urlpatterns = patterns('arena.views',
    url(r'^/?$', 'forums', name='forums'),
    url(_(r'^(?P<forum_slug>.+)/new/?$'), 'new_forum_thread', name='new_forum_thread'),
    url(r'^(?P<forum_slug>.+)/(?P<forum_thread_slug>.+)/?$', 'forum_thread', name='forum_thread'),
    url(r'^(?P<forum_slug>.+)/?$', 'forum', name='forum'),
)