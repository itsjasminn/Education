import re

from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from authentication.models import User


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = 'first_name', 'last_name', 'phone_number', 'address', 'city', 'avatar',

    def validate_phone_number(self, value):
        phone = re.sub('\D', '', value)
        pattern = r'^998(90|91|93|94|95|97|98|99|33|88|50|77)\d{7}$'

        if not re.match(pattern, phone):
            raise ValidationError('Telefon raqami quyidagi formatda bo‘lishi kerak: +998XXXXXXXXX')

        queryset = User.objects.filter(phone_number=phone)
        if queryset.exists():
            raise ValidationError('Bu telefon raqamli foydalanuvchi allaqachon mavjud.')
        return phone

    def validate_password(self, value):
        if len(value) < 4:
            raise ValidationError('Password must be at least 4 characters long.')
        if len(value) > 20:
            raise ValidationError('Password must be at most 20 characters long.')
        if not re.search(r'\d', value):
            raise ValidationError('Password must contain at least one digit.')
        if not re.search(r'[A-Za-z]', value):
            raise ValidationError('Password must contain at least one letter.')

        return value

    def validate_avatar(self, value):
        if value and not value.name.lower().endswith(('.jpg', 'jpeg', 'png')):
            raise ValidationError('Avatar must be an image.')
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
