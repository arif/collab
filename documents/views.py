from rest_framework import status
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from documents.models import Document
from documents.permissions import IsDocumentOwner
from documents.serializers import DocumentListSerializer
from users.authentication import JWTAuthentication


class DocumentViewSet(ListModelMixin, GenericViewSet):
    authentication_classes = (JWTAuthentication, )
    permission_classes = (IsAuthenticated, IsDocumentOwner, )
    serializer_class = DocumentListSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Document.objects.filter(author=user)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        if len(serializer.data) > 0:
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)
