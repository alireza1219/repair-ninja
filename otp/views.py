from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers


class CustomerOTPCreateViewSet(APIView):
    def post(self, request, *args, **kwargs):
        serializer = serializers.CreateUserOTPSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        otp_result = serializer.otp_action()

        if not otp_result:
            return Response(
                {'message': 'Something went wrong on our side. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            {'message': 'An OTP was sent to your email account.'},
            status=status.HTTP_200_OK
        )


class CustomerOTPVerifyViewSet(APIView):
    def post(self, request, *args, **kwargs):
        serializer = serializers.ValidateUserOTPSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        otp_result = serializer.otp_action()

        if not otp_result:
            return Response(
                {'message': 'Your OTP was not correct.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            serializer.generate_tokens(otp_result),
            status=status.HTTP_200_OK
        )
