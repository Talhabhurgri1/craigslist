from django.db import models

# Create your models here.
class Search(models.Model):
    searches = models.CharField(max_length=200)
    search_date = models.DateTimeField('Search_Done',auto_now=True)
    
    def __str__(self):
        return '{0}'.format(self.searches)
        