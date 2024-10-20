from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
  # Links a customer to a Django User (used for authentication). It's a one-to-one relationship, meaning each customer has exactly one user account.
  # CASCADE means if a user is deleted, the corresponding Customer instance will also be deleted.
  # null=True: it can be empty in the database.
  # blank=True：The field can be left blank in forms (it's not required to be filled).
  user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
  name = models.CharField(max_length=200, null=True)
  email = models.CharField(max_length=200, null=True)

  def __str__(self):
    return self.name
  

class Product(models.Model):
  name = models.CharField(max_length=200)
  price = models.DecimalField(max_digits=7,decimal_places=2)
  # This is a field that stores a True/False value (a boolean). In this case, it indicates whether the product is digital 
  digital = models.BooleanField(default=False, blank=True, null=True)
  image = models.ImageField(null=True, blank=True)

  def __str__(self):
    return self.name
  
  @property
  def imageURL(self):
    try:
      url = self.image.url
    except:
      url = ''
    return url
  
class Order(models.Model):
  #  This creates a relationship between the Order model and the Customer model. It links each order to a customer, meaning an order can only belong to one customer.
  #  if a customer is deleted, the customer field in the Order will be set to NULL, meaning the order will not be linked to any customer.
  customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
  # This automatically sets the field to the current date and time when a new order is created, and it cannot be changed later.
  date_ordered = models.DateTimeField(auto_now_add=True)
  # This is a True/False field that indicates whether the order is complete.
  complete = models.BooleanField(default=False)
  transaction_id = models.CharField(max_length=100, null=True)

  def __str__(self):
    return f'Order {self.id}'
  
  @property
  def shipping(self):
    shipping = False
    orderitems = self.orderitem_set.all()
    for i in orderitems:
      if i.product.digital == False:
        shipping = True
    return shipping 
  
  @property
  def get_cart_total(self):
    orderitems = self.orderitem_set.all()
    total = sum([item.get_total for item in orderitems])
    return total
  
  @property
  def get_cart_items(self):
    orderitems = self.orderitem_set.all()
    total = sum([item.quantity for item in orderitems])
    return total
  

'''
The OrderItem model connects individual products to a specific order, allowing you to track how many of each product were purchased.
'''  
class OrderItem(models.Model):
  # This establishes a foreign key relationship with the Product model, linking each OrderItem to a specific product. An order item can only refer to one product, but multiple OrderItem instances can reference the same product.
  product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
  # This establishes a relationship with the Order model. Each OrderItem is linked to a specific order, but an order can contain many OrderItem objects 
  order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
  quantity = models.IntegerField(default=0, null=True, blank=True)
  date_added = models.DateTimeField(auto_now_add=True)

  #  allows this method to be accessed as an attribute
  @property
  def get_total(self):
    total = self.product.price * self.quantity
    return total

  '''Example Scenario
      Let's say a customer orders 3 units of a product called "Laptop" and 2 units of a product called "Mouse."
      In this case, there would be two OrderItem objects:
          One for the "Laptop" with a quantity of 3.
          Another for the "Mouse" with a quantity of 2.
      Both OrderItem objects would reference the same Order object, representing the entire transaction for the customer.
  '''

class ShippingAddress(models.Model):
  customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
  order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
  address = models.CharField(max_length=200, null=False)
  city = models.CharField(max_length=100, null=False, default="Unknown")
  state = models.CharField(max_length=200, null=False)
  zipcode = models.CharField(max_length=200, null=False)
  date_added = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.address