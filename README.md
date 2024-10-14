# commerce: Django Auction Site

Welcome to the Django Auction Site! This web application allows users to create and manage auction listings, place bids, and engage in discussions through comments. The project is built using Django and includes user authentication, category filtering, and a dynamic user interface.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Models](#models)
- [Requirements](#requirements)
- [Contributing](#contributing)
- [License](#license)

## Features

- User registration and authentication
- Create and manage auction listings
- Active listings display with titles, descriptions, current prices, and images
- Individual listing pages with bidding and commenting functionality
- Watchlist feature for tracking favorite listings
- Category-based filtering for listings
- Django admin interface for site management

## Installation

To set up the project locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/django-auction-site.git
   cd django-auction-site
   ```

2. **Install the required packages**:
   Make sure you have Python installed, then install Django and any other dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. **Apply database migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

5. **Access the application**:
   Open your browser and visit `http://127.0.0.1:8000` to see the application in action.

## Usage

Once the server is running, you can register for an account by clicking on the "Register" link. After signing in, users can create auction listings, place bids, comment on listings, and manage their watchlist.

### User Roles
- **Registered Users**: Can create listings, bid, comment, and manage their watchlist.
- **Administrators**: Can manage all listings, comments, and bids through the Django admin interface.

## Models

The application includes the following models:

- **User**: Inherits from `AbstractUser` with optional additional fields.
- **Listing**: Represents an auction listing with fields for title, description, starting bid, image URL, and category.
- **Bid**: Represents a bid placed on a listing, tracking the bidder and bid amount.
- **Comment**: Allows users to leave comments on listings, associating each comment with a specific user and listing.
- **Category**: (Optional) Represents different categories for listings (e.g., Fashion, Electronics).

## Requirements

- Python 3.x
- Django 3.x or later

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for details.


Feel free to modify any sections to better fit your project!
