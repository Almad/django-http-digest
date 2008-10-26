from django.db import models

class ClearTextModel(models.Model):
    realm = models.CharField(max_length=30)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    
class ModelWithDefaultRealm(models.Model):
    username = models.CharField(max_length=30)
    secret = models.CharField(max_length=50)

class ModelWithRealmSet(models.Model):
    realm = models.CharField(max_length=30)
    username = models.CharField(max_length=30)
    secret = models.CharField(max_length=50)
    
    def __unicode__(self):
        return u"<ModelWithRealmSet realm=%s, username=%s>" % (self.realm, self.username)
