from django.contrib.auth.models import User
from django.forms import ValidationError
from rest_framework import serializers
from pprint import pprint
from advertisements.models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    def create(self, validated_data):
        """Метод для создания"""
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        checker = 0
        for advertisement in Advertisement.objects.filter(status='OPEN', creator = self.context['request'].user.id).all():
            checker += 1
        if checker == 10 and dict(data).get('status') != 'CLOSED':
            raise ValidationError('You already have more 10 advertisements. Close one for post')
        return data
