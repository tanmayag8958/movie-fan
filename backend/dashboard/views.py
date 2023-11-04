from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from dashboard.services.tiles import Tile


# Create your views here.


class TilesAPIView(APIView):
    name = 'tiles'

    def get(self, request):
        response = Tile().get_tiles()
        return Response(response)
