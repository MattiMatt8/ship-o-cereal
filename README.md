# Ship O Cereal
Web store that sells everything related to cereal.

# Requirements
- Recent version of Python
- Python packages:
    - django
    - django-filter
    - Pillow 
    - psycopg2-binary
    - python-dotenv

## Installing requirements

1. Change directory to the directory where requirements.txt is located.  

2. Activate your virtualenv.  

3. Run: pip install -r requirements.txt in your shell.  

## Required credentials
The application uses Google Cloud for the PostgreSQL database hosting.  
Contact us for the correct credentials that you have to put in a .env file.

# Run
- Command to run the server:
    - python manage.py runserver

# Additional functionality
- ### User related
    - #### Category pages
        - Filter by brand on top of filtering by label (e.g. Gluten free, Healthy, ...)
        - Order by newest arrivals, on sale on top of being able to order by price (ascending & descending) & name (ascending & descending).
    - #### Profile
        - Users can easily upload their profile picture straight to the website.
        - Users can save addresses to their accounts.
        - Users can save cards to their accounts.
        - Users can view their old orders in completion.
    - #### Checkout
        - User can select from his saved addresses or add a new one.
        - User can select from his saved cards or add a new one.
    - #### Product pages
        - Products can only be bought if they are in stock as each product has x amount of stock.
        - Users can post reviews on products, but only products they have bought and only one per product.
        - Products can be on sale and are displayed nicely to the user the old price, new price and the percentage difference.
    - #### The website is responsive and works on all devices.

- ### The admin panel
    - #### Orders
        - Nicely formatted overview page of all orders.
        - Orders status can be changed from e.g. Placed to Shipped to indicate at what stage the order is at.
        - If an order is selected it shows all the information of it and also shows the items that were purchased in that order nicely formatted in a table.
    - #### Products
        - Nicely formatted overview page of all products.
        - Products can be edited as the staff wish.
            - Images for a product can be easily uploaded through the admin panel.
        - Products can be easily added to the web store.
    - #### Product discounts
        - Staff can easily put products on discount and the only thing they need to specify is how much percentage off the product should be.
        - The admin panel then calculates the new price from that, saves it and displays it in the panel.

