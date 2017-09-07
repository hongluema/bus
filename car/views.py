from django.shortcuts import render
from .models import Car,Saler,SalerSalary,Driver,DriverSalary
from .forms import CarForm, DateForm,RealMoneyForm
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, get_list_or_404
from django.shortcuts import reverse
from datetime import datetime
import json
# Create your views here.

from django.core.paginator import Paginator
from django.views.generic import View, TemplateView, ListView

def test(request):
    print("request",request.POST)
    return HttpResponse("ok")

#解释说明：
"""
TemplateView自带的有一个GET请求的方法，返回的网页就是template_name = "user/userlist.html"，网页里面的传的数据内容可以通过重写get_context_data这个方法来获取，django自己写分页的话是利用列表的切片，类似于mysql的limit和offset，这里是引用自带的分页模块
"""
class CarView(TemplateView):
    template_name = "car/car_index.html"
    def get_context_data(self, **kwargs):
        #这个方法就可以将变量传到模板里
        context = super(CarView, self).get_context_data(**kwargs)
        try:
            page = int(self.request.GET.get("page","1")) #这里做了异常处理，如果page是字符，就会变成下面的page=1
        except:
            page = 1
        paginator = Paginator(Car.objects.all(),10)
        page_obj = paginator.page(page) #这个page_obj是为了和自带的方法保持一致
        context["object_list"] = page_obj.object_list # page_obj.object_list是要获得的
        context["page_obj"] = page_obj # page_obj 也是要获得的
        return context



def car_detail(request, year, month, day, name):
    car = get_object_or_404(Car,slug=name,\
                            date__year=year,\
                            date__month=month,\
                            date__day=day)
    content = {'car':car}
    return render(request,'car/car_detail.html',content)

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def car_detail_ajax(request):
    if request.method == "POST":
        print("post")
        money = float(request.POST.get("money",0).strip())
        real_income = float(request.POST.get("real_income",0).strip())
        warning = '''
        <div class="alert alert-warning alert-dismissible" role="alert">
  <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>
  <strong>警告!</strong> <strong>实际金额低</strong>于应有收入，请核对看是否有问题.
</div>
        '''
        well = '''
        <div class="alert alert-success alert-dismissible" role="alert">
  <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>
  <strong>警告!</strong> <strong>实际金额高</strong>于应有收入，请核对看是否有问题.
</div>
        '''
        normal = '''
        <div class="alert alert-info alert-dismissible" role="alert">
  <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>
  <strong>正确!</strong> 实际金额等于应有收入，账单没什么问题.
</div>
        '''
        if money < real_income:
            return HttpResponse(warning)
        elif money > real_income:
            return HttpResponse(well)
        else:
            return HttpResponse(normal)
    print("get")
    return render(request,'car/car_detail.html')

#
# def car_create(request):
#     if request.method == "POST":
#         form = CarForm(request.POST,initial={"name":""})
#         print("POST")
#         if form.is_valid():
#             cd = form.cleaned_data
#             name = cd.get("name","")
#             driver = cd.get("driver","")
#             d = get_object_or_404(Driver,name__contains =driver)
#             saler = cd.get("saler","")
#             s = get_object_or_404(Saler, name__contains=saler)
#             people_30 = int(cd.get("people_30",0))
#             people_40 = int(cd.get("people_40",0))
#             food = cd.get("food",0)
#             things = cd.get("things",0)
#             oil = int(cd.get("oil",0))
#             total_income = int(people_40)*40+int(people_30)*30+int(things)
#             real_income = int(people_40)*40+int(people_30)*30+int(things)-int(food)
#             total_people = int(people_30)+int(people_40)
#             car = Car(name=name,total_income=total_income,oil=oil,total_people=total_people,\
#                       real_income=real_income,saler=s,driver=d,people_30=people_30,\
#                       people_40=people_40,food=food,things=things)
#             car.save()
#             print(cd)
#             return HttpResponseRedirect(reverse('car:car_index'))
#     else:
#         form = CarForm(initial={"name":""})
#     return render(request, "car/run_create.html",{'form':form})

