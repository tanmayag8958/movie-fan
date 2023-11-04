def get_filter_query(filters, media):
    from dashboard.services.tiles import Tile
    if not filters:
        return None
    else:
        filter_field_mapping = {
            'star': 'media__stars__name', 'director': 'media__directors__name'
        }
        filter_fields = {}
        for _filter in filters:
            if _filter['value']:
                filter_fields[filter_field_mapping[_filter['name']]] = _filter['value']
        return Tile.get_media_mapping()[media]['model'].objects.filter(**filter_fields)
