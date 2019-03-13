from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Guitar, Practice
from .forms import PracticeForm

# Create your views here.
class GuitarCreate(CreateView):
    model = Guitar
    fields = '__all__'
    success_url = '/guitars/'    

class GuitarUpdate(UpdateView):
    model = Guitar
    fields = '__all__'

class GuitarDelete(DeleteView):
    model = Guitar
    success_url = '/guitars/'

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def guitars_index(request):
    guitars = Guitar.objects.all()
    return render(request, 'guitars/index.html', { 'guitars': guitars })

def guitars_detail(request, guitar_id):
    guitar = Guitar.objects.get(id=guitar_id)
    practice_form = PracticeForm()
    return render(request, 'guitars/detail.html', { 'guitar': guitar, 'practice_form': practice_form})

def add_practice(request, guitar_id):
    form = PracticeForm(request.POST)
    if form.is_valid():
        new_practice = form.save(commit=False)
        new_practice.guitar_id = guitar_id
        new_practice.save()
    return redirect('detail', guitar_id=guitar_id)



