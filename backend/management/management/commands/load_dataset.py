import csv
import json
import os
import re

from django.conf import settings
from django.core.management.base import BaseCommand

from dashboard.models import Genre, Director, Star, Series, Movie, Media


class Command(BaseCommand):

    @staticmethod
    def get_stars(row):
        stars = set()
        if 'Stars:' in row['STARS']:
            stars.update((star.strip() for star in row['STARS'].strip().split('Stars:')[1].split(',') if star.strip()))

        return stars

    @staticmethod
    def get_directors(row):
        directors = set()
        if 'Director:' in row['STARS'] and '|' in row['STARS']:
            directors.update(
                (
                    star.strip() for star in row['STARS'].strip().split('Director:')[1].split('|')[0].split(',')
                    if star.strip()
                )
            )

        return directors

    @staticmethod
    def get_genres(row):
        genres = set()
        if row['GENRE'].strip():
            genres.update((genre.strip() for genre in row['GENRE'].strip().split(',') if genre.strip()))

        return genres

    @staticmethod
    def create_entities(entities, entity_type):
        entities_mapping = {
            'genres': Genre, 'stars': Star, 'directors': Director
        }
        old_entities = set(entities_mapping[entity_type].objects.all().values_list('name', flat=True))
        new_entities = entities - old_entities
        for entity in new_entities:
            entities_mapping[entity_type].objects.create(name=entity)
        print(f'{len(new_entities)} new {entity_type.title()} added.')

    @staticmethod
    def create_media(medias):
        media_model_mapping = {
            'series': Series, 'movie': Movie
        }
        for media in medias:
            genres = media['media'].pop('genres')
            stars = media['media'].pop('stars')
            directors = media['media'].pop('directors')
            media_instance = Media.objects.create(**media['media'])
            for genre in genres:
                media_instance.genres.add(Genre.objects.get(name=genre))
            for star in stars:
                media_instance.stars.add(Star.objects.get(name=star))
            for director in directors:
                media_instance.directors.add(Director.objects.get(name=director))
            media.pop('media')
            media_type = media.pop('media_type')
            media_model_mapping[media_type].objects.create(
                media=media_instance, **media
            )
        print(f'{len(medias)} new movies and series added.')

    def get_media(self, row):
        year_dict = {}
        if row['YEAR']:
            media_type = 'movie' if '–' not in row['YEAR'] else 'series'
            if media_type == 'movie':
                try:
                    year_dict['year'] = re.search(r"([0-9]+)", row['YEAR']).group(1)
                except AttributeError:
                    pass
            else:
                year_dict['start_year'] = re.search(r"([0-9]+)–", row['YEAR']).group(1)
                year_dict['end_year'] = re.search(r"–([0-9]+)", row['YEAR']).group(1) if re.search(
                    r"–([0-9]+)", row['YEAR']
                ) else None

        return {
            'media': {
                'name': row['MOVIES'].strip(), 'run_time': int(row['RunTime']) if row['RunTime'] else 0,
                'rating': float(row['RATING']) if row['RATING'] else 0,
                'votes': int(row['VOTES'].replace(',', '')) if row['VOTES'] else 0,
                'description': row['ONE-LINE'], 'genres': self.get_genres(row),
                'stars': self.get_stars(row), 'directors': self.get_directors(row)
            }, **year_dict, 'media_type': media_type
        }

    def handle(self, *args, **options):
        with open(
                os.path.join(settings.BASE_DIR, 'management', 'datasets', 'movies.csv'), newline='', encoding="utf8"
        ) as file:
            rows = csv.DictReader(file, delimiter=',')
            genres = set()
            stars = set()
            directors = set()

            medias = []
            for row in rows:
                current_media = self.get_media(row)
                medias.append(current_media)
                genres.update(current_media['media']['genres'])
                stars.update(current_media['media']['stars'])
                directors.update(current_media['media']['directors'])

            self.create_entities(genres, entity_type='genres')
            self.create_entities(stars, entity_type='stars')
            self.create_entities(directors, entity_type='directors')
            self.create_media(medias=medias)

