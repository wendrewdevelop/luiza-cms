from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action, authentication_classes
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from plans.models import UserPlan, Plans
from plans.api.serializers import UserPlanSerializer
from user.permissions import UserPermission


class UserPlanViewset(ModelViewSet):
    serializer_class = UserPlanSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('user', 'plan')
    permission_classes = [UserPermission]

    def get_queryset(self):
        plan_id = self.request.query_params.get('user_id', None)
        queryset = UserPlan.objects.all()
        if plan_id:
            queryset = queryset.filter(id=plan_id)

        return queryset
    
    def list(self, request, *args, **kwargs):
        return super(UserPlanViewset, self).list(request, *args, **kwargs)
    
    @action(detail=True, methods=['get'])
    def user_plan(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        serializer = self.get_serializer(
            UserPlan.get_user_plan(
                user_id=user_id
            ), 
            many=True
        )

        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def assign_user_plan(self, request, *args, **kwargs):
        user_id = request.user
        plan_name = request.data.get('plan')

        plan_instance = Plans.objects.filter(
            plan=plan_name
        ).first()
        plan_assign_instance = UserPlan.assign_user_plan(
            user_id=user_id,
            plan_id=plan_instance
        )

        return plan_assign_instance

    @action(detail=True, methods=['put'])
    def update_user_plan(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        plan_name = request.data.get('plan')

        plan_instance = Plans.objects.filter(
            plan=plan_name
        ).first()
        new_plan_instance = UserPlan.update_user_plan(
            user_id=user_id,
            new_plan_id=plan_instance
        )

        return new_plan_instance