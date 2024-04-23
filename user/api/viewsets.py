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
    
    @action(detail=True, methods=['get'])
    def user_info(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        queryset = User.objects.all()
        if user_id:
            queryset = User.objects.filter(id=user_id)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def create_user(self, request, *args, **kwargs):
        email = request.data.get('email')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        password = request.data.get('password')

        user_instance = User(
            email=email,
            username=email,
            first_name=first_name,
            last_name=last_name
        )
        user_instance.set_password(password)
        user_instance.save()

        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['put'], permission_classes=[AllowAny])
    def update_user_info(self, request, *args, **kwargs):
        user_instance = self.get_object()  # Obtenha a instância do usuário com base na pk
        data = request.data

        for key, value in data.items():
            setattr(user_instance, key, value)

        user_instance.save()

        serializer = self.get_serializer(user_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)