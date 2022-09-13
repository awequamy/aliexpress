
from django.db import models
from django.contrib.auth import get_user_model
from category.models import Category

User=get_user_model()

class Product(models.Model):
    title=models.CharField(max_length=50)
    description=models.TextField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    category=models.ForeignKey(Category,on_delete=models.CASCADE, related_name='products')
    image=models.ImageField(upload_to='images',null=True,blank=True)

    class Meta:
        ordering=['title']
    def __str__(self):
        return self.title
    

class Likes(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE,related_name='likes')
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='liked')

    class Meta:
        unique_together=['product','user']


class Comments(models.Model):
    
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    product=models.ForeignKey(Product, related_name='comments',on_delete=models.CASCADE)
    body=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.user} -> {self.created_at}'

class Favorites(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE,related_name='favorites')
    user=models.ForeignKey(User, on_delete=models.CASCADE,related_name='favorites')
    class Meta:
        unique_together=['product','user']