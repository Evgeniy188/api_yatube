from http import HTTPStatus
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets
from posts.models import Post, Group
from .serializers import PostSerializer, CommentSerializer, GroupSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        if post.author != self.request.user:
            return Response(serializer.errors, status=HTTPStatus.FORBIDDEN)
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments.all()

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        if post.author != self.request.user:
            return Response(serializer.errors, status=HTTPStatus.FORBIDDEN)
        serializer.save(post=post, author=self.request.user)
