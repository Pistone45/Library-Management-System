from rest_framework import serializers
from users.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class StaffRecordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffRecords
        fields = '__all__'
