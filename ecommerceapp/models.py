from django.db import models

# Create your models here.


class Contact(models.Model):
    name = models.CharField(max_length=60)
    email = models.EmailField()
    phone = models.IntegerField()
    desc = models.TextField(max_length=500)


    def __str__(self):
        return self.name
    
class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50,default="")
    sub_category = models.CharField(max_length=60,default="")
    price = models.IntegerField(default=0)
    desc = models.TextField(max_length=500)
    image = models.ImageField(upload_to='image/')
    
    def __str__(self):
        return self.product_name