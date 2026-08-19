# 🛒 E-Commerce REST API

A comprehensive backend E-Commerce RESTful API built with Django and Django REST Framework (DRF).

## 🚀 Features
* Authentication & Authorization: Secure JWT-based authentication using rest_framework_simplejwt.
* Product Management: Endpoints for managing categories and products.
* Favorites System: Allow users to bookmark their favorite products.
* Shopping Cart: Full shopping cart functionality (add, update, remove items).
* Order Processing: Order creation and management workflows.

## 🛠️ Tech Stack
* Backend: Python, Django, Django REST Framework
* Authentication: SimpleJWT
* Database: SQLite (Development)

## 📌 Main API Endpoints
* POST /api/token/ - Obtain JWT token
* POST /api/token/refresh/ - Refresh JWT token
* /products/ - Manage products
* /cart/ - Manage cart items
* /orders/ - Handle orders and checkout
* /favorites/ - Manage user wishlist
