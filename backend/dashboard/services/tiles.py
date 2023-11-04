from django.db.models import Count, Q, F, Avg
from django_pivot.pivot import pivot

from dashboard.exceptions import TileNotImplemented
from data.models import Movie
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

    def get_movies_count_chart(self, tile_key):
        query = get_filter_query(self.filters)
        if not query:
            query = Movie.objects
        result = list(query.values('year').annotate(
            movies_count=Count('media__name', distinct=True)
        ).order_by('year').exclude(year__in=[None, '']))
        chart = ChartService(result=result).get_chart()
        return {
            'tile_key': tile_key, 'tile': {'result': chart}
        }

    def get_avg_rating_by_genre(self, tile_key):
        query = get_filter_query(self.filters)
        if not query:
            query = Movie.objects
        query_set = query.values(
            'year', 'media__genres__name', 'media__rating'
        ).exclude(Q(year__in=[None, '']) | Q(media__genres__name=None)).order_by('year')
        result = pivot(query_set, 'year', 'media__genres__name', F('media__rating'), Avg)
        chart = ChartService(result=result).get_chart()
        return {
            'tile_key': tile_key, 'tile': {'result': chart}
        }

    def tiles_available(self):
        return {
            'movies_count': self.get_movies_count,
            'movies_count_chart': self.get_movies_count_chart,
            'avg_rating_by_genre': self.get_avg_rating_by_genre
        }

    def get_tiles(self, tile_key=None):
        tiles = []
        if tile_key is None:
            for tile_key, func in self.tiles_available().items():
                tiles.append(func(tile_key=tile_key))
        else:
            try:
                return self.tiles_available()[tile_key]()
            except KeyError:
                raise TileNotImplemented(f'Tile {tile_key} is not yet supported.')

        return tiles
