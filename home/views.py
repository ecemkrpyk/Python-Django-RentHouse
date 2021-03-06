import json
from unicodedata import category

from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.core.checks import messages
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
from apartment.models import Apartment, Category, Images, Comment
from home.forms import SearchForm, SignUpForm
from home.models import Setting, ContactForm, ContactFormMessage, UserProfile, FAQ
from django.contrib import messages


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = Apartment.objects.filter(status='True')[:4]  # 4 tane veri getirir
    category = Category.objects.all()
    userprofile=UserProfile.objects.get(user_id=request.user.id)
    dayapartments = Apartment.objects.filter(status='True')[:4]
    lastapartments = Apartment.objects.filter(status='True').order_by('-id')[:4]
    randomapartments = Apartment.objects.filter(status='True').order_by('?')[:4]

    context = {'setting': setting,
               'category': category,
               'userprofile':userprofile,
               'page': 'home',
               'sliderdata': sliderdata,
               'dayapartments': dayapartments,
               'lastapartments': lastapartments,
               'randomapartments': randomapartments,

               }
    return render(request, 'index.html', context)


def hakkimizda(request):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    context = {'category':category,
               'setting': setting}
    return render(request, 'hakkimizda.html', context)


def referanslar(request):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    context = {'category':category,
             'setting': setting}
    return render(request, 'referanslarımız.html', context)


def iletisim(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactFormMessage()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')  # clientın ip'sini alma
            data.save()  # veritabanına kaydet

            messages.success(request, "Mesajınız başarı ile gönderilmiştir. Teşekkür ederiz")  # flash mesaj
            return HttpResponseRedirect('/iletisim')

    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    form = ContactForm()
    context = {'category':category,'setting': setting, 'form': form}
    return render(request, 'iletisim.html', context)


def category_apartments(request, id, slug):
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    apartments = Apartment.objects.filter(category_id=id,status='True')

    context = {'apartments': apartments,
               'category': category,
               'categorydata': categorydata
               }
    return render(request, 'apartments.html', context)


def apartment_detail(request, id, slug):
    category = Category.objects.all()
    apartment = Apartment.objects.get(pk=id)
    images = Images.objects.filter(apartment_id=id)
    comments = Comment.objects.filter(apartment_id=id, status='True')
    context = {'apartment': apartment,
               'category': category,
               'images': images,
               'comments': comments,
               }
    return render(request, 'apartment_detail.html', context)  # fonksiyonu çağırma


def apartment_search(request):
    if request.method == 'POST':  # form post edildiyse
        form = SearchForm(request.POST)
        if form.is_valid():
            category = Category.objects.all()
            query = form.cleaned_data['query']  # veriyi aldık
            catid = form.cleaned_data['catid']

            if catid == 0:
                apartments = Apartment.objects.filter(title__icontains=query)
            else:
                apartments = Apartment.objects.filter(title__icontains=query, category_id=catid)

            context = {'apartments': apartments,
                       'category': category,
                       }
            return render(request, 'apartment_search.html', context)

        return HttpResponseRedirect('/')


def apartment_search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')  # query
        apartments = Apartment.objects.filter(title__icontains=q)

        results = []
        for rs in apartments:
            apartment_json = {}
            apartment_json = rs.title
            results.append(apartment_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def login_view(request):
    if request.method == 'POST':  # post varsa login işlemi gerçekleşir
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')

        else:
            messages.warning(request, "Login Hatası! Kullanıcı adı ya da şifre yanlış")
            return HttpResponseRedirect('/login')

    category = Category.objects.all()
    context = {'category': category,
               }
    return render(request, 'login.html', context)


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)

            current_user=request.user
            data=UserProfile()
            data.user_id=current_user.id
            data.image="images/users/user.png" #default resim
            data.save()
            messages.success(request,"Hoş Geldiniz..Sitemize başarılı bir şekilde üye oldunuz.")
            return HttpResponseRedirect('/')  # kayıt olduktan sonra anasayfaya gönderiyoruz

    form = SignUpForm()
    category = Category.objects.all()
    context = {'category': category,
               'form': form,
               }
    return render(request, 'signup.html', context)


def faq(request):
    category=Category.objects.all()
    faq=FAQ.objects.all().order_by('ordernumber')
    context={
        'category': category,
        'faq':faq,
    }

    return  render(request, 'faq.html', context)



















