from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator

class Users(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30)
    email = models.EmailField()
    password = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class Routes(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    is_private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
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
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class AllRoutes(models.Model):
    id = models.AutoField(primary_key=True)
    parent_route_id = models.IntegerField(default=0)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    is_private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
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
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Reviews(models.Model):
    id = models.AutoField(primary_key=True)
    route_id = models.ForeignKey(Routes, on_delete=models.CASCADE)
    rating = models.IntegerField(default=5, validators=[
        MinValueValidator(1),
        MaxValueValidator(5)
    ])
    text = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

