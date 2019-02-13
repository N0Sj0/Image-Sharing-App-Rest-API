from rest_framework.views import APIView
from .models import Post
from django.http import JsonResponse
from django.contrib.auth import authenticate
from PIL import Image
from django.conf import settings
import os
from utils import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
import utils
import constants as const
from Comments.models import Comment


def create_image_path(user, post_id):
    extension = user.username + str(post_id) + ".png"
    full_path = os.path.join(settings.POST_ROOT, extension)

    return full_path, extension


class PostViewSet(ModelViewSet):

    # create/post post
    def create(self, request, *args, **kwargs):
        json_dict = request_file_to_dict(request)

        username = json_dict.get("username")
        password = json_dict.get("password")
        description = json_dict.get("description")

        user = authenticate(username=username, password=password)

        post = Post(description=description, owner=user.profile, owner_string=user.username)
        post.save()
        image = Image.open(request.FILES.get("image"))
        path, extension = create_image_path(user, post.pk)
        image.save(path)
        post.save()

        post_serializer = PostSerializer(post)

        return JsonResponse(post_serializer.data, status=200)

    @action(methods=["get"], detail=True)
    def likers(self, request, pk=None):
        post_id = pk
        owner = request.GET.get("owner")
        try:
            post = Post.objects.get(pk=post_id, owner_string=owner)
            liked_users_string = post.liked_users
            usernames = liked_users_string.split(',')
            users = utils.get_user_data_from_usernames(usernames)
            return JsonResponse(users, safe=False, status=200)
        except Post.DoesNotExist:
            return JsonResponse({"error_message": "Could not find Post"}, status=404)

    @action(methods=["post"], detail=True)
    def like(self, request, pk=None):
        user_dict = request_to_dict(request)
        username = user_dict["username"]
        password = user_dict["password"]
        post_id = pk
        owner = user_dict["owner_string"]

        try:
            user = authenticate(username=username, password=password)
            post = Post.objects.get(pk=post_id, owner_string=owner)
            if username not in post.liked_users:
                # like
                post.likes += 1
                post.liked_users += username + ","
            else:
                # unlike
                post.likes -= 1
                post.liked_users = utils.remove_username_from_string(post.liked_users, username)

            post.save()

            post_serializer = PostSerializer(post)

            return JsonResponse(post_serializer.data, status=200)
        except User.DoesNotExist:
            return JsonResponse({"error_message": "Could not find User"}, status=404)
        except Post.DoesNotExist:
            return JsonResponse({"error_message": "Could not find Post"}, status=404)

    @action(methods=["post"], detail=True)
    def comment(self, request, pk=None):
        comment_dict = request_to_dict(request)
        comment_text = comment_dict.get('comment_text')
        username = comment_dict.get("username")
        password = comment_dict.get("password")
        post_owner_string = comment_dict.get("post_owner")
        post_id = comment_dict.get("post_id")

        try:
            user = authenticate(username=username, password=password)
            post = Post.objects.get(pk=int(post_id), owner_string=post_owner_string)
            comment = Comment(text=comment_text, post=post, owner=user.profile)
            comment.save()

            post_serializer = PostSerializer(post)
            return JsonResponse(post_serializer.data, status=201)

        except User.DoesNotExist:
            return JsonResponse({"error_message": "Could not find User"}, status=404)
        except Post.DoesNotExist:
            return JsonResponse({"error_message": "Could not find Post"}, status=404)


class FeedView(APIView):

    # get the post of the users the user follows: FEED
    def get(self, request):

        try:
            username = request.GET.get("username")
            post_from_num = int(str(request.GET.get("num")))

            user = User.objects.get(username=username)
            follows_string = user.profile.follows_string

            usernames = follows_string.split(",")

            # so the user gets his own posts
            usernames.append(username)

            post_return_dict = {}
            posts, users = get_posts_from(usernames, username)

            post_return_dict["users"] = users

            # returns only 15 posts from the latest (num)
            begin = min(post_from_num, len(posts))
            end = min(len(posts), post_from_num+const.Constants.numberOfFeedPostsToReturn)
            post_return_dict["posts"] = posts[begin:end]

            return JsonResponse(post_return_dict, status=200)
        except User.DoesNotExist:
            return JsonResponse({"error_message": "Could not find User"}, status=404)
        except ValueError:
            return JsonResponse({"error_message": "Could not get num"}, status=400)



