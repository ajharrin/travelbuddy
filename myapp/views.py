from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

# Create your views here.
def main(request):
    return render(request, "main.html")

def register(request):
    errors = User.objects.regValidator(request.POST)
    print(errors)
    if errors:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect("/")
    else:
        hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(name = request.POST['name'], username = request.POST['username'], password = hash.decode())
        request.session["id"] = user.id
        return redirect("/travels")

def login(request):
    result = User.objects.loginValidator(request.POST)
    print(result)

    if result[0]:
        for key, value in result[0].items():
            messages.error(request, value, extra_tags=key)
        return redirect('/')
    else:
        request.session["id"] = result[1].id
        return redirect("/travels")

def travels(request):
    if "id" in request.session:
        all_trips = Trips.objects.all()
        user = User.objects.get(id=request.session['id'])
        user_trips = Trips.objects.filter(joined_by = request.session['id'])
        other_trips = Trips.objects.exclude(joined_by = request.session['id'])
        context={
            "user": user,
            "user_trips": user_trips,
            "all_trips": all_trips,
            "other_trips": other_trips
        }
        return render(request, "travels.html", context)
    else:
        return redirect("/")

def logout(request):
    request.session.clear()
    return redirect("/")

def add(request):

    return render(request, "add.html")

def addPlan(request):
    user = User.objects.get(id = request.session["id"])
    errors = Trips.objects.tripsValidator(request.POST)
    print(errors)

    if errors:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect("/add")
    else:
        trip = Trips.objects.create(destination= request.POST["destination"], plan = request.POST["plan"], start_date = request.POST["start_date"], end_date = request.POST["end_date"], planned_by_id = request.session["id"])
        user.joined.add(trip)
        return redirect("/travels")

def destination(request, trips_id):
    trip = Trips.objects.get(id=trips_id)
    planned_user_id = trip.planned_by_id
    all_users = trip.joined_by.exclude(id=planned_user_id)

    context={
        "trip":trip,
        "all_users": all_users
    }
    return render(request, "destination.html", context)

def joinTrip(request, trips_id):
    trips = Trips.objects.get(id = trips_id)
    user = User.objects.get(id = request.session["id"])
    user.joined.add(trips)
    return redirect("/travels")
