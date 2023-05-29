from django.contrib.auth import get_user_model

from rest_framework import serializers

UserModel = get_user_model()


class UserSerializerField(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = UserModel
        fields = ('first_name', 'last_name', 'full_name', )

    def get_full_name(self, obj):
        return obj.get_full_name()
