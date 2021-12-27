from django.shortcuts import render
import requests
from .utils import *


def HomeView(request):
    ics_id =request.POST.get('ics')
    if ics_id:
         request.session['ics']=ics_id
    try:
        id= request.session['ics'] or request.POST.get('ics_id')
        request.session['ics']=id
            
        url = f"https://e-uczelnia.ue.katowice.pl/wsrest/rest/ical/phz/calendarid_{id}.ics"
        r=requests.get(url, allow_redirects=True)
        open('data.ics', 'wb').write(r.content)

        df=convert_to_csv('data.ics','test16.csv')
        final_df=df_preparation(df)
        
        table=final_df.to_html(classes=['table',"table-striped",'table-bordered'])

        return render(request,'api/home.html',{"table":table})
    except:
        return render(
        request,'api/home.html',{
        "error":True,
        "table":None
        })

def HelpView(request):
    return render(request,'api/help.html',{})

def StatisticsView(request):
    ics_id =request.POST.get('ics')
    if ics_id:
         request.session['ics']=ics_id
    try:
        id= request.session.get('ics')
            
        url = f"https://e-uczelnia.ue.katowice.pl/wsrest/rest/ical/phz/calendarid_{id}.ics"
        r=requests.get(url, allow_redirects=True)
        open('data.ics', 'wb').write(r.content)

        df=convert_to_csv('data.ics','test16.csv')
        df=df_preparation(df)

        subjectsCountDF=subjectsCount(df)
        classTypeCountDF=classTypeCount(df)
        first_last_classDF=first_last_class(df)

        subjectsCountTable=subjectsCountDF.to_html(classes=['table',"table-striped",'table-bordered','text-center'],index=False)
        classTypeCountTable=classTypeCountDF.to_html(classes=['table',"table-striped",'table-bordered', 'text-center'],index=False)
        first_last_classTable=first_last_classDF.to_html(classes=['table',"table-striped",'table-bordered', 'text-center'],index=False)

        context={
            "subjectsCountTable":subjectsCountTable,
            "classTypeCountTable":classTypeCountTable,
            "first_last_classTable":first_last_classTable
        }

        return render(request,'api/statistics.html',context)
    except:
        context={
            "error":True
        }
        return render(request,'api/statistics.html',context)


def recordsView(request):
    ics_id =request.POST.get('ics')
    if ics_id:
         request.session['ics']=ics_id
    try:
        id= request.session['ics'] or request.POST.get('ics_id')
        request.session['ics']=id
            
        url = f"https://e-uczelnia.ue.katowice.pl/wsrest/rest/ical/phz/calendarid_{id}.ics"
        r=requests.get(url, allow_redirects=True)
        open('data.ics', 'wb').write(r.content)

        df=convert_to_csv('data.ics','test16.csv')
        final_df=df_records(df)
        
        table=final_df.to_html(classes=['table',"table-striped",'table-bordered'])

        return render(request,"api/records.html",{"table":table})
    except:
        return render(
        request,"api/records.html",{
        "error":True,
        "table":None
        })

