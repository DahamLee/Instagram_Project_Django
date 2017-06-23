from django.contrib import admin

from .models import User, Relation


class UserAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, UserAdmin)


class RelationAdmin(admin.ModelAdmin):
    pass


admin.site.register(Relation, RelationAdmin)
