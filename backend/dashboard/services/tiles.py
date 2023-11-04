from django.db.models import Count, Q, F, Avg
from django_pivot.pivot import pivot

from dashboard.exceptions import TileNotImplemented
from data.models import Movie, Series
from dashboard.services.charts import ChartService
from dashboard.services.utils import get_filter_query


class Tile:

    def __init__(self, media, filters=None):
        self.filters = filters
        self.media = media

    @staticmethod
    def get_media_mapping():
        return {
            'movie': {'model': Movie, 'label': 'Movies', 'year_column_name': 'year'},
            'series': {'model': Series, 'label': 'Series', 'year_column_name': 'start_year'}
        }

    def get_movies_count(self, tile_key):
        query = get_filter_query(self.filters, media=self.media)
        if query is None:
            query = self.get_media_mapping()[self.media]['model'].objects
        result = query.values('media__name').distinct().count()

        return {
            'tile_key': tile_key,
            'tile': {
                'result': {'label': f'Number of {self.get_media_mapping()[self.media]["label"]}:', 'value': result}
            }, 'type': 'count'
        }

    def get_movies_count_chart(self, tile_key):
        query = get_filter_query(self.filters, media=self.media)
        if query is None:
            query = self.get_media_mapping()[self.media]['model'].objects
        result = list(query.values(self.get_media_mapping()[self.media]['year_column_name']).annotate(
            movies_count=Count('media__name', distinct=True)
        ).order_by(self.get_media_mapping()[self.media]['year_column_name']).exclude(
            **{self.get_media_mapping()[self.media]['year_column_name'] + '__in': [None, '']}
        ))
        chart = ChartService(result=result).get_chart()
        return {
            'tile_key': tile_key, 'tile': {'result': chart}, 'type': 'chart'
        }

    def get_avg_rating_by_genre(self, tile_key):
        query = get_filter_query(self.filters, media=self.media)
        if query is None:
            query = self.get_media_mapping()[self.media]['model'].objects
        query_set = query.values(
            self.get_media_mapping()[self.media]['year_column_name'], 'media__genres__name', 'media__rating'
        ).exclude(
            Q(**{self.get_media_mapping()[self.media]['year_column_name'] + '__in': [None, '']})
            | Q(media__genres__name=None)
        ).order_by(
            self.get_media_mapping()[self.media]['year_column_name']
        )
        result = pivot(
            query_set, self.get_media_mapping()[self.media]['year_column_name'],
            'media__genres__name', F('media__rating'), Avg
        )
        chart = ChartService(result=result).get_chart()
        return {
            'tile_key': tile_key, 'tile': {'result': chart}, 'type': 'chart'
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
                return self.tiles_available()[tile_key](tile_key)
            except KeyError:
                raise TileNotImplemented(f'Tile {tile_key} is not yet supported.')

        return tiles
