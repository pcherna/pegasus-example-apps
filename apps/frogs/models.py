from django.db import models
from django.urls import reverse
from apps.utils.models import BaseModel

class Frog(BaseModel):
    # 'name' and 'number' are just example fields, visible in the List and Detail views
    name = models.CharField('Name', max_length=200)
    number = models.IntegerField('Number', default=0)
    # 'notes' is another example field that we will only show in the Detail view
    notes = models.TextField('Notes', max_length=4096, blank=True, default='')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('frogs:frog-detail', kwargs={'pk': self.pk})
