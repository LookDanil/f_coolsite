from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, CreateView

from .forms import AddPostForm, AddUserForm, LoginuserForm

from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from .utils import *


class WomenHome(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = "posts"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_dic = self.get_user_context(title='Главная страница')
        return dict(list(context.items()) + list(c_dic.items()))

    def get_queryset(self):
        return Women.objects.filter(is_published=True)


def about(request):
    return render(request, 'women/about.html', {'menu': menu, 'title': 'О нас'})


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = "women/addpage.html"
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_dic = self.get_user_context(title='Добавление статьи')
        return dict(list(context.items()) + list(c_dic.items()))


def contact(request):
    return HttpResponse("Страница обратной связи")


def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


class ShowPost(DataMixin, DeleteView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = "post_slug"
    context_object_name = "post"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_dic = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_dic.items()))


class WomenCategory(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = "posts"
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_dic = self.get_user_context(title="Категория - " + str(context['posts'][0].cat_slug),
                                      cat_selected=self.kwargs[
                                          'cat_slug_id'])
        return dict(list(context.items()) + list(c_dic.items()))

    def get_queryset(self):
        return Women.objects.filter(cat_slug_id=self.kwargs['cat_slug_id'], is_published=True)


class RegisterUser(DataMixin, CreateView):
    form_class = AddUserForm
    template_name = "women/register.html"
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_dic = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_dic.items()))
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginuserForm
    template_name = "women/login.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_dic = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_dic.items()))

    def get_success_url(self):
        return reverse_lazy('home')

def logoutuser(request):
    logout(request)
    return redirect('login')