from rest_framework.response import Response
from rest_framework.views import APIView

from data.models import Star, Director


class FilterAPIView(APIView):
    name = 'filter'

    def get(self, response):
        return Response([{
            'label': 'Star', 'name': 'star', 'values': Star.objects.values_list('name', flat=True).order_by('name')
        }, {
            'label': 'Director', 'name': 'director', 'values': Director.objects.values_list(
                'name', flat=True
            ).order_by('name')
        }])
