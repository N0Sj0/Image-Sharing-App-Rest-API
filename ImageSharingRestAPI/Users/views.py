from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.http import JsonResponse
from django.contrib.auth import authenticate
from .serializers import UserSerializer
from PIL import Image
from django.conf import settings
from constants import Constants as const
from Search import views as search_views
import json
import os
from utils import request_to_dict, get_user_data_from_usernames
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from .models import Profile
from rest_framework.exceptions import ValidationError, ParseError
import utils
import django

# Create your views here.


def create_user(username, password):
    if User.objects.filter(username=username).exists():
        return None

    user = User.objects.create_user(username)
    user.set_password(password)
    user.profile.username = user.username
    user.profile.save()
    user.save()
    search_views.add_user_to_search(username)
    return user


class UserViewSet(ModelViewSet):

    def retrieve(self, request, pk=None, *args, **kwargs):
        try:
            user = User.objects.get(username=pk)
            serializer = UserSerializer(user.profile)
            return JsonResponse(serializer.data)
        except User.DoesNotExist:
            return JsonResponse({"error_message": "Could not find user"}, status=404)

    def update(self, request, pk=None, *args, **kwargs):
        json_dict = request_to_dict(request)
        username = json_dict["username"]
        password = json_dict["password"]
        try:
            user = authenticate(username=username, password=password)
        except AttributeError:
            return JsonResponse({"error_message": "Wrong username or password"}, status=401)
        else:
            if json_dict["bio"] is not None:
                user.profile.bio = json_dict["bio"]
            if json_dict["firstname"] is not None:
                user.profile.firstname = json_dict["firstname"]
            if json_dict["lastname"] is not None:
                user.profile.lastname = json_dict["lastname"]

            user_serializer = UserSerializer(user.profile)
            user.profile.save()
            return JsonResponse(user_serializer.data)

    def create(self, request, *args, **kwargs):
        json_dict = request_to_dict(request)
        try:
            username = json_dict["username"]
            password = json_dict["password"]
            firstname = json_dict["first_name"]
            lastname = json_dict["last_name"]
            new_user = create_user(username, password)
            new_user.profile.bio = "This user has not created a bio yet"
            # successfully Created a user
            userserializer = UserSerializer(new_user.profile)
            return JsonResponse(userserializer.data)
        except AttributeError:
            return JsonResponse({"error_message": "Username not available"}, status=401)

    @action(methods=["post"], detail=True)
    def profile_image(self, request, pk=None):
        json_dict = utils.request_file_to_dict(request)

        username = pk
        password = json_dict["password"]

        user = authenticate(username=username, password=password)

        image = Image.open(request.FILES["profileImage"])
        path = os.path.join(settings.PROFILEPIC_ROOT, user.username + ".png")
        image.save(path)

        serializer = UserSerializer(user.profile)

        return JsonResponse(serializer.data)

    @action(methods=['get'], detail=True)
    def follows(self, request, pk=None):
        try:
            username = pk
            user = User.objects.get(username=username)
            follows = get_user_data_from_usernames(user.profile.follows_string.split(','))
            return JsonResponse(follows, safe=False)
        except User.DoesNotExist:
            return JsonResponse({"error_message": "Could not find user"}, status=404)

    @action(methods=['get'], detail=True)
    def followers(self, request, pk=None):
        username = pk
        try:
            user = User.objects.get(username=username)
            followers = get_user_data_from_usernames(user.profile.followers_string.split(','))
            return JsonResponse(followers, safe=False)
        except User.DoesNotExist:
            return JsonResponse({"error_message": "Could not find user"}, status=404)

    @action(methods=['get'], detail=True)
    def posts(self, request, pk=None):
        username = pk
        owner = request.GET.get("owner")

        posts, _ = utils.get_posts_from([owner], username)

        return JsonResponse(posts, safe=False, status=200)


class LoginView(APIView):

    def post(self, request):
        json_dict = request_to_dict(request)

        username = json_dict["username"]
        password = json_dict["password"]
        try:
            user = authenticate(username=username, password=password)
            user_serializer = UserSerializer(user.profile)

            return JsonResponse(user_serializer.data)
        except AttributeError:
            # no user
            return JsonResponse({"error_message": "Could not find user"}, status=404)


class FollowUserView(APIView):

    # returns if user follows specified user
    def get(self, request):
        username = request.GET.get('user')
        specified_username = request.GET.get('specified_user')
        try:
            user = User.objects.get(username=username)
            follows_list = user.profile.follows_string.split(',')
            follows = specified_username in follows_list
            return JsonResponse({"follows": str(follows)})
        except User.DoesNotExist:
            return JsonResponse({"error_message": "Could not find user"}, status=404)

    def post(self, request):
        json_dict = request_to_dict(request)

        username = json_dict["username"]
        password = json_dict["password"]

        user_to_follow_username = json_dict["user_to_follow"]
        try:
            user = authenticate(username=username, password=password)
            user_to_follow = User.objects.get(username=user_to_follow_username)
        except User.DoesNotExist:
            return JsonResponse({"error_message": "Could not find user"}, status=404)

        if user_to_follow_username not in user.profile.follows_string:
            # does not follow
            user.profile.follows_string += user_to_follow_username + ","
            user_to_follow.profile.followers_string += username + ","
            user.profile.follows_count += 1
            user_to_follow.profile.followers_count += 1
            user.profile.save()
            user_to_follow.profile.save()
        else:
            # follows, need to unfollow
            user.profile.follows_string = utils.remove_username_from_string(user.profile.follows_string,
                                                                      user_to_follow_username)
            user_to_follow.profile.followers_string = utils.remove_username_from_string(
            user_to_follow.profile.followers_string, user.profile.username)

            user.profile.follows_count -= 1
            user_to_follow.profile.followers_count -= 1
            user_to_follow.profile.save()
            user.profile.save()

        userserializer = UserSerializer(user.profile)

        return JsonResponse(userserializer.data)
