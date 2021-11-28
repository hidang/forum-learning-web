from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from accounts.models import Profile
from questions.models import Question
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.


def signup_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            user = User.objects.get(username=username)
            # sau khi tạo user, tạo thêm profile mặc định cho user
            b = Profile(user=user)
            b.save()
            messages.success(
                request, f'Your account has been created! You are now able to log in')
            return redirect('accounts:accounts_login')
    else:
        form = UserRegisterForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('question_list')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('question_list')


@login_required
def profile_me(request):
    questions = []
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('accounts:accounts_profile_me')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        questions = request.user.question_set.all()

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'questions': questions
    }

    return render(request, 'profile_me.html', context)


def profile_user(request, username):
    user = User.objects.get(username=username)
    questions = user.question_set.all()

    context = {
        'user': user,
        'questions': questions
    }

    return render(request, 'profile_user.html', context)
