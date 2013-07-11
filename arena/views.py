from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django.views.decorators.http import require_http_methods
from .forms import ForumPostForm, ForumThreadForm
from .models import ForumCategory, Forum, ForumThread
from .utils import add_client_data, add_user_to_post_data


@require_http_methods(['GET', ])
def forums(request):
    """Lists forums grouped by categories.

    In the view function, all forum categories are fetched and passed
    to the template for rendering. In django-arena, a forum can be
    unpublished by the staff; meaning that it's possible to list only
    published forums. To accomplish that, ``Forum``'s manager supports
    filtering published/unpublished forums. Please note that it's
    template's job to fetch published forums from a category.

    To filter unpublished posts and fetch published one, do the
    following:

    {% for forum_category in forum_categories %}
        {% for forum in forum_category.published_forums.all %}
            ...
        {% endfor %}
    {% endfor %}

    """
    forum_categories = ForumCategory.objects.order_by('order')
    return render_to_response('arena/forums.html', {
        'forum_categories': forum_categories,
        'logged_in_user': request.user
    }, context_instance=RequestContext(request))


@require_http_methods(['GET', ])
def forum(request, forum_slug):
    """Lists threads in a published forum.

    Fetches forum record from the database, only if found via slug and
    is published.

    """
    forum = get_object_or_404(Forum, slug=forum_slug, status='P',)
    return render_to_response('arena/forum.html', {
        'forum': forum,
        'logged_in_user': request.user
    }, context_instance=RequestContext(request))


@require_http_methods(['GET', 'POST', ])
def forum_thread(request, forum_slug, forum_thread_slug):
    forum_thread = get_object_or_404(ForumThread, forum__slug=forum_slug, slug=forum_thread_slug)
    form = ForumPostForm()
    if request.POST:
        if not request.user.is_authenticated():
            return redirect_to_login(reverse('arena:forum_thread', kwargs={
                'forum_slug': forum_slug,
                'forum_thread_slug': forum_thread_slug
            }))
        form = ForumPostForm(add_client_data(request, add_user_to_post_data(request, 'sender')),)
        if form.is_valid():
            form.save()
            return redirect('arena:forum_thread', forum_slug=forum_slug, forum_thread_slug=forum_thread_slug)
    forum_posts = forum_thread.get_forum_posts(user=request.user,).all()
    return render_to_response('arena/forum_thread.html', {
        'forum_thread': forum_thread,
        'forum_posts': forum_posts,
        'form': form,
        'logged_in_user': request.user
    }, context_instance=RequestContext(request))

@login_required
@require_http_methods(['GET', 'POST', ])
def new_forum_thread(request, forum_slug):
    forum = get_object_or_404(Forum, slug=forum_slug,)
    form = ForumThreadForm()
    if request.POST:
        form = ForumThreadForm(add_client_data(request, add_user_to_post_data(request, 'creator')),)
        if form.is_valid():
            forum_thread = form.save()
            return redirect('arena:forum_thread', forum_slug=forum_slug, forum_thread_slug=forum_thread.get_slug())
    return render_to_response('arena/new_forum_thread.html', {
        'forum': forum,
        'form': form,
        'logged_in_user': request.user
    }, context_instance=RequestContext(request))