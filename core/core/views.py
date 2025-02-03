from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.shortcuts import redirect

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


def homeview(request):
    return render(request, template_name='index.html')

def protected(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, template_name='protected_index.html')


class CustomLoginView(LoginView):

    def get_success_url(self):
        return reverse_lazy('index')
