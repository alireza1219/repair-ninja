from rest_framework import status
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

from . import serializers


class BurstRateThrottle(UserRateThrottle):
    """
    Rate limiting class inherited from rest-framework's UserRateThrottle class.
    """
    # 3 Requests per minute.
    # This allows to fight against the OTP brute-forcing.
    rate = '3/min'


class UserOTPCreateViewSet(APIView):
    """
    This view handle the OTP initial request.
    """

    def post(self, request, *args, **kwargs):
        """
        Only POST HTTP requests can be handled by this view.
        """
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


class UserOTPVerifyViewSet(APIView):
    """
    This view handle the OTP verification request.
    """
    throttle_classes = [BurstRateThrottle]

    def post(self, request, *args, **kwargs):
        """
        Only POST HTTP requests can be handled by this view.
        """
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
