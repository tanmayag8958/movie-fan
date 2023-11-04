from django.db.models import Count, Avg, Q, F
from django_pivot.pivot import pivot

from dashboard.exceptions import TileNotImplemented
from dashboard.models import Movie
from dashboard.services.utils import get_filter_query


class ChartService:
    def __init__(self, result):
        self.result = result

    @staticmethod
    def base_options_object():
        return {
            'scales': {
                'y': {
                    'position': 'left',
                    'ticks': {'color': "#b6baca"},
                    'grid': {'drawTicks': False, 'color': '#999999'},
                    'border': {'dash': [2, 10]},
                },
                'x': {
                    'ticks': {'color': "#b6baca"},
                    'grid': {'display': False},
                    'border': {'display': False},
                },
            },
            'interaction': {'intersect': False}
        }

    @staticmethod
    def base_dataset_object():
        return {
            'label': '',
            'backgroundColor': '#F5D257',
            'borderColor': '#F5D257',
            'pointRadius': 4,
            'tension': 0.3,
            'data': [],
            'yAxisID': 'y',
        }

    def base_chart_object(self):
        return {
            'data': {
                'labels': [],
                'datasets': []
            },
            'options': self.base_options_object()
        }

    def get_chart_object(self):
        chart_object = self.base_chart_object()
        for index, column_name in enumerate(self.result[0].keys()):
            if index == 0:
                chart_object['data']['labels'] = [row[column_name] for row in self.result]
            else:
                dataset_object = self.base_dataset_object()
                dataset_object['label'] = column_name
                dataset_object['data'] = [row[column_name] for row in self.result]
                chart_object['data']['datasets'].append(dataset_object)
        return chart_object

    def get_chart(self):
        return self.get_chart_object()
