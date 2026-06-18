from django.db import models

class Payment(models.Model):
    order_id = models.CharField(max_length=200)
    payment_id = models.CharField(max_length=200, blank=True, null=True)
    amount = models.IntegerField()
    status = models.CharField(max_length=50, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_id