# ajax创建车辆每日运行信息
def car_create_ajax(request):
    form = CarForm(request.POST)
    if form.is_valid():
        print("POST")
        cd = form.cleaned_data
        name = cd.get("name","")
        driver = cd.get("driver","")
        d = get_object_or_404(Driver,name__contains =driver)
        saler = cd.get("saler","")
        s = get_object_or_404(Saler, name__contains=saler)
        people_30 = int(cd.get("people_30",0))
        people_40 = int(cd.get("people_40",0))
        food = cd.get("food",0)
        things = cd.get("things",0)
        oil = int(cd.get("oil",0))
        total_income = int(people_40)*40+int(people_30)*30+int(things)
        real_income = int(people_40)*40+int(people_30)*30+int(things)-int(food)
        total_people = int(people_30)+int(people_40)
        car = Car(name=name,total_income=total_income,oil=oil,total_people=total_people,\
                  real_income=real_income,saler=s,driver=d,people_30=people_30,\
                  people_40=people_40,food=food,things=things)
        car.save()
        return JsonResponse({"status":200,"result":""})
    else:
        return JsonResponse({"status":400,'result':"",'errors':json.loads(form.errors.as_json())})

# 使用DataTable插件获取车辆信息
def get_car_info_ajax(request):
    cars = Car.objects.all()
    cars = [ car.as_dict() for car in cars]
    return JsonResponse({"data":cars})

#通过ajax获取每年的运营数据
def ajax_by_year(request):
    year = request.GET.get("year","2017")
    year_data = get_list_or_404(Car,date__year=year) #某一年的所有车辆数据
    dict_month = {}#该年的每个月的车辆的数据，月份为key，数据为value
    for i in year_data:
        # dict_month[i.date.month] = dict_month.get(i.date.month,[])+[(i.total_income,i.oil)]
        if i.date.month in dict_month:
            dict_month.get(i.date.month).append(((i.name,i.total_income,i.oil)))
        else:
            dict_month.setdefault(i.date.month,[(i.name,i.total_income,i.oil)])
    print(dict_month)
    dict_car ={}
    for m in dict_month:
        dict_car[m] ={}
        print('m','-->',m)
        for c in dict_month[m]:
            print('c','-->',c)
            if c[0] in dict_car[m]:
                print(dict_car[m],"-->",c)
                dict_car[m][c[0]] = (dict_car[m][c[0]][0]+c[1],dict_car[m][c[0]][1]+c[2])
            else:
                dict_car[m][c[0]] = (c[1],c[2])
    print('sum','-->',dict_car)
    return JsonResponse(dict_car)


from django.db.models import Q

class CarSearchView(TemplateView):
    template_name = "car/car_search.html"

    def get_context_data(self, **kwargs):
        #这个方法就可以将变量传到模板里
        context = super(CarSearchView, self).get_context_data(**kwargs)
        try:
            page = int(self.request.GET.get("page","1")) #这里做了异常处理，如果page是字符，就会变成下面的page=1
        except:
            page = 1
        keywords = self.request.GET.get("search", "")
        search_all = get_list_or_404(Car, Q(name__contains=keywords) | Q(driver__name__contains=keywords)|Q(saler__name__contains=keywords))
        print(search_all)
        paginator = Paginator(search_all,1)
        page_obj = paginator.page(page) #这个page_obj是为了和自带的方法保持一致
        context["object_list"] = page_obj.object_list # page_obj.object_list是要获得的
        context["page_obj"] = page_obj # page_obj 也是要获得的
        context['keywords'] = keywords
        return context

def static_car(request):
    if request.method == "POST":
        form = DateForm(request.POST, initial={"date":datetime.today()})
        if form.is_valid():
            cd = form.cleaned_data
            date_str = request.POST.get('date',datetime.today())
            print("date",date_str)
            date = datetime.strptime(date_str,'%Y-%m-%d')
            year = date.year
            month = date.month
            month_all = get_list_or_404(Car, date__year=year, date__month=month)
            print(month_all)
            return HttpResponseRedirect(reverse('car:static_car_month', args=(year,month)))
    else:
        form = DateForm()
    return render(request,"car/static_car.html",{"form":form})

