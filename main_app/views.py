from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView 
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PracticeForm
import uuid
import boto3
from .models import Guitar, Amp, Photo

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'guitarcollectorkja'

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('home')
    else:
      error_message = 'Invalid credentials - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

class GuitarCreate(LoginRequiredMixin, CreateView):
    model = Guitar
    fields = ['name', 'make', 'model', 'description']
    success_url = '/guitars/'   
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form) 

class GuitarUpdate(LoginRequiredMixin,UpdateView):
    model = Guitar
    fields = ['name', 'make', 'model', 'description']

class GuitarDelete(LoginRequiredMixin,DeleteView):
    model = Guitar
    success_url = '/guitars/'

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def guitars_index(request):
    guitars = Guitar.objects.filter(user=request.user)
    return render(request, 'guitars/index.html', { 'guitars': guitars })

@login_required
def guitars_detail(request, guitar_id):
    guitar = Guitar.objects.get(id=guitar_id)
    amps_guitar_doesnt_have = Amp.objects.exclude(id__in = guitar.amps.all().values_list('id'))
    practice_form = PracticeForm()
    return render(request, 'guitars/detail.html', { 
        'guitar': guitar, 
        'practice_form': practice_form,
        'amps': amps_guitar_doesnt_have
    })

@login_required
def add_practice(request, guitar_id):
    print('hello')
    form = PracticeForm(request.POST)
    if form.is_valid():
        new_practice = form.save(commit=False)
        new_practice.guitar_id = guitar_id
        new_practice.save()
    else:
        msg = 'Errors: %s' % form.errors.as_text()
        print(msg)  
    return redirect('detail', guitar_id=guitar_id)

@login_required
def add_photo(request, guitar_id):
	# photo-file was the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # we can assign to cat_id or cat (if you have a cat object
            photo = Photo(url=url, guitar_id=guitar_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', guitar_id=guitar_id)

class AmpList(LoginRequiredMixin, ListView):
    model = Amp

class AmpDetail(LoginRequiredMixin, DetailView):
    model = Amp

class AmpCreate(LoginRequiredMixin, CreateView):
    model = Amp
    fields = '__all__'

class AmpUpdate(LoginRequiredMixin, UpdateView):
    model = Amp 
    fields = '__all__'

class AmpDelete(LoginRequiredMixin, DeleteView):
    model = Amp 
    success_url = '/amps/'

@login_required
def assoc_amp(request, guitar_id, amp_id):
    Guitar.objects.get(id=guitar_id).amps.add(amp_id)
    return redirect('detail', guitar_id=guitar_id)

@login_required
def unassoc_amp(request, guitar_id, amp_id):
    Guitar.objects.get(id=guitar_id).amps.remove(amp_id)
    return redirect('detail', guitar_id=guitar_id)


