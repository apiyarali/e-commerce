# 🛒 E-commerce

A Django-based eBay-like auction site where users can post listings, place bids, comment on listings, and manage a personal watchlist.

## 🚀 Features

* User Authentication: Registration, login, logout with conditional UI rendering.
* Create Listings: Users can post auction listings with titles, descriptions, categories, images, and starting bids.
* Active Listings: Homepage displays all currently active auctions.
* Listing Detail Page: View listing details, place bids, post comments, and manage watchlist.
* Bidding: Bids must be higher than current highest bid or starting bid.
* Watchlist: Users can add/remove items to/from a personal watchlist.
* Auction Management: Listing creators can close auctions, declaring the highest bidder as the winner.
* Comments: Logged-in users can comment on listings.
* Categories: Listings can be browsed by category.
* Admin Interface: Django admin panel allows full CRUD access to listings, bids, and comments.

## 📸 Screenshots

<img src="https://github.com/apiyarali/e-commerce/blob/ba2a92bb81992198333e8079f81648301706631f/screenshot/main.jpg" alt="ecommerce_main" width="400">

<img src="https://github.com/apiyarali/e-commerce/blob/ba2a92bb81992198333e8079f81648301706631f/screenshot/listing_card.jpg" alt="listing_card" width="400">

<img src="https://github.com/apiyarali/e-commerce/blob/ba2a92bb81992198333e8079f81648301706631f/screenshot/details.jpg" alt="details" width="400">

## 🛠 Getting Started

1. Clone the Project

  Download the distribution code or clone this repository.

2. Set Up Environment
    In your terminal
```
cd commerce
python manage.py makemigrations auctions
python manage.py migrate
```

3. Run the Server
```
python manage.py runserver
```

4. Navigate to http://127.0.0.1:8000/ in your browser.

## 👩‍💻 Usage

* Register a new user and log in.
* Create a new listing from the "Create Listing" page.
* View all active listings from the homepage.
* Click on a listing to:
  * Place a bid (must be higher than the current bid or starting bid)
  * Add/remove from your watchlist
  * Leave a comment
  * If you are the creator, close the auction
* Manage your watchlist by visiting the "Watchlist" page.
* Browse by category via the "Categories" page.
* Admin actions via Django admin (/admin) after creating a superuser:
  ```
  python manage.py createsuperuser
  ```

## 🧩 Models

* User: Inherits from AbstractUser.
* Listing: Represents an auction listing.
* Bid: Represents a bid on a listing.
* Comment: Represents user comments on listings.

## 💡 Notes

* Listings can optionally include images and belong to categories like Fashion, Toys, Electronics, and Home.
* Listings become inactive once closed, and winners are shown when viewing a closed listing.
* Only authenticated users can place bids, comment, or manage watchlists.

## 🧰 Tech Stack

* Backend: Django
* Frontend: HTML, CSS (customizable)
* Database: SQLite (default with Django)

## Inspiration
Project inspired by Harvard's CS33 Web Programming curriculum.