def static_car_month(request,year,month):
    month_all = get_list_or_404(Car, date__year=year, date__month=month)
    try:
        page = int(request.GET.get("page", "1"))  # 这里做了异常处理，如果page是字符，就会变成下面的page=1
    except:
        page = 1
    paginator = Paginator(month_all, 3)
    page_obj = paginator.page(page)  # 这个page_obj是为了和自带的方法保持一致
    context = {}
    context["object_list"] = page_obj.object_list  # page_obj.object_list是要获得的
    context["page_obj"] = page_obj  # page_obj 也是要获得的
    return render(request, 'car/static_car_month.html', context)

#按年分
def car_by_year(request):
    year_all = Car.objects.all()
    years = list(set([i.date.year for i in year_all]))

    try:
        page = int(request.GET.get("page", "1"))  # 这里做了异常处理，如果page是字符，就会变成下面的page=1
    except:
        page = 1
    print(years)
    paginator = Paginator(years, 3)
    page_obj = paginator.page(page)  # 这个page_obj是为了和自带的方法保持一致
    context = {}
    context["object_list"] = page_obj.object_list  # page_obj.object_list是要获得的
    context["page_obj"] = page_obj  # page_obj 也是要获得的
    return render(request, 'car/car_by_year.html', context)

def car_by_year_detail(request,year):
    cars = get_list_or_404(Car, date__year=year)
    names = list(set([i.name for i in cars]))
    total_incomes = sum([i.total_income for i in cars])
    real_incomes = sum([i.real_income for i in cars])
    people_30s = sum([i.people_30 for i in cars])
    people_40s = sum([i.people_40 for i in cars])
    total_peoples = sum([i.total_people for i in cars])
    things = sum([i.things for i in cars])
    oils = sum([i.oil for i in cars])
    foods = sum([i.food for i in cars])

    for i in range(len(names)):
        son_cars = get_list_or_404(Car, date__year=year, name__contains=names[i])
        names[i] = {
            "year":year,
            "name":names[i],
            "total_income": sum([i.total_income for i in son_cars]),
            "real_income":sum([i.real_income for i in son_cars]),
            "people_30":sum([i.people_30 for i in son_cars]),
            "people_40":sum([i.people_40 for i in son_cars]),
            "total_people":sum([i.total_people for i in son_cars]),
            "things":sum([i.things for i in son_cars]),
            "oil":sum([i.oil for i in son_cars]),
            "food":sum([i.food for i in son_cars]),
        }
    content={
        "names":names,
        "year":year,
        "total_income":total_incomes,
        "real_income":real_incomes,
        "people_30":people_30s,
        "people_40":people_40s,
        "total_people":total_peoples,
        "things":things,
        "oil":oils,
        "food":foods,

    }
    print(content)
    return render(request,'car/car_by_year_detail.html',content)

#按月分
def car_by_month(request):
    month_all = Car.objects.all()
    years_months = list(set([(i.date.year,i.date.month) for i in month_all]))

    try:
        page = int(request.GET.get("page", "1"))  # 这里做了异常处理，如果page是字符，就会变成下面的page=1
    except:
        page = 1
    print(years_months)
    paginator = Paginator(years_months, 3)
    page_obj = paginator.page(page)  # 这个page_obj是为了和自带的方法保持一致
    context = {}
    context["object_list"] = page_obj.object_list  # page_obj.object_list是要获得的
    context["page_obj"] = page_obj  # page_obj 也是要获得的
    return render(request, 'car/car_by_month.html', context)

def car_by_month_detail(request,year, month):
    cars = get_list_or_404(Car, date__year=year, date__month=month)
    names = list(set([i.name for i in cars]))
    total_incomes = sum([i.total_income for i in cars])
    real_incomes = sum([i.real_income for i in cars])
    people_30s = sum([i.people_30 for i in cars])
    people_40s = sum([i.people_40 for i in cars])
    total_peoples = sum([i.total_people for i in cars])
    things = sum([i.things for i in cars])
    oils = sum([i.oil for i in cars])
    foods = sum([i.food for i in cars])

    for i in range(len(names)):
        son_cars = get_list_or_404(Car, date__year=year,date__month=month, name__contains=names[i])
        names[i] = {
            "year":year,
            "month":month,
            "name":names[i],
            "total_income": sum([i.total_income for i in son_cars]),
            "real_income":sum([i.real_income for i in son_cars]),
            "people_30":sum([i.people_30 for i in son_cars]),
            "people_40":sum([i.people_40 for i in son_cars]),
            "total_people":sum([i.total_people for i in son_cars]),
            "things":sum([i.things for i in son_cars]),
            "oil":sum([i.oil for i in son_cars]),
            "food":sum([i.food for i in son_cars]),
        }
    content={
        "names":names,
        "year":year,
        "month": month,
        "total_income":total_incomes,
        "real_income":real_incomes,
        "people_30":people_30s,
        "people_40":people_40s,
        "total_people":total_peoples,
        "things":things,
        "oil":oils,
        "food":foods,

    }
    print(content)
    return render(request,'car/car_by_month_detail.html',content)

