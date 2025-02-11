from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator
from simple_history.models import HistoricalRecords
from authentication.models import User


#class Photo(models.Model):
    #image = models.ImageField(upload_to='images/')


class Route(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, blank=True, null=True)
    #preview = models.ForeignKey(Photo, on_delete=models.CASCADE)
    is_private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()
    points = ArrayField(
        ArrayField(
            models.DecimalField(
                max_digits=22,
                decimal_places=19,
                validators=[
                    MinValueValidator(-180),
                    MaxValueValidator(180)
                ]
            ),
            size=2
        ),
        default=list
    )


    def __str__(self):
        return self.title


class Review(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    route_id = models.ForeignKey(Route, on_delete=models.CASCADE)
    rating = models.IntegerField(default=5, validators=[
        MinValueValidator(1),
        MaxValueValidator(5)
    ])
    text = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)


class Likes(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    route_id = models.ForeignKey(Route, on_delete=models.CASCADE)


class BannedWord(models.Model):
    word = models.CharField(max_length=20)
