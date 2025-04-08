from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.db.models.functions import Lower
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Category, Listings, Comments, Bids
from . import forms


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listings.objects.exclude(is_active=False).all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


# Create new listing
@login_required(login_url='login')
def create_listing(request):
    if request.method == "POST":
        form = forms.ListingForm(request.POST)
        if form.is_valid():
            listings = form.save(commit=False)
            listings.seller = request.user
            listings.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/newListing.html")
    else:
        return render(request,"auctions/newListing.html",{
            "form":forms.ListingForm()
        })


# Display all categories and enter new category
def category(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            form = forms.CategoryForm(request.POST)
            if form.is_valid():
                new_category = form.cleaned_data['category']

                # Check if category already exists
                if Category.objects.filter(category__iexact=new_category):
                    messages.warning(request, "Category already exists!")
                elif not new_category:
                    messages.warning(request, "Please enter category!")
                else:
                    form.save()
                
    return render(request, "auctions/category.html",{
        "form":forms.CategoryForm(), 
        "categories": Category.objects.all()
    })


# Display detail list itme, close list and check winner
def listing(request, list_id):
    try:
        list = Listings.objects.get(id=list_id)
    except Listings.DoesNotExist:
        raise Http404("Listing not found.")
    
    # Closing active listing
    if request.method == "POST":
        if list.seller == request.user:
            list.is_active=False
            list.save()

    # Find the maximum bid for given list id, return as dictionary
    # Convert the dictionary to Decimal field as specified in Model using list
    highest = Bids.objects.filter(listing=list_id).aggregate(Max('bid'))['bid__max']
    if highest is not None:
        highest=round(highest,2)

    # Check if user has added item to watchlist
    user_watch=False
    if request.user.is_authenticated:
        user_watch = list not in request.user.watchlist.all()

    # Check if user has won the bid
    if list.is_active==False:
        winner = Bids.objects.filter(listing=list_id).order_by('-bid').first()
        if winner is not None:
            if winner.user == request.user:
                messages.success(request, "You are the successfull winner of this listing")

    return render(request, "auctions/listing.html",{
        "listing":Listings.objects.get(id=list_id),
        "comments":Comments.objects.filter(listing=list_id),
        "form_comment":forms.CommentForm(),
        "form_bid":forms.BidForm(),
        "max_bid":highest,
        "user_watch": user_watch
    })


# Enter comments
@login_required(login_url='login')
def listcomment(request, list_id):
    try:
        list = Listings.objects.get(id=list_id)
    except Listings.DoesNotExist:
        raise Http404("Listing not found.")
    
    if request.method == "POST":
        if list.is_active:
            form = forms.CommentForm(request.POST)
            if form.is_valid():
                new_comment = form.save(commit=False)
                new_comment.user = request.user
                new_comment.listing = Listings.objects.get(id=list_id)
                new_comment.save()

    return redirect("list", list_id)


# Enter bid
@login_required(login_url='login')
def bid(request, list_id):
    try:
        list = Listings.objects.get(id=list_id)
    except Listings.DoesNotExist:
        raise Http404("Listing not found.")

    if request.method == "POST":
        if list.is_active and list.seller != request.user:
            form = forms.BidForm(request.POST)
            if form.is_valid():
                new_bid = form.save(commit=False)
                highest = Bids.objects.filter(listing=list_id).aggregate(Max('bid'))['bid__max']
                if (new_bid.bid > list.initial_bid) and (highest is None or new_bid.bid > highest):
                    new_bid.user = request.user
                    new_bid.listing = list
                    new_bid.save()
                    messages.success(request, "Bid Successful")
                else: 
                    messages.warning(request, "Bid must be higher than current highest bid and listed price.")

    return redirect("list", list_id)


# Show all items for particular category
def categorylist(request, category_id):
    return render(request,"auctions/categorylist.html",{
        "listings":Listings.objects.filter(category=category_id),
        "category": Category.objects.get(id=category_id)
    })


# Add item to watchlist
@login_required(login_url='login')
def watchlist_add(request, list_id):
    try:
        list = Listings.objects.get(id=list_id)
    except Listings.DoesNotExist:
        raise Http404("Listing not found.")

    if request.user.is_authenticated:
        if request.method == "POST":
            if list not in request.user.watchlist.all():
                request.user.watchlist.add(list)
                request.user.save()
                return redirect("list", list_id)
            else:
                request.user.watchlist.remove(list)
                request.user.save()
                return redirect("list", list_id)
    
    return redirect("list", list_id)


# Display watchlist items
@login_required(login_url='login')
def watchlist_view(request):
    return render(request,"auctions/watchlist.html",{
        "listings":request.user.watchlist.all()
    })