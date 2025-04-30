from django.shortcuts import render
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_auth
from django.contrib.auth import logout as logout_auth
import re
from .models import *
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import Blog
from .forms import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Blog
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, redirect




# Create your views here.
def home(request):
    blogs_list = Blog.objects.all()
    paginator = Paginator(blogs_list, 3)  # 3 blogs per page

    page_number = request.GET.get('page')
    blogs = paginator.get_page(page_number)

    context = {
        'blogs': blogs
    }
    return render(request, 'index.html', context)

def about(request):
     return render(request, 'about.html')


@login_required(login_url='login')
def my_profile(request):
    blogs_list = Blog.objects.filter(user=request.user).order_by('-created_at')
    paginator = Paginator(blogs_list, 3)  # Show 3 blogs per page
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'my_profile.html', context)

def edit_blog(request, slug):
     blog=Blog.objects.get(slug=slug)
     if request.method == 'POST':
        print("Coming Here") # not printing when submitting form
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():  # FIXED: added parentheses
            blog = form.save()  # Create but don't save to DB yet
            blog.save()  # Now save to DB
            return redirect('my_profile')
     form = BlogForm(instance = blog)
     context = {
          'form': form
     }
     return render(request, 'edit_blog.html', context)


def delete_blog(request, slug):  # Make sure 'slug' parameter is here
    blog = Blog.objects.get(slug = slug)
    blog.delete()
    return redirect('my_profile')  # Or wherever you want to redirect

def blog_detail(request, slug):
     blog = Blog.objects.get(slug=slug)
     context = {
          'blog': blog
     }
     return render(request, 'blog.html', context)

def contact(request):
     return render(request, 'contact.html')



@login_required(login_url='login')
def create_blog(request):
    print("Request Method:", request.method)
    form = BlogForm()
    if request.method == 'POST':
        print("Coming Here") # not printing when submitting form
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():  # FIXED: added parentheses
            blog = form.save(commit=False)  # Create but don't save to DB yet
            blog.user = request.user  # Set the user
            blog.save()  # Now save to DB
            return redirect('home')
    context = {
        'form': form
    }
    return render(request, 'create_blog.html', context)


def login(request):
     if request.method == "POST":
          username = request.POST.get("username")
          pass1 = request.POST.get("password")

          print(username, pass1)
          user = authenticate(username=username, password=pass1)

          if user is not None:
               login_auth(request, user)
               return redirect('home')

          else:
               messages.error(request, "Bad Credentials")
               return redirect("home")

     return render(request, 'login.html')



@login_required(login_url='login')
def logout(request):
     logout_auth(request)
     messages.success(request,"Logged out")
     return redirect('login')


def signup(request):
     if request.method == "POST":
          username = request.POST.get("username")
          fname = request.POST.get("fname")
          lname = request.POST.get("lname")
          email = request.POST.get("email")
          pass1 = request.POST.get("pass1")
          pass2 = request.POST.get("pass2")

          if pass1 != pass2:
               return HttpResponse("Password and Confirm password is not matching")

          
          # if User.objects.filter(username=username).exists():
          #   return HttpResponse("Username already taken. Please choose a different one.")

     #    # Validate password
     #      if not is_valid_password(pass1):
     #           return HttpResponse("Password must contain at least 2 uppercase letters, 2 lowercase letters, and 2 digits.")


          myuser = User.objects.create_user(username, email, pass1)
          myuser.first_name = fname
          myuser.last_name = lname

          myuser.save()
          
          messages.success(request, "Your account is created")
          
          user = authenticate(username=username, password=pass1)


          if user is not None:
               login_auth(request, user)
               messages.success(request, "You are logged In")
               return redirect('home')
          else:
               redirect('signup')



     return render(request,"signup.html")


