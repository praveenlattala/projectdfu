import os
from django.db import models


class Diabetes(models.Model):
    pestimg=models.FileField(upload_to=r'app\static\diabetes')
    
    def Imagename(self):
        return os.path.basename(self.pestimg.name)