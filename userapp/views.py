from django.contrib.auth import logout, authenticate, login
from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from userapp.models import User
from userapp.serializers import LoginSerializer, RegisterSerializer
from rest_framework.authtoken.models import Token


class Registerview(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = []
    def post(self,request):
        try:
            data = request.data
            serializer = RegisterSerializer(data=data)
            is_valid = serializer.is_valid(raise_exception=True)
            if is_valid:
                if(User.objects.filter(Q(username=request.data["email"])| Q(phone_number=request.data["phone_number"]))):
                    return Response({"status": "failure", "message": "User Already Exists"},status=status.HTTP_400_BAD_REQUEST)
                else:
                    
                    user = User(username=request.data["email"],phone_number=request.data["phone_number"],)
                    if(request.data["confirm_password"] == request.data["password"]):
                        user.set_password(request.data["password"])
                        user.save()
                        return Response({"status": "success", "message": "User Registration Successful"})
                    else:
                        return Response({"status": "failure", "message": "enter correct password"},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print('Exception {}'.format(e.args))
            try:
                error_message = e.args if not isinstance(e.args, tuple) and not isinstance(e.args, list) else e.args[0]
                if isinstance(error_message, list):
                    error_message = error_message[0]
                if isinstance(error_message, dict):
                    error = list(error_message.values())[0]
                    if isinstance(error, list):
                        error_message = error[0]
                    else:
                        error_message = error
            except Exception:
                error_message = 'Please check the values'
            return Response({'status': 'failure', 'message': error_message}, status=status.HTTP_400_BAD_REQUEST)



class Loginview(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = []
    def post(self,request):
        try:
            data = request.data
            serializer = LoginSerializer(data=data)
            is_valid = serializer.is_valid(raise_exception=True)
            if is_valid:
                check_email = User.objects.get(username=request.data["email"],is_active=True)
                user = authenticate(username=check_email.username, password=request.data["password"])
                print(user)
                if user is not None:
                    login(request,user)
                    token, created = Token.objects.get_or_create(user=user)
                    return Response({"status": "success", "message": "Login Successful",'token':token.key})
                else:
                    return Response({"status": "failure", "message": "Invalid Username or Password"},status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist as ce:
            print('Exception {}'.format(ce.args))
            return Response({'status': 'failure', 'message': 'Invalid Username or Password'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print('Exception {}'.format(e.args))
            try:
                error_message = e.args if not isinstance(e.args, tuple) and not isinstance(e.args, list) else e.args[0]
                if isinstance(error_message, list):
                    error_message = error_message[0]
                if isinstance(error_message, dict):
                    error = list(error_message.values())[0]
                    if isinstance(error, list):
                        error_message = error[0]
                    else:
                        error_message = error
            except Exception:
                error_message = 'Please check the values'
            return Response({'status': 'failure', 'message': error_message}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    def get(self, request):
        try:
            logout(request)
            return Response({"status":'success',"message":"Logged out Successfully"})
        except Exception as e:
            print('Exception {}'.format(e.args))
            return Response({"status": "failure",'message':e.args}, status=status.HTTP_400_BAD_REQUEST)

class DeleteView(APIView):
    def post(self, request):
        try:
            check_user = User.objects.get(username=request.data["email"],phone_number=request.data["phone_number"],is_active=True)
            check_user.is_active=False
            check_user.save()
            return Response({"status":'success',"message":"User Deleted Successfully",})

        except User.DoesNotExist as ce:
            print('Exception {}'.format(ce.args))
            return Response({'status': 'failure', 'message': 'Invalid Username'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print('Exception {}'.format(e.args))
            return Response({"status": "failure",'message':e.args}, status=status.HTTP_400_BAD_REQUEST)

class UpdateView(APIView):
    def put(self,request):
        try:
            check_user = User.objects.get(username=request.data["email"],phone_number=request.data["phone_number"],is_active=True)
            check_user.username =request.data["email"]
            check_user.phone_number = request.data["phone_number"]
            check_user.save()
            return Response({"status":'success',"message":"User Updated  Successfully",})

        except User.DoesNotExist as ce:
            print('Exception {}'.format(ce.args))
            return Response({'status': 'failure', 'message': 'Invalid Username'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print('Exception {}'.format(e.args))
            return Response({"status": "failure",'message':e.args}, status=status.HTTP_400_BAD_REQUEST)

