from django.db import models

# Create your models here.
        
class Laptop (models.Model):
    
    x = [
    ('Laptop', 'Laptop'),
    ('Mobile', 'Mobile'),
    ('Accessories', 'Accessories'),
]
    
    name = models.CharField(max_length=25)
    category = models.CharField(max_length=25,choices=x,default='Laptop')
    price = models.DecimalField(max_digits=8,decimal_places=2)
    content = models.TextField()
    image = models.ImageField(upload_to='photos/%y/%m/%d')
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['price']
        
        
class Mobile (models.Model):
    
    x = [
    ('Laptop', 'Laptop'),
    ('Mobile', 'Mobile'),
    ('Accessories', 'Accessories'),
]
    
    name = models.CharField(max_length=25)
    category = models.CharField(max_length=25,choices=x,default='Mobile')
    price = models.DecimalField(max_digits=8,decimal_places=2)
    content = models.TextField()
    image = models.ImageField(upload_to='photos/%y/%m/%d')
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['price']
        
class Accessories (models.Model):
    
    x = [
    ('Laptop', 'Laptop'),
    ('Mobile', 'Mobile'),
    ('Accessories', 'Accessories'),
]
    
    name = models.CharField(max_length=25)
    category = models.CharField(max_length=25,choices=x,default='Accessories')
    price = models.DecimalField(max_digits=8,decimal_places=2)
    content = models.TextField()
    image = models.ImageField(upload_to='photos/%y/%m/%d')
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['price']
