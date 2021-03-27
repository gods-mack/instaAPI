from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer
from rest_framework import viewsets, generics
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework import status

from django.contrib.auth import login

from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView



# Create your views here.


# Register API

# class RegisterAPI(generics.GenericAPIVew):
# 	serializer_class = RegisterSerializer

# 	def post(self,request,*args,**kwargs):
# 		serializer = self.get_serializer(data=request.data)
# 		serializer.is_valid(raise_exception=True)
# 		user = serializer.save()
# 		return Response({
# 			"user":UserSerializer(user, context=self.get_serializer_context()).data,
# 			"token":AuthToken.objects.create(user)[1]
# 			})


@api_view(['GET','POST'])
def user_list(request):


	if request.method=='GET':
		print("GET REQUEST BEING PROCESSED")
		users = User.objects.all()
		serializer = UserSerializer(users,many=True)
		return Response(serializer.data)


	elif request.method=='POST':
		print("POST REQUEST BEING PROCESSED")
		serializer = RegisterSerializer(data=request.data)
		if serializer.is_valid():
			user = serializer.save()
			return Response({
				"user":serializer.data,
				"token":AuthToken.objects.create(user)[1]
				}, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


# Get User API
class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

from rest_framework import generics, permissions

# Change Password

from django.contrib.auth.models import User
from .serializers import ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated   

class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

