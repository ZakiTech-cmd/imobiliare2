from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from .models import *
from .forms import AnnounceForm
from .forms import CreateUserForm
from django.db.models import Q
from django.views.generic import ListView
from .tables import AnnounceTable
from django_tables2 import SingleTableView


# Create your views here.

class Home(View):
    def get(self, request):
        announces = Announce.objects.all()
        context = {'announces': announces}
        return render(request, 'imobiliare/home.html', context)


class AnnounceListView(SingleTableView):
    model = Announce
    table_class = AnnounceTable
    template_name = 'imobiliare/calculator.html'


class LoginPage(View):

    def get(self, request):
        context = {'page': 'login'}
        return render(request, 'imobiliare/sign-in.html', context)

    def post(self, request):
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Utilizator inexistent')
            return render(request, 'imobiliare/sign-in.html', {'page': 'login'})

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Nume utilizator sau parola gresita')


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('home')


class RegisterPage(View):
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')
    form_class = CreateUserForm
    success_message = "Your profile was created successfully"
    def get(self, request):
        form = CreateUserForm()
        return render(request, 'imobiliare/sign-up.html', {'page': 'register', 'form': form})

    def post(self, request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return render(request, 'imobiliare/home.html', {'form': form})
        else:
            messages.error(request, form.errors)
            return render(request, 'imobiliare/sign-up.html')


class AnnounceDetails(View):
    def get(self, request, id):
        announce = Announce.objects.get(id=id)
        photos = PostImage.objects.filter(announce=announce)
        context = {'announce': announce, 'photos': photos}
        return render(request, 'imobiliare/announce_details.html', context)


class MyAnnounces(View):
    def get(self, request):
        announces = Announce.objects.filter(creator=request.user)
        context = {'announces': announces, 'announces_no': len(announces)}
        return render(request, 'imobiliare/my_announces.html', context)


class CreateAnnounce(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'register/'

    def get(self, request):
        form = AnnounceForm()
        context = {"form": form}
        return render(request, 'imobiliare/create_announce.html', context)

    def post(self, request):
        form = AnnounceForm(request.POST, request.FILES)
        image = request.FILES.getlist('image')
        if form.is_valid():
            instance = form.save(commit=False)
            instance.creator = request.user
            instance.save()
            for img in image:
                PostImage.objects.create(image=img, announce=instance)
            return redirect('my_announces')
        else:
            messages.error(request, form.errors)
            return render(request, 'imobiliare/create_announce.html')


class UpdateAnnounce(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'register/'

    def get(self,request, id):
        announce = Announce.objects.get(id=id)
        form = AnnounceForm(instance=announce)
        if request.user != announce.creator and not request.user.is_superuser:
            return HttpResponse('Nu poti modifica acest anunt!')
        context = {
            'form': form,
            'announce': announce}
        return render(request, 'imobiliare/edit_announce.html', context)

    def post(self, request, id):
        try:
            announce = Announce.objects.get(id=id)
            form = AnnounceForm(request.POST, request.FILES, instance=announce)
            if form.is_valid():
                form.save()
                return redirect('home')
        except:
            messages.error(request, 'A aparut o erroare la salvarea anuntului!')
            return render(request, 'imobiliare/edit_announce.html')

#
# @login_required(login_url='login')
# def deleteAnnounce(request, id):
#     announce = Announce.objects.get(id=id)
#
#     if request.user != announce.creator and not request.user.is_superuser:
#         return HttpResponse('Nu poti sterge acest anunt!')
#
#     if request.method == 'POST':
#         announce.delete()
#         return redirect('home')
#
#     return render(request, 'imobiliare/delete.html', {'obj': announce})


class DeleteAnnounce(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'register/'

    def get(self, request, id):
        announce = Announce.objects.get(id=id)
        if request.user != announce.creator and not request.user.is_superuser:
            return HttpResponse('Nu poti sterge acest anunt!')
        return render(request, 'imobiliare/delete.html', {'obj': announce})

    def post(self, request, id):
        announce = Announce.objects.get(id=id)
        announce.delete()
        return redirect('home')


class SearchAnnounce(View):
    def post(self, request):
        search_text = request.POST.get('search_text')
        search_location = request.POST.get('search_location')
        announces = Announce.objects.filter((Q(title__contains=search_text) | Q(description__contains=search_text)) &
                                            (Q(county__contains=search_location) | Q(location__contains=search_location)))
        return render(request, 'imobiliare/home.html', {'announces': announces})


class Calculator(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'register/'
    def get(self, request):
        return render(request, 'imobiliare/calculator.html')