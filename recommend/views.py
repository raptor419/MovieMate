import sys

import djongo
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.http import Http404
from .models import Movie, UserRating
from django.contrib import messages
from .forms import UserForm
from django.db.models import Case, When
from .matrixfactor import MFRecommender
import numpy as np
import pandas as pd


# for recommendation
def recommend(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if not request.user.is_active:
        raise Http404
    df = pd.DataFrame(list(UserRating.objects.all().values()))
    print(df,file=sys.stderr)
    nu = df.user.unique().shape[0]
    current_user_id = request.user.id
    # if new user not rated any movie
    if current_user_id > nu:
        movie = Movie.objects.get(id=1)
        ratingObject = UserRating()
        ratingObject.hashid = str(request.user.id) + "_" + str(movie.id)
        ratingObject.user = str(request.user.id)
        ratingObject.movie = str(movie.id)
        ratingObject.rating = 0
        try:
            ratingObject.save()
            messages.success(request, "Your Rating is submited ")
        except djongo.sql2mongo.SQLDecodeError:
            print("Handle Error")
            messages.success(request, "You had already rated the movie")

    print("Current user id: ", current_user_id)
    prediction_matrix, Ymean = MFRecommender()
    predictions = prediction_matrix[:, current_user_id - 1] + Ymean.flatten()
    pred_idxs_sorted = np.argsort(predictions)
    pred_idxs_sorted[:] = pred_idxs_sorted[::-1]
    pred_idxs_sorted = pred_idxs_sorted + 1
    print(pred_idxs_sorted)
    # preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(pred_idxs_sorted)])
    # print(preserved)
    movie_list = list(Movie.objects.filter(id__in=pred_idxs_sorted, ))
    return render(request, 'recommend/recommend.html', {'movie_list': movie_list})
    # return render(request, 'recommend/recommend.html', {'movie_list': None})


# List view
def index(request):
    movies = Movie.objects.all()
    query = request.GET.get('q')
    if query:
        movies = Movie.objects.filter(Q(title__icontains=query)).distinct()
        return render(request, 'recommend/list.html', {'movies': movies})
    return render(request, 'recommend/list.html', {'movies': movies})


# detail view
def detail(request, movie_id):
    if not request.user.is_authenticated:
        return redirect("login")
    if not request.user.is_active:
        raise Http404
    movies = get_object_or_404(Movie, id=movie_id)
    # for rating
    if request.method == "POST":
        rate = request.POST['rating']
        ratingObject = UserRating()
        ratingObject.hashid = str(request.user.id)+"_"+str(movies.id)
        ratingObject.user = str(request.user.id)
        ratingObject.movie = str(movies.id)
        ratingObject.rating = rate
        try:
            ratingObject.save()
            messages.success(request, "Your Rating is submited ")
        except djongo.sql2mongo.SQLDecodeError:
            messages.success(request, "You had already rated the movie")

        return redirect("index")
    return render(request, 'recommend/detail.html', {'movies': movies})


# Register user
def signUp(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("index")
    context = {
        'form': form
    }
    return render(request, 'recommend/signUp.html', context)


# Login User
def Login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("index")
            else:
                return render(request, 'recommend/login.html', {'error_message': 'Your account disable'})
        else:
            return render(request, 'recommend/login.html', {'error_message': 'Invalid Login'})
    return render(request, 'recommend/login.html')


# Logout user
def Logout(request):
    logout(request)
    return redirect("login")
