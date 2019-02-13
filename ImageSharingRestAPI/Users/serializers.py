from rest_framework import serializers
from .models import Profile


class UserSerializer(serializers.ModelSerializer):
    profile_pic_url = serializers.ReadOnlyField()
    string_follows_count = serializers.CharField(source="follows_count")
    string_followers_count = serializers.CharField(source="followers_count")

    class Meta:
        model = Profile
        fields = ('username', 'profile_pic_url', 'firstname', 'lastname', 'bio', 'string_follows_count',
                  'string_followers_count')
