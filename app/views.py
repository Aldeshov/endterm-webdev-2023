from rest_framework import status, generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from app.filters import PostFilter
from app.permissions import IsAuthorOrReadOnly
from app.serializers import *


class PostListAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    serializer_class = PostSerializer
    filter_class = PostFilter

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        context = super(PostListAPIView, self).get_serializer_context()
        author = self.request.user
        context.update({
            'author': author,
        })
        return context


class PostAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    permission_classes = [IsAuthorOrReadOnly]
    serializer_class = PostSerializer


class UserAPIView(APIView):
    @classmethod
    def get(cls, request):
        if request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        user = UserSerializer(request.user)
        return Response(user.data, status=status.HTTP_200_OK)

    @classmethod
    def post(cls, request):
        if not request.data.get('username') or not request.data.get('password') or not request.data.get('first_name'):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if len(request.data.get('username')) < 4 or User.objects.filter(username=request.data.get('username')).exists():
            return Response({"username": "exists or length less than 4"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=request.data.get('username'), password=request.data.get('password'))
        user.first_name = request.data.get('first_name')
        user.last_name = request.data.get('last_name')
        user.save()
        return Response(status=status.HTTP_201_CREATED)
