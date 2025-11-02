from django.shortcuts import render,redirect,get_object_or_404
from .models import Meme,Giphy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
# Create your views here.

def home(request):
    photos = Meme.objects.all()
    return render(request,'home.html',{'photos': photos})

def about(request):
    return render(request,"about.html")
    
    
def gippy(request):
    gipp = Giphy.objects.all()
    return render(request,'gippy.html',{'gipp':gipp})


def trending_meme(request):
    photos = Meme.objects.all().order_by('-likes') 
    return render(request,'trending.html',{'photos': photos})

def like_meme(request,meme_id):
    meme =get_object_or_404(Meme,id=meme_id)
    meme.likes +=1
    meme.save()
    return redirect('home')

def like_giphy(request, giphy_id):
    if request.method == "POST":
        giphy = get_object_or_404(Giphy, id=giphy_id)
        giphy.likes += 1
        giphy.save()
    return redirect('gippy')  # Or wherever you want to redirect


def search(request):
    query = request.GET.get('q')
    memes = []
    giphys = []
    
    if query:
        memes = Meme.objects.filter(title__icontains=query)
        giphys = Giphy.objects.filter(title__icontains=query)

    return render(request, "search.html", {
        "query": query,
        "memes": memes,
        "giphys": giphys
    })

from django.contrib.auth import authenticate, login, logout

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f"😂 Hello {username}, you are logged in!")
            return redirect("home")
        else:
            messages.error(request, "😅 Invalid username or password!")
    return render(request, "login.html")



def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Auto login after registration
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, f"😂 Welcome {username}! You are now logged in.")
            return redirect("home")
        else:
            messages.error(request, "😅 Something went wrong. Check username/password!")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("home")