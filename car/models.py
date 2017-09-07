from django.db import models
from django.utils.text import slugify
from django.core.urlresolvers import reverse
from datetime import datetime

# Create your models here.
class Driver(models.Model):
    name = models.CharField("姓名",max_length=50)

    class Meta:
        verbose_name_plural="司机列表"
        db_table = "car_driver"

    def __str__(self):
        return self.name

class Saler(models.Model):
    name = models.CharField("姓名",max_length=50)

    class Meta:
        verbose_name_plural="售票员列表"
        db_table = "car_saler"

    def __str__(self):
        return self.name

class DriverSalary(models.Model):
    name = models.OneToOneField(Driver,verbose_name="姓名",related_name='driversalary')
    salary = models.FloatField("工资",default=6000.00)
    borrow = models.FloatField("借钱",default=0,blank=True,null=True)
    real_salary = models.FloatField("实际工资",default=6000.00)
    date = models.DateField("日期",auto_now_add=True)
    time = models.DateField("请假开始日期")
    days = models.IntegerField("请假天数")
    reason = models.TextField("请假原因",blank=True,null=True)

    class Meta:
        verbose_name_plural = '司机工资列表'
        db_table = "car_driver_salary"
        ordering = ("salary",)

    def save(self):
        self.real_salary = int(self.salary)-int(self.borrow)-int(self.days)*200
        super(DriverSalary,self).save()

    def __str__(self):
        return self.name.name

class SalerSalary(models.Model):
    name = models.OneToOneField(Saler,verbose_name="姓名",related_name='salersalary')
    salary = models.FloatField("工资",default=2500.00)
    borrow = models.FloatField("借钱",default=0,blank=True,null=True)
    real_salary = models.FloatField("实际工资",default=2500.00)
    date = models.DateField("日期",auto_now_add=True)
    time = models.DateField("请假开始日期")
    days = models.IntegerField("请假天数")
    reason = models.TextField("请假原因",blank=True,null=True)

    class Meta:
        verbose_name_plural='售票员工资列表'
        db_table = "car_saler_salary"
        ordering = ("salary",)

    def save(self):
        self.real_salary = int(self.salary)-int(self.borrow)-int(self.days)*100
        super(SalerSalary,self).save()

    def __str__(self):
        return self.name.name


class Car(models.Model):
    car_choices = (
        ("2287","豫 A2287"),
        ('5658',"豫 A5658"),
        ("9809","豫 A9809"))
    date = models.DateField("运行日期",auto_now_add=True)
    name = models.CharField('车名',max_length=20,choices=car_choices,default="2287",unique_for_date='date')
    slug = models.SlugField("标签", max_length=200, blank=True)
    driver = models.ForeignKey(Driver,verbose_name='司机',related_name="cars",related_query_name='car', on_delete=models.CASCADE)
    saler = models.ForeignKey(Saler,verbose_name='售票员',related_name="cars",related_query_name='car',on_delete=models.CASCADE)
    total_income = models.FloatField("总收入")
    real_income = models.FloatField("净收入")
    total_people = models.IntegerField("总人数")
    oil = models.FloatField('油钱',default=0)
    people_30 = models.IntegerField("30元票价人数",default=0)
    people_40 = models.IntegerField("40元票价人数",default=0)
    things = models.IntegerField("货钱",default=0)
    food = models.IntegerField("饭钱及其他额外花销",default=0)

    class Meta:
        verbose_name_plural = "车辆列表"
        db_table = "car"
        ordering = ("-date",)

    def save(self):
        if not self.slug:
            self.slug = slugify(self.name)
            super(Car,self).save()

    def get_absolute_url(self):
        dt = self.date
        dt_year = datetime.strftime(dt,"%Y")
        dt_month = datetime.strftime(dt,"%m")
        dt_day = datetime.strftime(dt,"%d")
        return reverse("car:car_detail", args=(dt_year,dt_month,dt_day,self.name))

    def __str__(self):
        return self.name

    def as_dict(self): #这个方法是为了让DataTable展示数据的，这些都是要展示的值
        return {'date':self.date.strftime('%Y-%m-%d'),'name':self.name,'driver':self.driver.name,'saler':self.saler.name,\
                'total_income':str(self.total_income)+" 元","real_income":str(self.real_income)+" 元","total_people":str(self.total_people)+" 人",\
                'oil':str(self.oil)+" 元","detail":"<a href="+self.get_absolute_url()+">豫A "+self.slug+"</a>"}


