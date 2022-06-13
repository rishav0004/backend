
import email
from logging import raiseExceptions
from django.shortcuts import get_object_or_404
from matplotlib.style import context
from rest_framework.response import Response
from rest_framework import generics, permissions, status
from accounts.models import Customuser, Driver, Manager, Vehicle
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken 

from accounts.serializers import VehicleUpdateSerializer, DriverSignupSerializer,UpdateUserSerializer,DriverSerializer,  HeadSignupSerializer, ManagerSerializer, ManagerSignupSerializer, SendPasswordResetEmailSerializer, UserChangePasswordSerializer, UserLoginSerializer, UserPasswordResetSerializer, UserProfileSerilaizer,  UserSerializer, VehicleSerializer, VehicleSignupSerializer, Driveradd
# from rest_framework.authtoken.models import Token

# Create your views here.
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }



class UserLoginView(APIView):
    def post(self,request,format=None):
        serializer = UserLoginSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email,password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token':token,'msg':'Login Success'},status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}},status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class AllUsersView(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self,request,pk=None,format = None):
        id = pk
        if id is not None:
            veh = Customuser.objects.get(id=id)
            serializer = UserProfileSerilaizer(veh,context ={'request':request})
            return Response(serializer.data)
        queryset = Customuser.objects.all()
        serializer = UserProfileSerilaizer(queryset,many=True,context ={'request':request})
        return Response(serializer.data,status=status.HTTP_200_OK)



class HeadSignupView(generics.GenericAPIView):
    serializer_class = HeadSignupSerializer
    def post(self, request, *args, **kwargs):
        # if request.user.is_superuser == True:
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user':UserSerializer(user,context=self.get_serializer_context()).data,
            'msg':'account created successfully'
        })
 

class AllVehicles(APIView):
    def get(self,request,pk=None,format = None):
        id = pk
        
        if id is not None:
            veh = Vehicle.objects.get(id=id)
            serializer = VehicleSerializer(veh,context ={'request':request})
            return Response(serializer.data)

        queryset = Vehicle.objects.all()
        serializer = VehicleSerializer(queryset,many=True,context ={'request':request})
        return Response(serializer.data)

class AllDrivers(APIView):
    def get(self,request,pk=None,format=None):
        id = pk
        if id is not None:
            d = Driver.objects.get(id=id) 
            serializer = DriverSerializer(d,context={'request':request})
            return Response(serializer.data)
        queryset = Driver.objects.all()
        serializer = DriverSerializer(queryset,many=True,context = {'request':request})
        return Response(serializer.data)

class AllUserDriver(APIView):
    def get(self,request,pk=None,format=None):
        id = pk
        if id is not None:
            d = Customuser.objects.get(id=id) 
            serializer = UserSerializer(d,context={'request':request})
            return Response(serializer.data)
        queryset = Customuser.objects.filter(is_driver=True)
        serializer = UserSerializer(queryset,many=True,context={'request':request})
        return Response(serializer.data)

class AllManagers(APIView):
    def get(self,request,pk=None,format = None):
        id = pk
        if id is not None:
            man = Manager.objects.get(id=id)
            serializer = ManagerSerializer(man,context ={'request':request})
            return Response(serializer.data)
        queryset = Manager.objects.all()
        serializer = ManagerSerializer(queryset,many=True,context = {'request':request})
        return Response(serializer.data)

class VehicleSignupView(generics.GenericAPIView):
    serializer_class = VehicleSignupSerializer
    def post(self, request, *args, **kwargs):
        if request.user.is_manager == True or request.user.is_head == True:
            serializer = self.get_serializer(data = request.data)
            serializer.is_valid(raise_exception=True)
            vehicle = serializer.save()
            return Response({
                'vehicle':VehicleSerializer(vehicle,context=self.get_serializer_context()).data,
                'msg':'Vehicle created successfully'
            })
        return Response({'msg':'you are not eligible to add Vehicle, login as Manager or Head'})
    

