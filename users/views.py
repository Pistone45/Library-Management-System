from django.contrib.auth import authenticate, logout
from django.db import transaction
from django.http import JsonResponse
from rest_framework import generics, permissions, status
from django.contrib.auth.models import User as AuthUser
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from library_catalogue.models import Membership
from users.serializers import *


class SignInView(APIView):
    authentication_classes = []  # Disable authentication for this view
    permission_classes = []  # Disable permission checks for this view

    def post(self, request, *args, **kwargs):
        username = request.data['username']
        password = request.data['password']

        if not username or not password:
            return JsonResponse({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Get user from database
        user = authenticate(username=username, password=password)
        if user is not None:
            # A backend authenticated the credentials
            token = Token.objects.get_or_create(user=user)
            print(user.id)
            user_data = User.objects.get(user_id=user.id)
            data = {'token': token[0].key,
                    'user_id': user.id,
                    'first_name': user.first_name,
                    'middle_name': user_data.middle_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'postal_address': user_data.postal_address,
                    'physical_address': user_data.physical_address,
                    'role': {'role_id': user_data.role.role_id, 'role_name': user_data.role.role_name}
                    }
            return JsonResponse(data, safe=False)
        else:
            # No backend authenticated the credentials
            return JsonResponse({'error': 'Invalid credentials'}, safe=False)


# User Views
class UserCreateView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            sid = transaction.savepoint()
            try:

                if len(request.data['password'].replace(" ", "")) < 8:
                    return Response({"error": "Password must be at least 8 characters long"},
                                    status=status.HTTP_400_BAD_REQUEST)

                # Create parent user
                parent_user = AuthUser.objects.create_user(username=request.data['username'],
                                                           password=request.data['password'],
                                                           email=request.data['email'],
                                                           first_name=request.data['first_name'],
                                                           last_name=request.data['last_name'])
                parent_user.save()

                # Extend user
                ext_user = User(middle_name=request.data['middle_name'], postal_address=request.data['postal_address'],
                                physical_address=request.data['physical_address'], role_id=request.data['role_id'],
                                user_id=parent_user.id)
                ext_user.save()

                # Check Role
                role = Role.objects.get(pk=request.data['role_id'])
                if role.role_name == "Member":
                    # Create pending Membership
                    membership = Membership(membership_status_id=3, user_id=ext_user.user_id)
                    membership.save()

                else:
                    # Create staff records
                    staff = StaffRecords(qualification=request.data['qualification'],
                                         experience=request.data['experience'],
                                         skill_set=request.data['skill_set'], grade=request.data['grade'],
                                         user_id=ext_user.user_id)
                    staff.save()

                # Authenticate and Create a token
                user = authenticate(username=request.data['username'], password=request.data['password'])
                token = Token.objects.get_or_create(user=user)
                data = {'token': token[0].key,
                        'user_id': parent_user.id,
                        'first_name': parent_user.first_name,
                        'middle_name': ext_user.middle_name,
                        'last_name': parent_user.last_name,
                        'email': parent_user.email,
                        'postal_address': ext_user.postal_address,
                        'physical_address': ext_user.physical_address,
                        'role': {'role_id': ext_user.role.role_id, 'role_name': ext_user.role.role_name}
                        }

                # Commit the changes
                transaction.savepoint_commit(sid)
                return JsonResponse(data, safe=False)

            except Exception as e:
                transaction.savepoint_rollback(sid)
                data = {"code": status.HTTP_400_BAD_REQUEST, "message": "Failed to create user"}
                return JsonResponse(data, safe=False)


class UserListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserUpdateView(generics.UpdateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDestroyView(generics.DestroyAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Role Views
class RoleCreateView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class RoleListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class RoleDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class RoleUpdateView(generics.UpdateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class RoleDestroyView(generics.DestroyAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


# Staff Records Views
class StaffRecordsCreateView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = StaffRecords.objects.all()
    serializer_class = StaffRecordsSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class StaffRecordsListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = StaffRecords.objects.all()
    serializer_class = StaffRecordsSerializer


class StaffRecordsDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = StaffRecords.objects.all()
    serializer_class = StaffRecordsSerializer


class StaffRecordsUpdateView(generics.UpdateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = StaffRecords.objects.all()
    serializer_class = StaffRecordsSerializer


class StaffRecordsDestroyView(generics.DestroyAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = StaffRecords.objects.all()
    serializer_class = StaffRecordsSerializer
