import json
from django.contrib.auth.models import User
from Posts.serializers import PostSerializer
from Users.serializers import UserSerializer
import functools


def request_file_to_dict(request):
    json_string = str(request.FILES["json"].read().decode('utf-8'))
    json_dict = json.loads(json_string)
    return json_dict


def request_to_dict(request):
    json_string = request.body.decode('utf-8')
    json_dict = json.loads(json_string)

    return json_dict


def get_user_data_from_usernames(usernames):
    users = []
    for username in usernames:
        if User.objects.filter(username=username).exists():
            follower = User.objects.get(username=username)
            userserializer = UserSerializer(follower.profile)
            users.append(userserializer.data)

    return users


def sort_posts_by_date(a, b):
    first_date = str(a.date)[:19]
    second_date = str(b.date)[:19]

    first_date = first_date.replace(" ", "")
    first_date = first_date.replace(":", "")
    first_date = first_date.replace("-", "")

    second_date = second_date.replace(" ", "")
    second_date = second_date.replace(":", "")
    second_date = second_date.replace("-", "")

    first_date_val = int(first_date)
    second_date_val = int(second_date)

    if first_date_val > second_date_val:
        return 1
    elif first_date_val == second_date_val:
        return 0
    else:
        return -1


def get_posts_from(usernames, user_asking_for_posts=None):
    posts = []
    users = []
    for username in usernames:
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            user_serializer = UserSerializer(user.profile)
            users.append(user_serializer.data)
            for post in user.profile.post_set.all():
                posts.append(post)

    serialized_posts = []

    posts = sorted(posts, key=functools.cmp_to_key(sort_posts_by_date))

    posts.reverse()

    for post in posts:
        post_serializer = PostSerializer(post, context={"user": user_asking_for_posts})
        serialized_posts.append(post_serializer.data)

    return serialized_posts, users


def remove_username_from_string(string, username):
    location = string.find(username)
    p1 = string[:location]
    p2 = string[location + len(username) + 1:]
    return p1+p2
