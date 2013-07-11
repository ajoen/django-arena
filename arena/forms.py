from django import forms
from django.contrib.auth import get_user_model
from django.db import transaction
from .models import Forum, ForumThread, ForumPost


# TODO: Add transaction and try/catch blocks
class ForumThreadForm(forms.Form):
    forum = forms.ModelChoiceField(queryset=Forum.objects.all())
    creator = forms.ModelChoiceField(queryset=get_user_model().objects.all())
    title = forms.CharField(max_length=127,)
    content = forms.CharField(widget=forms.Textarea)
    ip_address = forms.CharField(max_length=20,)
    user_agent = forms.CharField(max_length=255,)

    def save(self):
        with transaction.commit_on_success():
            forum_thread = ForumThread()
            forum_thread.forum = self.cleaned_data['forum']
            forum_thread.creator = self.cleaned_data['creator']
            forum_thread.title = self.cleaned_data['title']
            forum_thread.save()

            # then, create the post.
            post = ForumPost()
            post.forum_thread = forum_thread
            post.sender = forum_thread.creator
            post.content = self.cleaned_data['content']
            post.ip_address = self.cleaned_data['ip_address']
            post.user_agent = self.cleaned_data['user_agent']
            post.save()

        # return the forum thread.
        return forum_thread


class ForumPostForm(forms.ModelForm):
    class Meta:
        model = ForumPost
        exclude = ['status',]