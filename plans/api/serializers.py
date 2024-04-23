from rest_framework import serializers
from plans.models import UserPlan


class UserPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPlan
        fields = (
            'id', 
            'plan', 
            'user'
        )