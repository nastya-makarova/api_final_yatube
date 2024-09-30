from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.exceptions import ParseError
from rest_framework.response import Response

from .permissions import OwnerOrReadOnly, ReadOnly
from .serializers import CommentSerializer, GroupSerializer, FollowSerializer, PostSerializer
from posts.models import Follow, Group, Post, User


class BaseViewSet(viewsets.ModelViewSet):
    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()


class PostViewSet(BaseViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (OwnerOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(BaseViewSet):
    serializer_class = CommentSerializer
    permission_classes = (OwnerOrReadOnly,)

    def get_post(self):
        post_id = self.kwargs['post_id']
        return get_object_or_404(Post, pk=post_id)

    def get_queryset(self):
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer

    def get_user(self):
        user_id = self.request.user.id
        return get_object_or_404(User, id=user_id)

    def get_queryset(self):
        return self.get_user().follower.all()

    def perform_create(self, serializer):
        following_name = self.request.data.get('following')
        following_user = get_object_or_404(User, username=following_name)

        if self.request.user == following_user:
            raise ParseError('Вы не можете подптсаться на самого себя.'
                             'Укажите другое имя пользователя.')

        if Follow.objects.filter(
            user=self.request.user, following=following_user
        ):
            raise ParseError('Вы уже подписаны на этого пользователя.')

        serializer.save(user=self.request.user, following=following_user)
