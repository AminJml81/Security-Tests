from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.urls import reverse_lazy
from django.shortcuts import redirect

# Create your views here.
from .forms import CommentForm
from .models import Comment


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
    

def commentadd(request):
    template = 'comment_form.html'
    context = {'form': CommentForm()}
    if request.method == "GET":
        return render(request, template, context=context)
        
    elif request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
        return render(request, template, context=context)


class CommentDetail(LoginRequiredMixin, DetailView):
    model = Comment
    context_object_name = 'comment'
    template_name = 'template_detail.html'


    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)
    

    def get_object(self, queryset = ...):
        """
        Override to handle the case where the object doesn't exist or doesn't belong to the user.
        """
        queryset = self.get_queryset()
        pk = self.kwargs.get(self.pk_url_kwarg)

        try:
            comment = queryset.get(pk=pk)
            return comment
        except Comment.DoesNotExist:
            raise Http404("Comment not found or you do not have permission to view it.")


