from django.contrib.gis.db import models
from redisearch import Suggestion
from .config import ac, client


class SearchKey(models.Model):
    english_search = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return f"{self.english_search}"

    def save(self, force_insert=False, force_update=False, 
                using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)

        client.redis.hset(
            f'doc:f{self.id}',
            mapping={
            'english_name' : self.english_search,
            'nepali_name' : self.english_search,
            }
        )

        # Adding some terms
        ac.add_suggestions(Suggestion(self.english_search, 1.0))
    
