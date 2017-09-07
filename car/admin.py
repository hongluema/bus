from django.contrib import admin
from .models import Saler, Driver, Car, DriverSalary, SalerSalary

# Register your models here.


class SalerSalaryAdmin(admin.ModelAdmin):
    list_display = ("name","salary","borrow","real_salary","time", "days", "reason")
    list_filter = ("name","time", "days", "reason")
    search_fields = ("name", "days")
    actions_selection_counter = True
    # date_hierarchy
class DriverSalaryAdmin(admin.ModelAdmin):
    list_display = ("name","salary","borrow","real_salary","time", "days", "reason")
    list_filter = ("name","time", "days")
    search_fields = ("name",'days')
    actions_selection_counter = True

class SalerAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_filter = ("name",)
    search_fields = ("name",)

class DriverAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_filter = ("name",)
    search_fields = ("name",)

class CarAdmin(admin.ModelAdmin):
    list_display = ("name",'date','driver','saler','oil','total_people','real_income','total_income')
    list_filter = ("name",'date','driver','saler')
    search_fields = ("name",'driver','saler')
    actions_selection_counter = True
    date_hierarchy = 'date'

admin.site.register(DriverSalary, DriverSalaryAdmin)
admin.site.register(Driver, DriverAdmin)
admin.site.register(SalerSalary, SalerSalaryAdmin)
admin.site.register(Saler, SalerAdmin)
admin.site.register(Car, CarAdmin)