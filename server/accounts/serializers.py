from django.db.models import fields
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model
import re

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    # write_only : 시리얼라이징은 하지만 응답에는 포함시키지 않음
    password = serializers.CharField(write_only=True)

    def validate_username(self, value):
        regex = re.compile('^[\w\d_]{6,20}')
        if not regex.match(value):
            raise ValidationError('유효한 아이디 형식이 아닙니다.')
            
        return value
    
    def validate_password(self, value):
        regex = re.compile('^(?=.*[a-zA-z])(?=.*[0-9])(?=.*[$`~!@$!%*#^?&\\(\\)\-_=+])(?!.*[^a-zA-z0-9$`~!@$!%*#^?&\\(\\)\-_=+]).{8,20}$')
        if not regex.match(value):
            raise ValidationError('비밀번호 형식이 올바르지 않습니다.')

        return value

    class Meta:
        model = User
        fields = ('username', 'password')
