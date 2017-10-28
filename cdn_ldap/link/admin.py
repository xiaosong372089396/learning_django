from django.contrib import admin

# Register your models here.


from link import models


class LinkAdmin(admin.ModelAdmin):

    list_display = ("name", "url")

admin.site.register(models.Link,LinkAdmin)