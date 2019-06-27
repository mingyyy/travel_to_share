from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,ProfileTraveler, ProfileHost, Program, Link, Language, Topic, Space
from .models import User
# Register your models here.


admin.site.register(User, UserAdmin)
admin.site.register(ProfileTraveler)
admin.site.register(ProfileHost)
admin.site.register(Program)
admin.site.register(Language)

admin.site.register(Space)
admin.site.register(Topic)
admin.site.register(Link)




