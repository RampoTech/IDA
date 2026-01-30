from django.db import models

class SiteSetting(models.Model):
    site_name = models.CharField(max_length=200, default="Ticket System")
    logo = models.ImageField(upload_to='site_logo/', blank=True, null=True)
    primary_color = models.CharField(max_length=7, default="#0d6efd") # Bootstrap Info/Primary
    secondary_color = models.CharField(max_length=7, default="#6c757d") # Bootstrap Secondary

    def __str__(self):
        return self.site_name

    class Meta:
        verbose_name = "Site Setting"
        verbose_name_plural = "Site Settings"

    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and SiteSetting.objects.exists():
            return
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
