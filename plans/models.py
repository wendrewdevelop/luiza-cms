import uuid
from django.db import models
from rest_framework import status
from rest_framework.response import Response
from user.models import User


class Plans(models.Model):
    """
        Plans: [
            Free tier (free_tier), 
            Basic (basic), 
            Premium (premium), 
            Plus (plus)
        ]
    """
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4,
        editable=False
    )
    plan = models.CharField(
        verbose_name='plan',
        max_length=200,
        blank=True,
        null=True
    )
    created_at = models.DateTimeField('date joined', auto_now_add=True)

    class meta:
        verbose_name = 'plan'
        verbose_name_plural = 'plans'
        db_table = 'tb_plans'


class UserPlan(models.Model):
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4,
        editable=False
    )
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT
    )
    plan = models.ForeignKey(
        Plans,
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )
    created_at = models.DateTimeField('date joined', auto_now_add=True)

    class meta:
        verbose_name = 'user_plan'
        verbose_name_plural = 'user_plans'
        db_table = 'tb_user_plan'

    def get_user_plan(user_id: uuid):
        user_instance = Plans.objects.filter(
            user=user_id
        ).first()

        if user_instance:
            if user_instance.plan:
                return user_instance.plan
        else:
            return None
        
    def assign_user_plan(user_id: uuid, plan_id: uuid):
        try:
            plan_instance = UserPlan(
                user=user_id,
                plan=plan_id
            )
            plan_instance.save()
            return Response({'message': 'Plan selected successfully!'}, status=status.HTTP_201_CREATED)
        except Exception as error:
            return Response({'message': f'{error}'}, status=status.HTTP_400_BAD_REQUEST)
        
    def update_user_plan(user_id: uuid, new_plan_id: uuid):
        try:
            plan_instance = UserPlan.objects.filter(
                user=user_id
            ).first()
            plan_instance.plan = new_plan_id
            plan_instance.save()
            return Response({'message': 'Plan updated successfully!'}, status=status.HTTP_201_CREATED)
        except Exception as error:
            return Response({'message': f'{error}'}, status=status.HTTP_400_BAD_REQUEST)

