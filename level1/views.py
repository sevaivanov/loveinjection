from django.shortcuts import HttpResponse, render_to_response, render
from django.views.decorators.csrf import csrf_protect, csrf_exempt, requires_csrf_token
from django.db import connection

def login(request):
    return render_to_response('level1/login.html')

@csrf_exempt
def auth(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        cursor = connection.cursor()
        sql = """SELECT username, password FROM level1_user 
            WHERE username='""" + username + "' AND password='" + password + "';"
        
        try:
            query = cursor.execute(sql)
        except Exception, error:
            return render(request, 'level1/login.html', {"log": error})

        creds = {}
        auth = False 
        for user, pwd in query:
            creds[user] = pwd
            if user: auth = True

        log = username + " </br>" + password + "</br>" + str(auth) + "</br>" + str(creds) + " </br>" + sql
        return render(request, 'level1/login.html', {"log": log})
