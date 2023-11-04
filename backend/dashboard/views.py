import json

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from dashboard.services.tiles import Tile


# Create your views here.


class TilesAPIView(APIView):
    name = 'tiles'

    def get(self, request):
        filters_object = json.loads(request.GET.get('filters', '{}'))
        filters = [{'name': filter_name, 'value': filter_value} for filter_name, filter_value in filters_object.items()]
        tile_key = request.GET.get('tile_key')
        response = Tile(filters=filters).get_tiles(tile_key=tile_key)
        return Response(response)
