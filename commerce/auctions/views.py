from pydoc import describe
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse

from .models import User, bids, listings, comments, watchList
from .Form import CreateListingForm, CATAGORIES, ListPageForm


def index(request):
    Listings = []
    listingsList = listings.objects.all()
    for listing in listingsList:
        if not listing.sold:
            Listings.append(listing)

    return render(request, "auctions/index.html", {"Listings": Listings})


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


@login_required
def createListing(request):
    if request.method == "GET":
        f = CreateListingForm()
        v = bids(user_id=1, amount=1234, listing_id=32)
        v.save()
        p = bids.objects.filter(amount=1234)
        print(p)
        bids.objects.filter(amount=1234).delete()
        return render(request, "auctions/createListing.html", {"Catagories": CATAGORIES, })
    else:
        # get the data
        f = CreateListingForm(request.POST)
        # check if the form is valid
        if f.is_valid():
            selected = request.POST.get("catagory")
            # if the selected is not valid, render a appology
            if not selected in CATAGORIES:
                return render(request, "auctions/sorry.html", {"message": "Invalid catagory"})
            # manually check text area
            text = request.POST.get("dis")
            if not text:
                return render(request, "auctions/sorry.html", {"message": "Input a description"})

            # import into the listings table
            l = listings(title=f["title"].value(), description=text, starting_bid=f["startBid"].value(), current_bid=f["startBid"].value(),
                         imag_url=f["imageUrl"].value(), catagory=selected, user_id=request.user.id)
            l.save()

            # redirect the user to the index
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "auctions/sorry.html", {"message": "Invalid Input"})


def listingPage(requests, idl):
    if requests.method == "GET":
        # get the info
        listing = listings.objects.filter(id=idl)[0]
        commentList = comments.objects.filter(listing_id=idl)
        owner = False
        winner = {"win": False, "name": ""}

        # checks if the listing has been already sold, this will be used to display a diffrent form of the webpage
        if listing.sold:
            winner["win"] = True
            print("00000000000000000000000000000000", listing.sold_to)
            winner["name"] = User.objects.filter(
                pk=listing.sold_to)[0].username

        # checks if this is the owner of the page
        if requests.user.id == listing.user_id:
            # if so, allows them to close the auction at anytime
            owner = True
        # else the user is taken to the reqular page
        return render(requests, "auctions/listingsPage.html", {"listing": listing, "comments": commentList, "owner": owner, "winner": winner})
    else:
        # this is for when the person wants to bid upon the item in the auction, or some other process such as adding it to the watch list
        # general info
        commentList = comments.objects.filter(listing_id=idl)
        owner = False
        winner = {"win": False, "name": ""}

        # get info from page
        f = ListPageForm(requests.POST)
        listing = listings.objects.filter(id=idl)[0]
        bidbutton = requests.POST.get('bidbutton')
        watchbutton = requests.POST.get('watchbutton')
        closebutton = requests.POST.get('closebutton')
        commentbutton = requests.POST.get('commentbutton')
        # check if the form is valid

        # check if it has been sold
        if listing.sold:
            winner["win"] = True
            winner["name"] = User.objects.filter(
                pk=listing.sold_to)[0].username

        # checks if this is the owner of the page
        if requests.user.id == listing.user_id:
            # if so, allows them to close the auction at anytime
            owner = True

        # Bid Route
        if f.is_valid() and not winner:
            f.clean()
            bid = int(f["bid"].value())
            if bidbutton:
                # compare it to the current bid
                if bid <= listing.current_bid:
                    # return a error message
                    return render(requests, "auctions/listingsPage.html", {"listing": listing, "comments": commentList, "close": owner, "message": "To low"})
                # update the current bid, and refresh the page with a success message
                listings.objects.filter(id=idl).update(
                    current_bid=bid, current_holder=requests.user.id)
                listing = listings.objects.filter(id=idl)[0]
                return render(requests, "auctions/listingsPage.html", {"listing": listing, "comments": commentList, "close": owner, "message": "Successfull Bid!"})

        if watchbutton:
            # add the listing to the users watch list
            # check for duplicates and if there is dont do anything
            if len(watchList.objects.filter(user_id=requests.user.id, listing_id=listing.id)) == 0:
                watch = watchList(user_id=requests.user.id,
                                  listing_id=listing.id)
                watch.save()

        if closebutton and not winner:
            # closes the auction
            # updates the sold, and sold_for values
            listings.objects.filter(id=idl).update(
                sold=True, sold_for=listing.current_bid, sold_to=listing.current_holder)

        if commentbutton and not winner:
            commentText = requests.POST.get('comment')
            comment = comments(
                text=commentText, user_id=requests.user.id, listing_id=listing.id, user_name=requests.user.username)
            comment.save()
            commentList = comments.objects.filter(listing_id=idl)
            return render(requests, "auctions/listingsPage.html", {"listing": listing, "comments": commentList, "close": owner})

        # redirect to the index page
        return HttpResponseRedirect(reverse("index"))


def watchListPage(requests):
    if requests.method == "GET":
        watchListings = []
        watchs = watchList.objects.filter(user_id=requests.user.id)
        for watch in watchs:
            lis = listings.objects.filter(id=watch.listing_id)
            for x in lis:
                watchListings.append(x)
        return render(requests, "auctions/watchPage.html", {"watchs": watchListings})
    else:
        # this is to delete a watch list entry
        # get id , find it in watchlist, delete it, refresh page

        pass


def all(requests):
    Listings = listings.objects.all()
    return render(requests, "auctions/allListings.html", {"Listings": Listings})


def catagories(requests):
    return render(requests, "auctions/catagories.html", {"catagories": CATAGORIES})


def catagory(requests, catagory):
    catList = listings.objects.filter(catagory=catagory)
    return render(requests, "auctions/catagoryListings.html", {"Listings": catList})
