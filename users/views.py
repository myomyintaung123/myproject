from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile  # Import the Profile model


# Create your views here.

def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username is already taken. Please choose a different username.")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email is already registered. Please use a different email address.")
            else:
                form.save()
                messages.success(request, "Registration successful. You can now log in.")
                return redirect("users:login")
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {"form": form})




def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username.capitalize()}.")

                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                else:
                    return redirect("/")  # Redirect to the desired page after login
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {"form": form})



def logout_view(request):
    if request.method == "POST":
        messages.success(request, f'Goodbye, {request.user.username}! You have been logged out.')
        logout(request)
        return redirect("users:login")


@login_required(login_url='/users/login/')
def profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    #posts = Post.objects.filter(author=user)  # Fetch posts by the user
    profile = user.profile  # assuming you have a OneToOne relationship with User

    # Check if the current user is the profile owner
    # if request.user != user:
    #     messages.error(request, 'You are not authorized to edit this profile.')
    #     return redirect('users:profile', username=request.user.username)

    if request.user == user:
        if request.method == "POST":
            u_form = UserUpdateForm(request.POST, instance=request.user)
            p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
            
            if u_form.is_valid() and p_form.is_valid():

                # this is remove profile then left default.jpg
                if p_form.cleaned_data.get('remove_image'):
                    if profile.image and profile.image.url != 'profile_pics/default.jpg':
                        profile.image.delete(save=False)  # Delete the image file from the storage
                    profile.image = 'profile_pics/default.jpg'  # Reset to default image
                    profile.save()

                else:
                    u_form.save()
                    p_form.save()
                messages.success(request, 'Your account has been updated!')
                return redirect('/', username=user.username)
        else:
            u_form = UserUpdateForm(instance=request.user)
            p_form = ProfileUpdateForm(instance=request.user.profile)
    
    else:
        u_form = None
        p_form = None
        
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'profile': profile,
        'user': user
    }

    # context = {
    #     'profile_user': user,
    #     'profile': profile,
    #     'is_owner': request.user == user,
    #     'u_form': u_form,
    #     'p_form': p_form,
    #     'posts': posts,  # Add posts to the context
    # }
    return render(request, 'users/profile.html', context)

    #return render(request, 'users/profile.html', {'profile': profile, 'user': user})
    #return render(request, 'users/profile.html')