from rest_framework import serializers

from documents.models import Document
from users.serializer_fields import UserSerializerField


class DocumentListSerializer(serializers.ModelSerializer):
    author = UserSerializerField()

    class Meta:
        model = Document
        fields = ('id', 'title', 'content', 'author', 'created', )


class DocumentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'title', 'content', )
