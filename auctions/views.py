from django.contrib.auth import authenticate, login, logout  # Import authentication functions
from django.contrib.auth.decorators import login_required  # Ensure certain views require login
from django.db import IntegrityError  # Handle integrity errors, like unique constraint violations
from django.http import HttpResponse, HttpResponseRedirect  # Handle HTTP responses and redirects
from django.shortcuts import render, redirect  # Render templates and handle redirects
from django.urls import reverse  # Generate URL paths based on view names
from .models import User, Auction, Category  # Import necessary models
from django import forms  # Import Django forms framework
from .forms import *  # Import custom forms from forms.py

# View for the homepage, showing all auctions
def index(request):
    return render(request, "auctions/index.html", {
        'list_auctions': Auction.objects.all(),  # Pass all active auctions to the template
        'title': 'Active Listings'  # Set the page title
    })

# View to display a specific auction listing
def listing(request, listing_id):
    auction = Auction.objects.get(id=listing_id)  # Get the auction by its ID
    if request.user.username:
        # If user is logged in, initialize forms and check if the auction is on their watchlist
        watch_list_form = WatchListForm(auction=auction, user=request.user)
        is_on_watchlist = request.user.watchlist.filter(auction=auction).exists()  # Check if the auction is on the user's watchlist
        comment_form = CommentForm(auction=auction, user=request.user)  # Form for adding comments
    else:
        watch_list_form = None  # No form if user is not logged in
        is_on_watchlist = False  # Auction can't be on watchlist if user isn't logged in
        comment_form = None  # No comment form if user isn't logged in

    return render(request, "auctions/listing.html", {
        'auction': Auction.objects.get(id=listing_id),  # Pass the auction object
        'BidForm': BidForm(auction=auction),  # Form to place a bid
        'WatchListForm': watch_list_form,  # Watchlist form
        'is_on_watchlist': is_on_watchlist,  # Whether the auction is on the user's watchlist
        'CommentForm': comment_form  # Comment form
    })

# View for user login
def login_view(request):
    if request.method == "POST":
        # Get the username and password from the POST request
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)  # Authenticate the user

        # If authentication is successful, log the user in and redirect to the homepage
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            # If authentication fails, reload the login page with an error message
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")  # If not a POST request, show the login page

# View for logging out the user
def logout_view(request):
    logout(request)  # Log the user out
    return HttpResponseRedirect(reverse("index"))  # Redirect to homepage after logout

# View for user registration
def register(request):
    if request.method == "POST":
        # Get user details from POST request
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        # Check if passwords match
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Try to create a new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()  # Save the new user to the database
        except IntegrityError:
            # Handle case where username already exists
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        
        # Log in the newly registered user and redirect to homepage
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")  # Show the registration page if not POST

# View to create a new auction listing (requires login)
@login_required
def create(request):
    if request.method == "POST":
        form = AuctionForm(request.POST)  # Initialize the form with POST data
        if form.is_valid():
            auction = form.save(commit=False)  # Create an auction instance but don't save yet
            auction.creator = request.user  # Set the creator of the auction to the logged-in user
            auction.save()  # Save the auction to the database
            return redirect('create')  # Redirect to the create page (or you could redirect elsewhere)

    else:
        form = AuctionForm()  # If not POST, display an empty form

    return render(request, "auctions/create.html", {
        'form': form  # Render the form in the template
    })

# View to add a bid on an auction (requires login)
@login_required
def add_bid(request, listing_id):
    if request.method == "POST":
        auction = Auction.objects.get(id=listing_id)  # Get the auction by its ID
        form = BidForm(request.POST, auction=auction)  # Initialize the form with POST data and auction
        if form.is_valid():
            bid = form.save(commit=False)  # Create a bid instance but don't save yet
            bid.user = User.objects.get(username=request.user.username)  # Set the user who made the bid
            bid.auction = Auction.objects.get(id=listing_id)  # Set the auction for the bid
            bid.save()  # Save the bid to the database
        else:
            # If form is not valid, render the listing page with the form errors
            return render(request, "auctions/listing.html", {
                'auction': auction,
                'BidForm': form
            })

    return redirect('listing', listing_id)  # Redirect back to the auction listing

# View to manage the user's watchlist (requires login)
@login_required
def edit_watchlist(request, listing_id):
    if request.method == "POST":
        auction = Auction.objects.get(id=listing_id)  # Get the auction by its ID
        form = WatchListForm(request.POST, auction=auction, user=request.user)  # Initialize the watchlist form
        user_watchlist = request.user.watchlist.filter(auction=auction)  # Get the user's watchlist for this auction
        request_url = (request.META.get('HTTP_REFERER', '/'))  # Get the referring URL

        if user_watchlist.exists():
            user_watchlist.delete()  # If the auction is already on the watchlist, remove it
        elif form.is_valid():
            form.save()  # If the form is valid, add the auction to the watchlist

    return redirect('listing', listing_id)  # Redirect back to the auction listing

# View to close an auction (requires login)
@login_required
def close_auction(request, listing_id):
    if request.method == "POST":
        auction = Auction.objects.get(id=listing_id)  # Get the auction by its ID
        if auction.is_active and auction.creator.username == request.user.username:
            auction.is_active = False  # Mark the auction as closed
            auction.save()  # Save the changes

    return redirect('listing', listing_id)  # Redirect back to the auction listing

# View to add a comment to an auction (requires login)
@login_required
def add_comment(request, listing_id):
    if request.method == "POST":
        auction = Auction.objects.get(id=listing_id)  # Get the auction by its ID
        form = CommentForm(request.POST, auction=auction, user=request.user)  # Initialize the comment form
        if form.is_valid():
            form.save()  # Save the comment to the database
        else:
            print(form.errors)  # If form is not valid, print errors

    return redirect('listing', listing_id)  # Redirect back to the auction listing

# View to show the user's watchlist (requires login)
@login_required
def watchlist(request):
    list_auctions = [element.auction for element in request.user.watchlist.all()]  # Get all auctions on the user's watchlist

    return render(request, "auctions/index.html", {
        'title': 'Watchlist',
        'list_auctions': list_auctions  # Render the watchlist on the index page
    })

# View to show all categories
def categories(request):
    list_categories = Category.objects.all()  # Get all categories
    for category in list_categories:
        category.count_auctions = category.auctions.filter(is_active=True).count()  # Count active auctions in each category
    return render(request, "auctions/categories.html", {
        'categories': list_categories  # Render categories in the template
    })

# View to show auctions in a specific category
def show_category(request, category):
    category_object = Category.objects.get(name=category)  # Get the category by its name
    return render(request, "auctions/index.html", {
        'title': category.capitalize(),  # Set the page title to the category name
        'list_auctions': category_object.auctions.all()  # Get all auctions in
    })
