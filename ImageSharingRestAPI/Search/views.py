from django.shortcuts import render
from Users.serializers import UserSerializer
from rest_framework.views import APIView
from django.contrib.auth.models import User
from constants import Constants as const
from django.http import JsonResponse
from django.contrib.auth import authenticate
import json
from PIL import Image
from django.conf import settings
import os
from .models import SearchNode
# Create your views here.


def request_to_dict(request):
    raw_data = str(request.body)
    json_string = raw_data[2:len(raw_data) - 1]
    json_dict = json.loads(json_string)

    return json_dict


def add_user_to_search(username):

    username = username.lower()
    if SearchNode.objects.filter(val="").exists():
        # it exists a root node
        root_node = SearchNode.objects.get(val="")
        root_node.usernames += username + ","
        root_node.save()
    else:
        # create a root node
        root_node = SearchNode(val="", usernames="")
        root_node.usernames += username + ","
        root_node.save()

    temp = ""
    count = 0
    for char in username:
        count += 1
        temp += char
        if not SearchNode.objects.filter(val=temp).exists():
            new_node = SearchNode(val=temp, usernames=username + ",")
            new_node.save()
        else:
            node = SearchNode.objects.get(val=temp)
            node.usernames += username + ","
            node.save()


class SearchForUsersView(APIView):

    def get(self, request):
        search_string = request.GET.get("search_string")
        search_string = search_string.lower()

        node = SearchNode.objects.get(val=search_string)

        usernames = node.usernames.split(",")
        show_count = 5
        if len(usernames) < 5:
            show_count = len(usernames)

        users = []

        if User.objects.filter(username__iexact=search_string).exists():
            user = User.objects.get(username__iexact=search_string)
            userserializer = UserSerializer(user.profile)
            users.append(userserializer.data)

        for username in usernames:
            if username != search_string:
                if show_count <= 0:
                    break
                show_count -= 1
                # only filtering with lowercase
                if User.objects.filter(username__iexact=username).exists():
                    user = User.objects.get(username__iexact=username)
                    userserializer = UserSerializer(user.profile)
                    users.append(userserializer.data)

        return JsonResponse(users, safe=False, status=200)



