from rest_framework import serializers


class RegisterSerializer(serializers.Serializer):
    # name = serializers.CharField(required=True,error_messages={'blank':'name field may not be blank','required': 'Enter Valid Name'})
    email = serializers.EmailField(required=True,error_messages={'blank':'email field may not be blank','required': 'Enter Valid Mail-ID'})
    phone_number = serializers.CharField(required=True, max_length=10, allow_null=True, allow_blank=True,
                                                       error_messages={'required': 'Please enter Mobile Number',
                                                                       'invalid': 'Invalid Mobile NUmber',
                                                                       'max_length': 'Invalid Mobile Number'})

    def validate(self, attrs):
        # name = attrs['name']
        phone_number = attrs['phone_number']
        # if(name.isalpha() == False):
        #     raise serializers.ValidationError('Enter Valid Name')
        if phone_number:
            if len(phone_number) != 10 or not phone_number.isdigit():
                raise ValueError('Invalid Mobile number')
        return attrs

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True,error_messages={'blank':'email field may not be blank','required': 'Enter Valid Mail-ID'})
    password = serializers.CharField(required=True,error_messages={'blank':'password field may not be blank','required': 'Enter Correct Password'})
