from django.db import models
from django.conf import settings
from django.utils.timezone import now

# define category options
category_list = [
    ('praca - zatrudnie', 'praca - zatrudnie'),
    ('prace - poszukuje', 'prace - poszukuje'),
    ('elektronika - kupie', 'elektronika - kupie'),
    ('elektronika - sprzedam', 'elektronika - sprzedam'),
    ('usługi - zlece', 'usługi - zlece'),
    ('usługi - wykonam', 'usługi - wykonam'),
    ('dom - kupie', 'dom - kupie'),
    ('dom - sprzedam', 'dom - sprzedam'),
    ]


# offer model
class Offer(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL)
    title = models.CharField(default='', blank=True, null=True, max_length=200)
    short_description = models.TextField(default='', blank=True, null=True, max_length=200)
    full_description = models.TextField(default='', blank=True, null=True)
    category = models.CharField(max_length=30, choices=category_list)
    display_period = models.IntegerField(default=1)
    display_date = models.DateField(default=now)
    highlight = models.BooleanField(default=False)
    update_date = models.DateField(default=now)

    def __str__(self):
        return str(self.id)

    objects = models.Manager()


# save file model for offer
class SaveFile(models.Model):
    offer = models.ForeignKey(Offer, blank=True, null=True, on_delete=models.CASCADE)
    file = models.FileField(upload_to='graphic/', blank=True, null=True)

    def __str__(self):
        return '%s' % (str(self.offer) + '/' + str(self.file.name))

    objects = models.Manager()
