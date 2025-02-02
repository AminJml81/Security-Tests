from django.shortcuts import render

# Create your views here.
from .forms import CommentForm


def view(request):
    template = 'comment_form.html'
    context = {'form': CommentForm()}
    if request.method == "GET":
        return render(request, template, context=context)
        
    elif request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
        return render(request, template, context=context)
    