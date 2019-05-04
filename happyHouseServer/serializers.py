from rest_framework import serializers
from happyHouseServer.models import (
    User,
    Family,
    Housework,
    HouseworkCheck
    )

class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        models = User
        fields = ('id','user_unique_id','user_name','user_profile_image','user_email','family_id')

class FamilyModelSerializer(serializers.ModelSerializer):
    class Meta:
        models = Family
        fields = ('id','created_time')

class HouseWorkModelSerializer(serializers.ModelSerializer):
    class Meta:
        models = Housework
        fields = ('id', 'housework_name', 'assignee_id')

class HouseworkCheckModelSerializer(serializers.ModelSerializer):
    class Meta:
        models = HouseworkCheck
        fields = ('id', 'housework_id','assignee_id', 'duedate')