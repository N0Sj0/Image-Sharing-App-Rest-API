"""ImageSharingRestAPI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.urls import path
from Users import views as user_views
from Posts import views as post_views
from Search import views as search_views
from django.conf.urls import url
from django.views.static import serve
from rest_framework import routers

router = routers.SimpleRouter()
router.register('users', user_views.UserViewSet, base_name="users")
router.register('posts', post_views.PostViewSet, base_name="posts")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', user_views.LoginView.as_view()),
    path('feed/', post_views.FeedView.as_view()),
    path("search/", search_views.SearchForUsersView.as_view()),
    path("follow/", user_views.FollowUserView.as_view()),
]

urlpatterns += router.urls
urlpatterns += [url(r'^postimages/(?P<path>.*)', serve, {'document_root': settings.POST_ROOT})]
urlpatterns += [url(r'^profilepictures/(?P<path>.*)', serve, {'document_root': settings.PROFILEPIC_ROOT})]