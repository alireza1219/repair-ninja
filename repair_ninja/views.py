from rest_framework import status

from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def home_page_view(request):
    """A simple request handler for the homepage."""
    if request.method != 'GET':
        return Response(
            'Method not allowed.',
            status.HTTP_405_METHOD_NOT_ALLOWED
        )

    return Response(
        'Greetings from RepairNinja API 🥷',
        status.HTTP_200_OK
    )
