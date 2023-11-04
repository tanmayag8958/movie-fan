from django.db.models import Count

from dashboard.exceptions import TileNotImplemented
from dashboard.models import Movie, Star, Director
from dashboard.services.charts import ChartService
from dashboard.services.utils import get_filter_query


class Tile:

    def __init__(self, filters=None):
        self.filters = filters

    def get_movies_count(self, tile_key):
        query = get_filter_query(self.filters)
        if not query:
            query = Movie.objects
        result = query.values('media__name').distinct().count()

        return {
            'tile_key': tile_key, 'tile': {'result': result}
        }

    def get_chart_by_tile_key(self, tile_key):
        chart = ChartService(tile_key=tile_key, filters=self.filters).get_chart()
        return {
            'tile_key': tile_key, 'tile': {'result': chart}
        }

    def tiles_available(self):
        return {
            'movies_count': self.get_movies_count,
            'movies_count_chart': self.get_chart_by_tile_key,
            'avg_rating_by_genre': self.get_chart_by_tile_key
        }

    def get_tiles(self, tile_key=None):
        tiles = []
        if tile_key is None:
            for tile_key, func in self.tiles_available().items():
                tiles.append({'tile_key': tile_key, 'tile': func(tile_key=tile_key)})
        else:
            try:
                return self.tiles_available()[tile_key]()
            except KeyError:
                raise TileNotImplemented(f'Tile {tile_key} is not yet supported.')

        return tiles
