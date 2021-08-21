from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from .models import User
from .forms import SigUpForm



class AccountAdmin(UserAdmin):
	add_form = SigUpForm

	list_display = ('email','username', 'date_joined', 
		'last_login', 'is_superuser','is_staff', 'is_active')
	search_fields = ('email','username',)
	readonly_fields=('id', 'date_joined', 'last_login')
	fieldsets = (
				('Main', {'classes': ('wide',),'fields': ('id', 'email','username','password')}),
				('Permissions', {'classes': ('collapse',),'fields': ('is_superuser', 'is_staff', 'is_active')}),
				('Extras', {'classes': ('collapse',),'fields': ('bio', 'avatar', 'date_joined', 'last_login')}),
			)
	add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )


	filter_horizontal = ()
	list_filter = ()
	ordering = ('date_joined',)
	


admin.site.register(User, AccountAdmin)
admin.site.unregister(Group)