from IPython.core.displaypub import DisplayPublisher
from django.db import models
import unicodedata

# Create your models here

class Publisher(models.Model):
    name = models.CharField(max_length=50,unique=False)

    def __unicode__(self):
        return self.name

    def get_publisher(self):
        return unicodedata.normalize('NFKD', self.name).encode('ascii','ignore')

    class Meta:
        ordering = ['name']


class Application(models.Model):
    name = models.CharField(max_length=100,unique=False,u)
    version = models.CharField(max_length=30,unique=False)
    publisher = models.ForeignKey(Publisher,unique=False)
    license = models.IntegerField(default=0)
    cost = models.IntegerField(default=0)


    def __unicode__(self):
        return u'%s' % (self.name)

    class Meta:
        ordering = ['name']

    def get_name(self):
        return unicodedata.normalize('NFKD', self.name).encode('ascii','ignore')

    def get_version(self):
        return str(self.version)

    def get_cost(self):
        return str(self.version)

    def get_publisher(self):
        return unicodedata.normalize('NFKD', self.publisher).encode('ascii','ignore')

    def get_license_num(self):
        return self.license

    def get_license_txt(self):
        if  self.license == 1:
            return "Free"
        elif self.license == 2:
            return "Need license"
        return "Unknown"


class Computer(models.Model):
    name = models.CharField(max_length=30,unique=False)
    owner = models.CharField(max_length=100,unique=False)
    applications =  models.ManyToManyField(Application)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']

