from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    owner_string = serializers.SerializerMethodField('_get_owner_string')

    def _get_owner_string(self, comment):
        return comment.owner.username

    class Meta:
        model = Comment
        fields = ('owner_string', 'text')