class DriverSignupView(generics.GenericAPIView):
    serializer_class = DriverSignupSerializer
    def post(self, request, *args, **kwargs):
        if request.user.is_manager == True or request.user.is_head == True or request.user.is_admin==True:
            serializer = self.get_serializer(data = request.data,context ={'request':request})
            serializer.is_valid(raise_exception = True)
            driver = serializer.save()
            return Response({
                'driver':UserSerializer(driver,context=self.get_serializer_context()).data,
                'msg':'account created successfully'
            })
        return Response({'msg':'you are not eligible to add Driver, login as Manager or Head'})



class ManagerSignupView(generics.GenericAPIView):
    serializer_class = ManagerSignupSerializer
    def post(self, request, *args, **kwargs):
        if request.user.is_head==True:
            serializer = self.get_serializer(data = request.data,context ={'request':request})
            serializer.is_valid(raise_exception = True)
            manager = serializer.save()
            return Response({
                'manager':UserSerializer(manager,context=self.get_serializer_context()).data,
                'msg':'account created successfully'
            })
        return Response({'msg':'you are not eligible to add Manager, login as Head'})
 

# class ManagerView(generics.RetrieveAPIView):
#     serializer_class=UserSerializer
#     def get_object(self):
#         return self.request.user
class UpdateManagerView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self,request,pk,format=None):
        if request.user.is_head==True:
            id = pk
            man = Manager.objects.get(id=pk)
            serializer = ManagerSerializer(man,data=request.data,context ={'request':request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'msg':'Manager Updated Successfully'})
            return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)
        
class UpdateDriverView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self,request,pk,format=None):
        if request.user.is_head==True or request.user.is_manager==True:
            id = pk
            man = Driver.objects.get(id=pk)
            serializer = DriverSerializer(man,data=request.data,context ={'request':request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'msg':' Updated Successfully'})
            return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)

class UpdateVehicleView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self,request,pk,format=None):
        if request.user.is_head==True or request.user.is_manager==True:
            id = pk
            veh = Vehicle.objects.get(pk=id)
            serializer = VehicleSerializer(veh, data=request.data,context ={'request':request})
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':'Data updated Successfully'})
            return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)


class DeleteVehicleView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self,request,pk,format=None):
        if request.user.is_head==True or request.user.is_manager==True:
            id = pk
            veh = Vehicle.objects.get(pk=id)
            veh.delete()
            return Response({'msg':'Vehicle deleted Successfully'})
        return Response({'msg':'You are not allowed to Delete the Vehicle'})

class DeleteDriverView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self,request,pk,format=None):
        if request.user.is_head==True or request.user.is_manager==True:
            id = pk
            veh = Driver.objects.get(pk=id)
            veh.delete()
            return Response({'msg':'Driver with Assigned Vehicle deleted Successfully'})
        return Response({'msg':'You are not allowed to Delete '})

class UpdateProfileView(generics.UpdateAPIView):
    queryset = Customuser.objects.all()
    serializer_class = UpdateUserSerializer
    
class DeleteProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self,request,pk,format=None):
        if request.user.is_head==True or request.user.is_manager==True:
            id = pk
            cuser = Customuser.objects.get(pk=id)
            cuser.delete()
            return Response({'msg':'User deleted Successfully'})
        return Response({'msg':'You are not allowed to Delete the user'})

    

class UserChangePassword(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(data = request.data,context = {'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class SendPasswordResetEmailView(APIView):
    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Reset Link send, Check your email'}, status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class UserPasswordResetView(APIView):
    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(data = request.data,
        context = {'uid':uid, 'token':token})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class newDriver(generics.GenericAPIView):
    serializer_class = Driveradd
    def post(self, request, *args, **kwargs):
        # id = request.data.get('user')
        # instance = Customuser.objects.get(id = id)
        # vehicle_assigned = request.data.get('vehicle_assigned')
        # instance = Customuser.objects.get(email = user)
        if request.user.is_driver==True or request.user.is_manager==True or request.user.is_head==True:
        # instance = Vehicle.objects.get(vehicle_name = vehicle_assigned)
            serializer = self.get_serializer( data = request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({
                # 'driver':UserSerializer(driver,context=self.get_serializer_context()).data,
                'msg':'account created successfully'
            })
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
  permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
    serializer = UserSerializer(request.user,context ={'request':request})
    return Response(serializer.data, status=status.HTTP_200_OK)