# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from .models import Game, Category, Comment
from .forms import GameForm, CommentForm

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

def game_list(request):
    games = Game.objects.all().annotate(comment_count=Count('comments'))
    categories = Category.objects.all()
    
    # Filtering
    category_slug = request.GET.get('category')
    difficulty = request.GET.get('difficulty')
    search = request.GET.get('search')
    
    if category_slug:
        games = games.filter(categories__slug=category_slug)
    if difficulty:
        games = games.filter(difficulty=difficulty)
    if search:
        games = games.filter(
            Q(title__icontains=search) | 
            Q(description__icontains=search) |
            Q(instructions__icontains=search)
        )
    
    context = {
        'games': games,
        'categories': categories,
        'selected_category': category_slug,
        'selected_difficulty': difficulty,
        'search_query': search,
    }
    return render(request, 'gamevault/game_list.html', context)

def game_detail(request, slug):
    game = get_object_or_404(Game, slug=slug)
    game.increment_views()
    comments = game.comments.select_related('author')
    
    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.game = game
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect('game_detail', slug=slug)
    else:
        form = CommentForm()
    
    context = {
        'game': game,
        'comments': comments,
        'form': form,
    }
    return render(request, 'gamevault/game_detail.html', context)

@login_required
def game_create(request):
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            game = form.save(commit=False)
            game.created_by = request.user
            game.save()
            form.save_m2m()
            messages.success(request, 'Game created successfully!')
            return redirect('game_detail', slug=game.slug)
    else:
        form = GameForm()
    
    return render(request, 'gamevault/game_form.html', {'form': form, 'action': 'Create'})

@login_required
def game_edit(request, slug):
    game = get_object_or_404(Game, slug=slug)
    
    if request.method == 'POST':
        form = GameForm(request.POST, instance=game)
        if form.is_valid():
            form.save()
            messages.success(request, 'Game updated successfully!')
            return redirect('game_detail', slug=game.slug)
    else:
        form = GameForm(instance=game)
    
    return render(request, 'gamevault/game_form.html', {'form': form, 'action': 'Edit', 'game': game})

# Auth views

def user_register(request):
    if request.user.is_authenticated:
        return redirect('game_list')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to SquadGames, {user.username}!')
            return redirect('game_list')
    else:
        form = UserCreationForm()
    
    return render(request, 'gamevault/register.html', {'form': form})

def user_login(request):
    if request.user.is_authenticated:
        return redirect('game_list')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                next_url = request.GET.get('next', 'game_list')
                return redirect(next_url)
    else:
        form = AuthenticationForm()
    
    return render(request, 'gamevault/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('game_list')