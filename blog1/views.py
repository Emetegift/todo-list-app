from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Task 
# from django.http import HttpResponse

# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'blog1/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')
    
class RegisterPage(FormView):
    template_name = 'blog1/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('tasks')  
    
    # To redirect the user once the registration form is submitted
    def  form_valid(self, form):
        user = form.save()
        if user is not None: # This means if the user was successfully created
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)  

    def get(self,*args,**kwargs): # keyword arguments
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)

#TaskList is used to check all tasks
class TaskList(LoginRequiredMixin, ListView):
   model = Task
   context_object_name = 'tasks'

   #to make a user only have access to his/her page without seeing others contents

   def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context['tasks'] = context['tasks'].filter(user=self.request.user)
       context['count'] = context['tasks'].filter(complete=False).count()

    # To make the search area work
       search_input = self.request.GET.get('search-area') or ''
       if search_input:
           context['tasks'] = context['tasks'].filter(title__startswith=search_input)
       
       context['search_input'] = search_input
       
       return context

#DetailView is used to check info about a specific task 
class TaskDetail (LoginRequiredMixin, DetailView):
   model = Task
   context_object_name = 'task'
   template_name = 'blog1/task.html'

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task  
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')

#to over ride a method called form valid
    def form_valid(self, form):
        form.instance.user= self.request.user
        return super(TaskCreate, self).form_valid(form)
    
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')

