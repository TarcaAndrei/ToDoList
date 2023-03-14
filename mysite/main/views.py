from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import ToDoList, Item
from .forms import CreateNewList
from webpush import send_user_notification
# Create your views here.

def index(response, id):
    ls = ToDoList.objects.get(id=id)
    #{"save":["save"], "c1":["clicked"]}
    if ls in response.user.todolist.all():

        if response.method == "POST":
            print(response.POST)
            if response.POST.get("save"):
                for item in ls.item_set.all():
                    if response.POST.get("c" + str(item.id)):
                        item.complete = True
                    else:
                        item.complete = False
                    item.save()

            elif response.POST.get("newItem"):
                txt = response.POST.get("new")
                day = response.POST.get("data")
                hour = response.POST.get("timp")
                if len(txt)>2:
                    ls.item_set.create(text = txt, complete = False, ora = hour, ziua = day)
                else:
                    print("invalid")

        return render(response, "main/list.html", {"ls":ls})
    return  render(response, "main/view.html", {"ls":ls})

def send(request):
    payload = {"head": "Welcome!", "body": "Hello World"}
    send_user_notification(user=request.user, payload=payload, ttl=1000)
    webpush = {"group": 'mysite'}
    return render(request, 'core/index.html', {"webpush": webpush})

def home(response):
    return render(response, "main/home.html")

def create(response):
    response.user
    if response.method == "POST":
        form = CreateNewList(response.POST)

        if form.is_valid():
            n = form.cleaned_data["name"]
            t = ToDoList(name = n)
            t.save()
            response.user.todolist.add(t)

        return HttpResponseRedirect("/%i" % t.id)
    else:
        form = CreateNewList()
    return render(response, "main/create.html", {"form":form})

def view(response):
    return render(response, "main/view.html", {})


