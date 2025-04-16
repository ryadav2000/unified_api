#  Ecommerce Sync API (Shopify + Klaviyo)

This project is a Django REST Framework-based API that integrates with external ecommerce platforms — **Shopify** and **Klaviyo** — to synchronize **products** and **customers** into a local database.

## Features

-  Sync products and customers from Shopify via API
-  Sync customer data from Klaviyo
-  Background sync using Celery
-  Robust exception handling and logging
-  Swagger UI for API testing and documentation
-  Filterable viewsets for Products, Customers, and Orders

---

##  Tech Stack

- **Python 3.12**
- **Django 5.2**
- **Django REST Framework**
- **Celery + Redis** (for background tasks)
- **drf-yasg** (Swagger docs)
- **Shopify Admin API**
- **Klaviyo API v2**

---

##  Installation

1. **Clone the repo**
   ```bash
   git clone https://github.com/yourusername/ecommerce-sync-api.git
   cd ecommerce-sync-api



Step 2 :- Create virtual environment

            python -m venv env
            source env/bin/activate


Step 3:- Install dependencies

        pip install -r requirements.txt

Step 4 :- Set environment variables

        Create a .env file with:

        SHOPIFY_API_KEY=your_shopify_api_key
        SHOPIFY_PASSWORD=your_shopify_password
        SHOPIFY_STORE_NAME=your-store.myshopify.com

        KLAVIYO_API_KEY=your_klaviyo_private_api_key

Step 5 :- Apply migrations

    python manage.py migrate

Step 6:- Run server

    python manage.py runserver


Step 7:- Start Celery worker


    celery -A your_project_name worker --loglevel=info


API Endpoints


Method	   Endpoint	                Description
GET	       /products/	            List all products
GET	       /customers/	            List all customers
GET	       /orders/	                List all orders
POST	   /sync/	                Sync both Shopify + Klaviyo
POST	   /api/sync/shopify/	    Run Shopify sync in background
POST	   /api/sync/klaviyo/	    Run Klaviyo sync in background
POST	   /test-sync/shopify/	    Test direct Shopify sync
POST	   /test-sync/klaviyo/	    Test direct Klaviyo sync


 Swagger Documentation Visit:-

    http://localhost:8000/swagger/   (To explore and test all API endpoints visually.)
 

 Testing

 python manage.py test



 Project Structure
        core/
        ├── models.py
        ├── views.py
        ├── sync/
        │   ├── shopify.py
        │   └── klaviyo.py
        ├── tasks.py
        └── urls.py


Author
Ravi Kumar Yadav
Developed as part of a practical API integration challenge.




