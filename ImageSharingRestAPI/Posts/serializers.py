from rest_framework import serializers
from .models import Post
from Comments.serializers import CommentSerializer


class PostSerializer(serializers.ModelSerializer):
    image_url = serializers.ReadOnlyField()
    string_likes = serializers.CharField(source="likes")
    post_id_string = serializers.SerializerMethodField("_post_id")
    user_is_liking = serializers.SerializerMethodField('_user_is_liking')
    owner_string = serializers.SerializerMethodField('_get_owner_string')
    comments = serializers.SerializerMethodField("_get_comments")
    date_string = serializers.SerializerMethodField('_get_date_string')

    def _get_date_string(self, post):
        return str(post.date)[:10]

    def _get_owner_string(self, post):
        return str(post.owner.username)

    def _post_id(self, post):
        return str(post.pk)

    def _user_is_liking(self, post):

        if "user" in self.context.keys() and self.context["user"] is not None:
            user = self.context["user"]
            return str(user in post.liked_users)

        return str(False)

    def _get_comments(self, post):

        comments = []
        for comment in post.comment_set.all():
            comment_serializer = CommentSerializer(comment)
            comments.append(comment_serializer.data)
        return comments

    class Meta:
        model = Post
        fields = ('image_url', 'description', 'owner_string', 'string_likes', "post_id_string", 'user_is_liking',
                  'comments', 'date_string')



