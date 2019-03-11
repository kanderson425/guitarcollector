from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse('<h1>I freaking love guitars!</h1>')

def about(request):
    return render(request, 'about.html')

def guitars_index(request):
    return render(request, 'guitars/index.html', { 'guitars': guitars })

class Guitar:
    def __init__(self, name, brand, model, description):
        self.name = name
        self.brand = brand
        self.model = model
        self.description = description

guitars = [
    Guitar('White Lightning', 'Fender', 'Stratocaster', 'A great versatile strat!'),
    Guitar('The Red Devl', 'Gibson', 'SG', 'Great for chugging and summoning Satan'),
    Guitar('The Guitar my Girlfriend Prefers', 'Taylor', '214ce', 'A great acoustic guitar built to write songs my girlfriend will actually listen to'),
]
