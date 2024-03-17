from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from . import utils as otp_utils


# Get the default user model defined in settings.
User = get_user_model()


class CreateUserOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'A user with this email does not exists!')
        return email

    def otp_action(self):
        user_email = self.validated_data.get('email')
        try:
            user = User.objects.get(email=user_email)
            otp = otp_utils.generate_otp(user)

            # TODO: Actually implement this and sent an email with otp.
            # For now just print it in the terminal.

            print(f"Here is your otp: {otp}")

            return True
        except User.DoesNotExist:
            return False


class ValidateUserOTPSerializer(CreateUserOTPSerializer):
    otp = serializers.CharField(max_length=6)

    def otp_action(self):
        user_email = self.validated_data.get('email')
        try:
            user = User.objects.get(email=user_email)
            otp = self.validated_data.get('otp')
            otp_result = otp_utils.verify_otp(user, otp)

            if otp_result:
                return user
            return False
        except User.DoesNotExist:
            return False

    def generate_tokens(self, user):
        token = RefreshToken.for_user(user)
        return {
            'refresh': str(token),
            'access': str(token.access_token),
        }
