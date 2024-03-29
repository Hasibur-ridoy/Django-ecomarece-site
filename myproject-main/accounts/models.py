from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	phone = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)
	profile_pic = models.ImageField(default="shah.jpg" ,null=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.name or ''   #There was an type error here for str solved it by giving or '' 

class Tag(models.Model):
	
	name = models.CharField(max_length=200, null=True)

	def __str__(self):
		return self.name
		

class Product(models.Model):
	CATAGORY = (
			('Indoor','Indoor'),
			('Out door', 'Out door'),	
		)
	name = models.CharField(max_length=200, null=True)
	price = models.FloatField(null=True)
	catagory = models.CharField(max_length=200, null=True, choices=CATAGORY)
	description = models.CharField(max_length=200, null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	tags = models.ManyToManyField(Tag)

	def __str__(self):
		return self.name 


class Order(models.Model):
	STATUS = (
			('Pending', 'Pending'),
			('Out of delivery', 'Out of delivery'),
			('Delivered', 'Delivered'),
		) 
	customer = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	status = models.CharField(max_length=200, null=True, choices=STATUS)
	note = models.CharField(max_length=1000, null=True)
	
	def __str__(self):
		return self.product.name