#按天分
def car_by_day(request):
    day_all = Car.objects.all()
    years_months = list(set([(i.date.year,i.date.month,i.date.day) for i in day_all]))

    try:
        page = int(request.GET.get("page", "1"))  # 这里做了异常处理，如果page是字符，就会变成下面的page=1
    except:
        page = 1
    print(years_months)
    paginator = Paginator(years_months, 3)
    page_obj = paginator.page(page)  # 这个page_obj是为了和自带的方法保持一致
    context = {}
    context["object_list"] = page_obj.object_list  # page_obj.object_list是要获得的
    context["page_obj"] = page_obj  # page_obj 也是要获得的
    return render(request, 'car/car_by_day.html', context)

def car_by_day_detail(request,year, month,day):
    cars = get_list_or_404(Car, date__year=year, date__month=month,date__day=day)
    names = list(set([i.name for i in cars]))
    total_incomes = sum([i.total_income for i in cars])
    real_incomes = sum([i.real_income for i in cars])
    people_30s = sum([i.people_30 for i in cars])
    people_40s = sum([i.people_40 for i in cars])
    total_peoples = sum([i.total_people for i in cars])
    things = sum([i.things for i in cars])
    oils = sum([i.oil for i in cars])
    foods = sum([i.food for i in cars])

    for i in range(len(names)):
        son_cars = get_list_or_404(Car, date__year=year,date__month=month,date__day=day, name__contains=names[i])
        names[i] = {
            "year":year,
            "month":month,
            "day":day,
            "name":names[i],
            "total_income": sum([i.total_income for i in son_cars]),
            "real_income":sum([i.real_income for i in son_cars]),
            "people_30":sum([i.people_30 for i in son_cars]),
            "people_40":sum([i.people_40 for i in son_cars]),
            "total_people":sum([i.total_people for i in son_cars]),
            "things":sum([i.things for i in son_cars]),
            "oil":sum([i.oil for i in son_cars]),
            "food":sum([i.food for i in son_cars]),
        }
    content={
        "names":names,
        "year":year,
        "month": month,
        "day":day,
        "total_income":total_incomes,
        "real_income":real_incomes,
        "people_30":people_30s,
        "people_40":people_40s,
        "total_people":total_peoples,
        "things":things,
        "oil":oils,
        "food":foods,

    }
    print(content)
    return render(request,'car/car_by_day_detail.html',content)

def driver(request):
    drivers = Driver.objects.all()
    print(drivers)
    context = {}
    context["object_list"] = drivers
    return render(request,'car/driver.html', context)

def driver_salary(request, name):
    drivers_salary = get_list_or_404(DriverSalary, name__name =name)
    print(drivers_salary)
    context = {}
    context["object_list"] = drivers_salary
    context["name"] = name
    return render(request,'car/driver_salary.html', context)

def driver_salary_list(request):
    drivers_salary = get_list_or_404(DriverSalary)
    print(drivers_salary)
    context = {}
    context["object_list"] = drivers_salary
    return render(request,'car/driver_salary_list.html', context)

def saler(request):
    salers = Saler.objects.all()
    print(salers)
    context = {}
    context["object_list"] = salers
    return render(request,'car/saler.html', context)

def saler_salary(request, name):
    salers_salary = get_list_or_404(SalerSalary, name__name =name)
    print(salers_salary)
    context = {}
    context["object_list"] = salers_salary
    context["name"] = name
    return render(request,'car/saler_salary.html', context)

def saler_salary_list(request):
    salers_salary = get_list_or_404(SalerSalary)
    print(salers_salary)
    context = {}
    context["object_list"] = salers_salary
    return render(request,'car/saler_salary_list.html', context)
