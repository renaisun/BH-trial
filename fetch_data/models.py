from django.db import models

class DailyStockPrice(models.Model):
    stock_symbol = models.CharField(max_length=10)
    date = models.DateField()
    open_price = models.DecimalField(max_digits=40, decimal_places=4)
    high_price = models.DecimalField(max_digits=40, decimal_places=4)
    low_price = models.DecimalField(max_digits=40, decimal_places=4)
    close_price = models.DecimalField(max_digits=40, decimal_places=4)
    volume = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['stock_symbol', 'date'], name='unique_stock_code_date')
        ]
        indexes = [
            models.Index(fields=['date'], name='date_idx'),
            models.Index(fields=['stock_symbol'], name='stock_symbol_idx'),
        ]
