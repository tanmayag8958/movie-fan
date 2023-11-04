import random


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
            'legend': {
                'labels': {
                    'fontColor': "white",
                    'fontSize': 18
                }
            },
            'interaction': {'intersect': False}
        }

    @staticmethod
    def base_dataset_object():
        return {
            'label': '',
            'backgroundColor': '',
            'borderColor': '',
            'hoverBackgroundColor': "white",
            'hoverBorderColor': "white",
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
        if not self.result:
            return {}
        for index, column_name in enumerate(self.result[0].keys()):
            if index == 0:
                chart_object['data']['labels'] = [row[column_name] for row in self.result]
            else:
                dataset_object = self.base_dataset_object()
                dataset_object['label'] = column_name
                dataset_object['data'] = [row[column_name] for row in self.result]
                dataset_object['borderColor'] = dataset_object['backgroundColor'] = "#" + ''.join(
                    [random.choice('0123456789ABCDEF') for j in range(6)]
                )
                chart_object['data']['datasets'].append(dataset_object)
        return chart_object

    def get_chart(self):
        return self.get_chart_object()
