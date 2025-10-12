from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.views.generic import ListView
from django.db import transaction
from .models import User, LocalGuide
from .forms import SignUpForm, UserProfileForm, LocalGuideForm


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'accounts/login.html')


def user_logout(request):
    logout(request)
    return redirect('home')


def user_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('accounts:login')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})


# Fixed Admin-only guide management views
@staff_member_required
def guide_create(request):
    if request.method == 'POST':
        form = LocalGuideForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Create user first
                    user = User.objects.create(
                        username=form.cleaned_data['user_username'],
                        email=form.cleaned_data['user_email'],
                        first_name=form.cleaned_data['user_first_name'],
                        last_name=form.cleaned_data['user_last_name'],
                    )

                    # Create guide profile
                    guide = form.save(commit=False)
                    guide.user = user
                    guide.save()

                    messages.success(request, f'Guide profile created for {user.get_full_name()}!')
                    return redirect('accounts:guide_detail', pk=guide.pk)
            except Exception as e:
                messages.error(request, f'Error creating guide: {str(e)}')
    else:
        form = LocalGuideForm()

    return render(request, 'accounts/guide_form.html', {
        'form': form,
        'title': 'Create New Guide'
    })


@staff_member_required
def guide_update(request, pk):
    guide = get_object_or_404(LocalGuide, pk=pk)

    if request.method == 'POST':
        form = LocalGuideForm(request.POST, request.FILES, instance=guide)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Update user information
                    user = guide.user
                    user.username = form.cleaned_data['user_username']
                    user.email = form.cleaned_data['user_email']
                    user.first_name = form.cleaned_data['user_first_name']
                    user.last_name = form.cleaned_data['user_last_name']
                    user.save()

                    # Update guide profile
                    form.save()

                    messages.success(request, f'Guide profile updated for {user.get_full_name()}!')
                    return redirect('accounts:guide_detail', pk=guide.pk)
            except Exception as e:
                messages.error(request, f'Error updating guide: {str(e)}')
    else:
        form = LocalGuideForm(instance=guide)

    return render(request, 'accounts/guide_form.html', {
        'form': form,
        'title': f'Update Guide: {guide.user.get_full_name()}'
    })


@staff_member_required
def guide_delete(request, pk):
    guide = get_object_or_404(LocalGuide, pk=pk)

    if request.method == 'POST':
        guide_name = guide.user.get_full_name()
        user = guide.user
        guide.delete()
        user.delete()  # Also delete the user account
        messages.success(request, f'Guide profile for {guide_name} has been deleted.')
        return redirect('accounts:guide_list')

    return render(request, 'accounts/guide_confirm_delete.html', {'guide': guide})


# Public views for users
class GuideListView(ListView):
    model = LocalGuide
    template_name = 'accounts/guide_list.html'
    context_object_name = 'guides'
    paginate_by = 12

    def get_queryset(self):
        return LocalGuide.objects.filter(is_verified=True).order_by('-rating', '-created_at')


def guide_detail(request, pk):
    guide = get_object_or_404(LocalGuide, pk=pk)
    reviews = []  # You can add guide reviews later
    context = {
        'guide': guide,
        'reviews': reviews
    }
    return render(request, 'accounts/guide_detail.html', context)