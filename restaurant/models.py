from django.db import models

# Create your models here.

class Content(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    image = models.ImageField(upload_to='media/img/content/', blank=True, null=True)
    video = models.FileField(upload_to='media/video/', blank=True, null=True)
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Контент"
        verbose_name_plural = "Контент"
        ordering = ['title']


class ContentType(models.Model):
    title = models.CharField(max_length=100)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Тип контента"
        verbose_name_plural = "Типы контента"
        ordering = ['title']