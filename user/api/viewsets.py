from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action, authentication_classes
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from user.models import User
from user.api.serializers import UserSerializer
from user.permissions import UserPermission


class UserViewset(ModelViewSet):
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('email', 'first_name')
    permission_classes = [UserPermission]

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id', None)
        queryset = User.objects.all()
        if user_id:
            queryset = queryset.filter(id=user_id)

        return queryset
    
    def list(self, request, *args, **kwargs):
        return super(UserViewset, self).list(request, *args, **kwargs)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def create_user(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        return super(UserViewset, self).destroy(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super(UserViewset, self).retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super(UserViewset, self).update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super(UserViewset, self).partial_update(request, *args, **kwargs)