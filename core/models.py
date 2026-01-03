from django.db import models

# ... baki models ke neeche ...

class Scheme(models.Model):
    title = models.CharField(max_length=200, verbose_name="Yojana Ka Naam")
    description = models.TextField(verbose_name="Choti Jankari")
    link = models.URLField(verbose_name="Website Link (Apply Karne Ke Liye)")
    icon_image = models.ImageField(upload_to='schemes/', verbose_name="Logo/Icon", blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name="Active Hai?")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
