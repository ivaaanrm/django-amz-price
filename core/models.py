from django.db import models
from .utils import get_link_product

class Link(models.Model):
    name = models.CharField(max_length=255, blank=True)
    url = models.URLField()
    current_price = models.FloatField(blank=True)
    target_price = models.FloatField(default=0)
    old_price = models.FloatField(default=0)
    
    price_difference = models.FloatField(default=0)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ('price_difference', '-created')

    def save(self, *args, **kwargs):
        name, price = get_link_product(self.url)
        old_price = self.current_price
        if self.current_price:
            if price != old_price:
                self.price_difference = round(price - old_price, 2)
                self.old_price = old_price
        else:
            self.old_price = 0
            self.price_difference = 0
        self.name = name
        self.current_price = price
        super().save(*args, **kwargs)