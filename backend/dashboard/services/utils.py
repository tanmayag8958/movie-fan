from data.models import Movie


def get_filter_query(filters):
    if not filters:
        return None
    else:
        filter_field_mapping = {
            'star': 'media__stars__name', 'director': 'media__directors__name'
        }
        filter_fields = {}
        for _filter in filters:
            filter_fields[filter_field_mapping[_filter['name']]] = _filter['value']
        return Movie.objects.filter(**filter_fields)
