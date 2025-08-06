from django.db import models

class AnalyticsResult(models.Model):
    month1 = models.CharField(max_length=3)
    month2 = models.CharField(max_length=3)
    value1 = models.FloatField()
    value2 = models.FloatField()
    chart_image = models.ImageField(upload_to='charts/')
    created_at = models.DateTimeField(auto_now_add=True)