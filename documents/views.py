from rest_framework import status
from rest_framework.mixins import (CreateModelMixin, ListModelMixin,
                                   RetrieveModelMixin)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from documents.models import Document
from documents.permissions import IsDocumentOwner
from documents.serializers import (DocumentCreateSerializer,
                                   DocumentListSerializer)
from users.authentication import JWTAuthentication


class DocumentViewSet(ListModelMixin,
                      CreateModelMixin,
                      RetrieveModelMixin,
                      GenericViewSet):
    authentication_classes = (JWTAuthentication, )

    def get_permissions(self):
        permission_classes = (IsAuthenticated, IsDocumentOwner, )
        if self.action == 'retrieve':
            permission_classes = (AllowAny, )
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        serializer_class = DocumentListSerializer
        if self.action == 'create' or self.action == 'perform_create':
            serializer_class = DocumentCreateSerializer
        return serializer_class

    def get_queryset(self):
        queryset = Document.objects.all()
        if self.action != 'retrieve':
            user = self.request.user
            queryset = Document.objects.filter(author=user)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        if len(serializer.data) > 0:
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = {
                'x-document-id': serializer.data.get('id'),
            }
            return Response(headers=headers, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)
