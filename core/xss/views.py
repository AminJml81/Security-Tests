from django.shortcuts import render
from django.contrib.auth import get_user_model

# Create your views here.
from xss.models import Comment
from xss.forms import CommentForm


def xss_view(request):
    template = 'comment_form.html'
    context = {'form': CommentForm()}
    if request.method == "GET":
        return render(request, template, context=context)
        
    elif request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
        return render(request, template, context=context)
    
    