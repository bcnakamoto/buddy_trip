from django.shortcuts import render, redirect
from .models import User, Trip 
from django.contrib import messages
import datetime

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.validate(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        if request.method == "POST":
            user = User.objects.register(request.POST)
            request.session['user_id'] = user.id
            request.session['user_name'] = user.first_name
        return redirect('/trips')

def username():
    found = False
    mysql = connectToMySQL('ajaxWall')        # connect to the database
    query = "SELECT username from users WHERE users.username = %(user)s;"
    data = { 'user': request.form['username'] }
    result = mysql.query_db(query, data)
    if result:
        found = True
    return render_template('partials/username.html', found=found)  # render a partial and return it
    # Notice that we are rendering on a post! Why is it okay to render on a post in this scenario?
    # Consider what would happen if the user clicks refresh. Would the form be resubmitted?        

def login(request):
    if request.method == "GET":
        return redirect('/')
    if not User.objects.authenticate(request.POST['email'], request.POST['password']):
        messages.error(request, 'Invalid Email/Password')
        return redirect('/')
    user = User.objects.get(email=request.POST['email'])
    request.session['user_id'] = user.id
    request.session['user_name'] = user.first_name
    return redirect('/trips')

def logout(request):
    request.session.clear()
    return redirect('/')
    
def trips(request):
    user = None if 'user_id' not in request.session else User.objects.get(id=request.session['user_id'])
    if not user:
        return redirect('/trips')
    
    my_trips = Trip.objects.filter(owner=user)
    other_trips = Trip.objects.all().exclude(owner=user).exclude(joiner=user)

    return render(request, 'trips.html', {'user': user, 'my_trips': my_trips, 'other_trips': other_trips})

def add_trip(request):
    user = None if 'user_id' not in request.session else User.objects.get(id=request.session['user_id'])
    if not user:
        return redirect('/trips')
    return render(request, 'add_trip.html')

def create_trip(request):
    user = None if 'user_id' not in request.session else User.objects.get(id=request.session['user_id'])
    if not user:
        return redirect('/trips')
    errors = Trip.objects.validate(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/add-trip')
    Trip.objects.create(dest=request.POST.get('dest'), start_date=request.POST.get('start_date'), end_date=request.POST.get('end_date'), plan=request.POST.get('plan'), owner=user)
    return redirect('/trips')

def view_trip(request, trip_id):
    user = None if 'user_id' not in request.session else User.objects.get(id=request.session['user_id'])
    if not user:
        return redirect('/trips')
    context = {
        'trip': Trip.objects.get(id=trip_id)
    }
    return render(request, 'view_trip.html', context)

def join_trip(request, trip_id):
    # pass
    user = None if 'user_id' not in request.session else User.objects.get(id=request.session['user_id'])
    if not user:
        return redirect('/trips')
    joined_trip = Trip.objects.get(id=trip_id)
    joiner = Trip.objects.filter(joiner=user)
    joined_trip.joiner.add(user)
    return redirect('/trips')

def delete_trip(request, trip_id):
    user = None if 'user_id' not in request.session else User.objects.get(id=request.session['user_id'])
    if not user:
        return redirect('/trips')

    trip = Trip.objects.get(id=trip_id)
    if trip.owner == user:
        trip.delete()
    return redirect('/trips')

def cancel_trip(request, trip_id):
    user = None if 'user_id' not in request.session else User.objects.get(id=request.session['user_id'])
    if not user:
        return redirect('/trips')
    if trip.owner == user:
        trip.delete()
    else:
        joined_trip = Trip.objects.get(id=trip_id)
        joiner = Trip.objects.filter(joiner=user)
        joined_trip.joiner.remove(user)
    return redirect('/trips')