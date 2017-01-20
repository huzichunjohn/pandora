from django.contrib import admin
from .models import Domain, Role

class DomainAdmin(admin.ModelAdmin):
    pass

class RoleAdmin(admin.ModelAdmin):
    pass

admin.site.register(Domain)
admin.site.register(Role)
