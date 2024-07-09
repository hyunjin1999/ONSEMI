from django.db import models
from django.urls import reverse
from autoslug import AutoSlugField
from django.utils.text import slugify
from auth_app.models import User

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='name', unique=True, always_update=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop_app:product_list_by_category',
                       args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='name', unique=True, always_update=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=0)  # 소수점 없이 원화로 표시
    stock = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='product_likes', blank=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop_app:product_detail',
                       args=[self.id, self.slug])
    
    def reduce_stock(self, quantity): # 주문하면 그 숫자 만큼 재고가 줄어들음
        if self.stock >= quantity:
            self.stock -= quantity
            self.save()
        else:
            raise ValueError("재고가 부족합니다.")
        
    def total_likes(self):
        return self.likes.count()
        
# 후기
class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    likes = models.ManyToManyField(User, related_name='comment_likes', blank=True)
    rating = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.content[:20]  # 첫 20자를 반환

    def total_likes(self):
        return self.likes.count()