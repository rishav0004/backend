from django.utils import timezone
from rest_framework import serializers
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode

from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.forms import ValidationError
# from .utils import Util
from .models import Customuser, Vehicle, Manager, Driver, Head

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customuser
        fields = ['id','username','email','first_name','last_name','profile_image','is_driver','is_manager','is_head']


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'


class DriverSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    vehicle_assigned = VehicleSerializer(many=False)
    class Meta:
        model = Driver
        fields = '__all__'
        
class ManagerSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    class Meta:
        model = Manager
        fields = '__all__'

class HeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Head
        fields = '__all__'

class HeadSignupSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={"input_type":"password"}, write_only=True)
    class Meta:
        model=Customuser
        # fields=['username','email','password','first_name','last_name','password2','profile_image','dob',]
        fields=['username','email','password','first_name','last_name','password2','dob',]
        extra_kwargs={
            'password':{'write_only':True}
        }
        

    def save(self, **kwargs):
        user = Customuser(
            username = self.validated_data['username'],
            email=self.validated_data['email'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            dob = self.validated_data['dob'],
            # profile_image = self.validated_data['profile_image'],
        )
        password=self.validated_data['password']
        password2=self.validated_data['password2']
        if password !=password2:
            raise serializers.ValidationError({"error":"password do not match"})
        user.set_password(password)
        user.is_head = True
        user.last_login = timezone.now()
        user.save()
        Head.objects.create(user = user)
        return user

class DriverSignupSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={"input_type":"password"}, write_only=True)

    class Meta:
        model=Customuser
        fields=['username','email','password','first_name','last_name','password2','dob']
        extra_kwargs={
            'password':{'write_only':True}
        }
        

    def save(self, **kwargs):
        user = Customuser(
            username = self.validated_data['username'],
            email=self.validated_data['email'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            dob = self.validated_data['dob'],
            # profile_image = self.validated_data['profile_image']
        )
        password=self.validated_data['password']
        password2=self.validated_data['password2']
        if password !=password2:
            raise serializers.ValidationError({"error":"password do not match"})
        user.set_password(password)
        user.is_driver = True
        user.last_login = timezone.now()
        user.save()
        # Customuser.objects.create(user = user)
        return user


class VehicleSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['vehicle_name','vehicle_model','vehicle_year','vehicle_type',
                    'vehicle_photo','chassi_number','registration_number']

    def create(self, validated_data):
        return Vehicle.objects.create(**validated_data)
    
    



class ManagerSignupSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={"input_type":"password"}, write_only=True)
    class Meta:
        model=Customuser
        fields=['username','email','password','first_name','last_name','password2','dob',]
        extra_kwargs={
            'password':{'write_only':True}
        }
        

    def save(self, **kwargs):
        user = Customuser(
            username = self.validated_data['username'],
            email=self.validated_data['email'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            dob = self.validated_data['dob'],
        )
        password=self.validated_data['password']
        password2=self.validated_data['password2']
        if password !=password2:
            raise serializers.ValidationError({"error":"password do not match"})
        user.set_password(password)
        user.is_manager = True
        user.last_login = timezone.now()
        user.save()
        Manager.objects.create(user = user)
        return user

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length = 255)
    class Meta:
        model = Customuser
        fields = ['email','password']

class UserProfileSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = Customuser
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customuser
        fields = ['id','username','email','first_name','last_name','dob','profile_image','is_driver','is_head','is_manager']

        
class Driveradd(serializers.ModelSerializer):
    # vehicle_assigned = VehicleSerializer(many=True)

    class Meta:
        model = Driver
        fields = '__all__'

    def create(self,validated_data):
        # vehicle_assigned = validated_data.pop('vehicle_assigned')
        # user_data = validated_data.pop('user')
        # driver = user_data.is_driver
        driver_data = Driver.objects.create(**validated_data)
        return driver_data

        # for user_data in users_data:
            # user = Customuser.objects.create(user=user_data,**driver_data)
        # return user
        # users_data = validated_data.pop('user')
        # driver_data = Driver.objects.create(**validated_data)
        # for user_data in users_data:
        #     Customuser.objects.create(**user_data)
        # return driver_data
class UpdateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customuser
        fields = ['username','first_name','last_name','profile_image','email','dob']
        

    def put(self, instance, validated_data):
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.username = validated_data['username']
        instance.profile_image = validated_data['profile_image']
        instance.dob = validated_data['dob']
        instance.email = validated_data['email']
        instance.save()

        return instance


class VehicleUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vehicle
        fields = ['vehicle_name','vehicle_model','vehicle_year','vehicle_type',
                    'vehicle_photo','chassi_number','registration_number']
    
    def put(self,instance,validated_data):
        instance.vehicle_name = validated_data['vehicle_name']
        instance.vehicle_model = validated_data['vehicle_model']
        instance.vehicle_year = validated_data['vehicle_year']
        instance.vehicle_type = validated_data['vehicle_type']
        instance.vehicle_photo = validated_data['vehicle_photo']
        instance.chassi_number = validated_data['chassi_number']
        instance.registration_number = validated_data['registration_number']

        instance.save()

        return instance
    
# class DeleteUserSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Customuser
#         fields = '__all__'
    
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)





class UserChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'}
    ,write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type':'password'}
    ,write_only=True)
    
    class Meta:
        model = Customuser
        fields = ['password','password2']
    
    def validate(self,attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password!=password2:
            raise serializers.ValidationError('password and confirm password doesnot match')
        user.set_password(password)
        user.save()
        return attrs

        
class SendPasswordResetEmailSerializer(serializers.ModelSerializer):
        email = serializers.EmailField(max_length=255)
        class Meta:
            model = Customuser
            fields = ['email']

        
        def validate(self, attrs):
            email = attrs.get('email')
            if Customuser.objects.filter(email=email).exists():
                user = Customuser.objects.get(email=email)
                uid = urlsafe_base64_encode(force_bytes(user.id))
                print('encoded UID',uid)
                token = PasswordResetTokenGenerator().make_token(user)
                print('possword reset token',token)
                link ='http://localhost:3000/api/reset-password/'+uid+'/'+token
                print('password reset link',link)

                body = 'Click Following Link to Reset Your Password '+link
                data = {
                    'subject':'Reset Your Password',
                    'message':body,
                    'to_email':user.email
                }
                # Util.sending_mail(data)
                return attrs
            else:
                raise serializers.ValidationError('You are not a Registered User')

class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'}
    ,write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type':'password'}
    ,write_only=True)
    
    class Meta:
        fields = ['password','password2']
    
    def validate(self,attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password!=password2:
                raise serializers.ValidationError('password and confirm password doesnot match')
            id = smart_str(urlsafe_base64_decode(uid))
            user = Customuser.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise ValidationError('Token is not valid or expired')
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user,token)
            raise ValidationError('Token is not valid or expired')
