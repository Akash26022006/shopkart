from django.db import models
from django.contrib.auth.models import User
import datetime
import os


# def getFileName(request,filename):
#     now_time =datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
#     new_filename="%s%s"%(now_time,filename)
#     return os.path.join('uploads/',new_filename)
   
    # category/apple.jpg
class Category(models.Model):
    name=models.CharField(max_length=150)
    image=models.ImageField(upload_to="category")
    description=models.TextField(max_length=150)
    status =models.BooleanField(default=False,help_text="0-show,1-Hidden")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100)
    updated_by = models.CharField(max_length=100,null = True,blank=True)


    def __str__(self):
        return self.name

class Product(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    name=models.CharField(max_length=150)
    vendor=models.CharField(max_length=150)
    product_image=models.ImageField(upload_to="products")
    quantity=models.IntegerField()
    original_price=models.FloatField()
    selling_price=models.FloatField()
    description=models.TextField(max_length=150)
    status =models.BooleanField(default=False)
    trending=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100)
    updated_by = models.CharField(max_length=100,null = True,blank=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    product_qty=models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100)
    updated_by = models.CharField(max_length=100,null = True,blank=True)


"""class Orders(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    contact = models.CharField(max_length=10, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    address = models.TextField(blank=True, null=True)
    count = models.IntegerField(default=1)
    cost = models.IntegerField(default=0)
    delivered = models.BooleanField(default=False)
    delivered_on = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name()"""

 
class Favourite(models.Model):
    
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100)
    updated_by = models.CharField(max_length=100,null = True,blank=True)

	
class Order(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    # fname = models.CharField(max_length=150, null=False)
    # lname = models.CharField(max_length=150, null=False)
    # email = models.CharField(max_length=150, null=False)
    phone = models.CharField(max_length=150)
    address = models.TextField()
    city = models.CharField(max_length=150)
    state= models.CharField(max_length=150)
    country= models.CharField(max_length=150)
    pincode= models.CharField(max_length=150)
    total_price = models.FloatField()
    payment_mode=models.CharField(max_length=150)
    # payment_id=models.CharField(max_length=250, null=True)
    product = models.CharField(max_length = 100)
    # ['mobile','lunch','','']
    #quantity=models.CharField(max_length =10,null=False)
    
    status=models.CharField(max_length=150,default='Pending')
    message=models.TextField(null=True)
    tracking_no=models.CharField(max_length=250, null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100)
    updated_by = models.CharField(max_length=100,null = True,blank=True)

    def __str__(self):
        return '{} - {}'.format(self.id,self.tracking_no)
    # 1 - 000001

# class OrderItem(models.Model):
#     order=models.ForeignKey(User,on_delete=models.CASCADE)
#     product=models.ForeignKey(Product,on_delete=models.CASCADE)
#     price=models.FloatField(null=False)
#     quatity=models.IntegerField(null=False)

#     def __str__(self):
#         return '{} {}'.format(self.order.id,self.order.tracking_) 

