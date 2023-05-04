from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from users.models import User


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    username = serializers.CharField(
        max_length=127,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="username already taken.",
                lookup="iexact",
            )
        ],
    )

    password = serializers.CharField(max_length=127, write_only=True)

    email = serializers.CharField(
        max_length=150,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="email already registered.",
                lookup="iexact",
            )
        ],
    )

    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    birthdate = serializers.DateField(allow_null=True, default=None)

    is_employee = serializers.BooleanField(allow_null=True, default=False)
    is_superuser = serializers.BooleanField(read_only=True)

    def create(self, validated_data: dict) -> User:
        is_employee = validated_data.get("is_employee", False)
        is_superuser = is_employee if is_employee else False
        validated_data["is_superuser"] = is_superuser
        return User.objects.create_user(**validated_data)

    def update(self, instance: User, validated_data: dict) -> User:
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.set_password(validated_data["password"])

        instance.save()

        return instance
