from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from .permissions import OwnerOrReadOnly, ReadOnly
from .serializers import CommentSerializer, GroupSerializer, PostSerializer
from posts.models import Group, Post


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
    print(queryset)
    serializer_class = GroupSerializer
