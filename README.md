# Needful Things

Needful Things is a simple e-commerce website. It is a Django application that uses MongoDB as the main database and it also uses a local SQLite database to keep sessions. It is deployed on Render at https://e-commerce-20ct.onrender.com/index.html

It's frontend is developed using HTML, CSS and JavaScript on top of [DarkLook Theme](https://github.com/DarkLookTheme/DarkLookTheme.github.io). It uses Bootstrap for styling and jQuery for some of the functionalities.

All the urls and endpoints used by the system are listed below:

```
https://e-commerce-20ct.onrender.com/index.html
https://e-commerce-20ct.onrender.com/product/<str:product_id>/<str:product_name>
https://e-commerce-20ct.onrender.com/user/<str:username>
https://e-commerce-20ct.onrender.com/login.html
https://e-commerce-20ct.onrender.com/login-action.html
https://e-commerce-20ct.onrender.com/logout.html
https://e-commerce-20ct.onrender.com/admin.html
https://e-commerce-20ct.onrender.com/delete_user/<str:username>
https://e-commerce-20ct.onrender.com/delete_product/<str:product_id>
https://e-commerce-20ct.onrender.com/create_user.html
https://e-commerce-20ct.onrender.com/create_product.html
```

## How to Login

1. Go to https://e-commerce-20ct.onrender.com/login.html
2. Enter `harry91` as username and `p455w0rd` as password (or any other username on the system, they all have the same password)
3. Click on `Login` button

## Log in as Admin

1. Go to https://e-commerce-20ct.onrender.com/login.html
2. Enter `mrneedful` as username and `p455w0rd` as password
3. Click on `Login` button
4. You can visit admin panel by clicking on `admin` button on the top of the website or by visiting https://e-commerce-20ct.onrender.com/admin.html

## Used Technologies

- HTML
- CSS
- JavaScript
- Bootstrap
- jQuery
- Django
- MongoDB
- SQLite