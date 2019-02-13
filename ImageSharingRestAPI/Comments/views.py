from rest_framework.views import APIView
from Posts.models import Post
from Posts.serializers import PostSerializer
from django.http import JsonResponse
from django.contrib.auth import authenticate
from utils import *
from .models import Comment

# Create your views here.
