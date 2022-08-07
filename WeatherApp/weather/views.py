from django.shortcuts import render, redirect
import requests
from .models import City
from .forms import CityForm
from django.http import HttpResponse


def index(request):
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('info')
    else:
        form = CityForm
        context = {
            'form': form,
        }
        return render(request, 'weather/index.html', context)


def info(request):
    appid = '4c134bf1102a32bac429024a3b8cf39c'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&lang=ru&appid=' + appid

    cities = City.objects.order_by('-id')
    all_cities = []
    for city in cities:
        res = requests.get(url.format(city.name)).json()
        city_info = {
            'city': city.name,
            'temp': res['main']['temp'],
            'icon': res['weather'][0]['icon'],
            'speed': res['wind']['speed']
        }
        all_cities.append(city_info)
    context = {'all_info': all_cities}
    return render(request, 'weather/info.html', context)
