from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import utils
from django.template.defaulttags import register
import random
from django.views.decorators.csrf import csrf_protect 
from django.contrib.auth.hashers import check_password, make_password
from bson import ObjectId




@register.filter
def get_item(dictionary, key=None):
    if not key:
        key = "_id"
    return str(dictionary.get(key)) + "/" + dictionary.get("name").replace(" ", "-")

@register.filter
def get_item_id(dictionary, key=None):
    if not key:
        key = "_id"
    return dictionary.get(key)

def home(request):
    context = {}
    db, _ = utils.get_collection_handle("items")
    categories = db.aggregate([{ '$group': { '_id': '$category'} }])
    context['categories'] = sorted([x['_id'] for x in categories])



    products = []
    if name := request.GET.get('category'):
        context["current_category"] = name
        single_category = db.find({"category": name})
        if single_category:
            # import ipdb; ipdb.set_trace()
            products = [x for x in single_category]
        else:
            return HttpResponse('Category not found')
    else:
        products = [x for x in db.find()]
        # for product in context['categories'].clone():
        #     products += product['items']

        
        
    
    for product in products:
        ratingSum = 0
        ratingCount = 0
        for rating in product['ratings']:
            ratingSum += rating['rating']
            ratingCount += 1

        product['ratingAvg'] = int(ratingSum / ratingCount) if ratingCount > 0 else 0
        product['ratingAvgRange'] = range(product['ratingAvg'])
        product['ratingAvgRangeRemainder'] = range(5 - product['ratingAvg'])
    random.shuffle(products)
    context['products'] = products

    
    return render(request, 'home.html', context)

def product(request, product_id, name):
    context = {}
    db, _ = utils.get_collection_handle("items")
    categories = db.aggregate([{ '$group': { '_id': '$category'} }])
    context['categories'] = sorted([x['_id'] for x in categories])





    try:
        product = utils.get_document_by_id('items', product_id)
    except:
        return HttpResponse('Product not found')
    if product:

        if request.session.get('username', False):
            # get old rating and review
            for rating in product['ratings']:
                if rating['username'] == request.session['username']:
                    context['userRating'] = rating['rating']
                    break
            for review in product['reviews']:
                if review['username'] == request.session['username']:
                    context['userReview'] = review['review']
                    break


        updated = False
        if request.method == 'POST' and request.session.get('username', False):
            if request.POST.get('rating'):
                rating = int(request.POST.get('rating'))
                if rating > 5 or rating < 1:
                    return HttpResponse('Invalid rating')
                res = db.update_one({"_id": ObjectId(product_id), "ratings.username": request.session['username']}, {'$set': {'ratings.$.rating': rating}})
                if res.modified_count or res.matched_count:
                    updated = True
                else:
                    res = db.update_one({"_id": ObjectId(product_id)}, {'$push': {'ratings': {'username': request.session['username'], 'rating': rating}}})
                    if res.modified_count:
                        updated = True

            if request.POST.get('text'):
                review = request.POST.get('text')
                res = db.update_one({"_id": ObjectId(product_id), "reviews.username": request.session['username']}, {'$set': {'reviews.$.review': review}})
                if res.modified_count or res.matched_count:
                    updated = True
                else:
                    res = db.update_one({"_id": ObjectId(product_id)}, {'$push': {'reviews': {'username': request.session['username'], 'review': review}}})
                    if res.modified_count:
                        updated = True
            else:
                res = db.update_one({"_id": ObjectId(product_id)}, {'$pull': {'reviews': {'username': request.session['username']}}})
                updated = True


        if updated:
            try:
                product = utils.get_document_by_id('items', product_id)
                if product is None:
                    return HttpResponse('Product not found')
                for rating in product['ratings']:
                    if rating['username'] == request.session['username']:
                        context['userRating'] = rating['rating']
                        break
                for review in product['reviews']:
                    if review['username'] == request.session['username']:
                        context['userReview'] = review['review']
                        break
            except:
                return HttpResponse('Product not found')





        if name != product['name'].replace(" ", "-"):
            return HttpResponse('Product not found')
        context["current_category"] = product['category']
        context['product'] = product
        ratingSum = 0
        ratingCount = 0
        for rating in product['ratings']:
            ratingSum += rating['rating']
        ratingCount = len(product['ratings'])
        product['reviewCount'] = len(product['reviews'])
        product['ratingCount'] = ratingCount
        product['ratingAvg'] = int(ratingSum / ratingCount+.5) if ratingCount > 0 else 0
        product['ratingAvgRange'] = range(product['ratingAvg'])
        product['ratingAvgRangeRemainder'] = range(5 - product['ratingAvg'])
        if updated:
            context['updated'] = True
        return render(request, 'product.html', context)
    else:
        return HttpResponse('Product not found')
    
def user(request, username):
    context = {}
    items, _ = utils.get_collection_handle("items")
    users, _ = utils.get_collection_handle("users")

    current_user = users.find_one({"username": username})

    if not current_user:
        return HttpResponse('User not found')
    
    if not current_user['username'] == request.session.get('username', False):
        return HttpResponse('User not found')

    context['user'] = current_user
    del context['user']['password'], context['user']['_id'], context['user']['role'], context['user']['username']
    if context['user'].get('website', False):
        del context['user']['website']

    searchItems = items.find({"ratings": {"$elemMatch": {"username": username}}})
    ratingSum = 0
    ratingCount = 0
    for item in searchItems:
        for rating in item['ratings']:
            if rating['username'] == username:
                ratingSum += rating['rating']
                ratingCount += 1
    context['ratingCount'] = ratingCount
    context['ratingAvg'] = int(ratingSum / ratingCount) if ratingCount > 0 else 0
    context['ratingAvgRange'] = range(context['ratingAvg'])
    context['ratingAvgRangeRemainder'] = range(5 - context['ratingAvg'])

    # reviews written by user
    searchReviews = items.find({"reviews": {"$elemMatch": {"username": username}}})
    presentReview = []
    for item in searchReviews:
        for review in item['reviews']:
            if review['username'] == username:
                review['item'] = item
                presentReview.append(review)
    context['reviews'] = presentReview


    categories = items.aggregate([{ '$group': { '_id': '$category'} }])
    context['categories'] = sorted([x['_id'] for x in categories])
    context["username"] = username


    return render(request, 'user.html', context)

def login(request):
    context = {}
    items, _ = utils.get_collection_handle("items")
    categories = items.aggregate([{ '$group': { '_id': '$category'} }])
    context['categories'] = sorted([x['_id'] for x in categories])

    return render(request, 'login.html', context)

@csrf_protect 
def login_action(request):
    context = {}
    users, _ = utils.get_collection_handle("users")
    username = request.POST.get('username')
    password = request.POST.get('password')
    if not username or not password:
        return HttpResponse('Invalid username or password')
    user = users.find_one({"username": username})
    if not user:
        return HttpResponse('Invalid username or password')
    if not check_password(password, user['password']):
        return HttpResponse('Invalid username or password')
    context['user'] = user
    context['username'] = username

    print(user['role'])
    # set session
    request.session['username'] = username
    request.session['role'] = user['role']

    # redirect to home page

    return redirect('/index.html')

def logout(request):
    request.session.flush()
    return redirect('/index.html')

def admin(request):
    context = {}

    if not request.session.get('role', False) == 'admin':
        return HttpResponse('Page not found')

    items, _ = utils.get_collection_handle("items")
    users, _ = utils.get_collection_handle("users")


    
    categories = items.aggregate([{ '$group': { '_id': '$category'} }])
    context['categories'] = sorted([x['_id'] for x in categories])

    userList = users.find()
    context['userlist'] = userList

    productlist = items.find()
    context['productlist'] = productlist

    return render(request, 'admin.html', context)

def delete_user(request, username):
    
    if not request.session.get('role', False) == 'admin':
        return HttpResponse('Page not found')

    users, _ = utils.get_collection_handle("users")
    items, _ = utils.get_collection_handle("items")

    user = users.find_one({"username": username})
    if not user:
        return HttpResponse('User not found')
    if user['role'] == 'admin':
        return HttpResponse('Admin cannot be deleted')

    # delete user
    users.delete_one({"username": username})
    # delete user from items
    items.update_many({}, {'$pull': {'ratings': {'username': username}}})
    items.update_many({}, {'$pull': {'reviews': {'username': username}}})

    return redirect('/admin.html')

def delete_product(request, product_id):
    
    if not request.session.get('role', False) == 'admin':
        return HttpResponse('Page not found')

    items, _ = utils.get_collection_handle("items")

    product = items.find_one({"_id": ObjectId(product_id)})
    if not product:
        return HttpResponse('Product not found')

    # delete item
    items.delete_one({"_id": ObjectId(product_id)})

    return redirect('/admin.html')

def create_user(request):
    context = {}

    if not request.session.get('role', False) == 'admin':
        return HttpResponse('Page not found')

    users, _ = utils.get_collection_handle("users")

    for user in users.find():
        if user['username'] == request.POST.get('username'):
            return HttpResponse('Username already exists')
    
    utils.data_insert('users', {
        'username': request.POST.get('username'),
        'password': make_password(request.POST.get('password')),
        'role': request.POST.get('role'),
        'name': request.POST.get('name'),
        'mail': request.POST.get('mail'),
        'sex': request.POST.get('sex'),
        'job': request.POST.get('job'),
        'company': request.POST.get('company'),
        'ssn': request.POST.get('ssn'),
        'residence': request.POST.get('residence'),
        'blood_group': request.POST.get('blood_group'),
        'address': request.POST.get('address'),
    })


    return redirect('/admin.html')

def create_product(request):
    context = {}

    if not request.session.get('role', False) == 'admin':
        return HttpResponse('Page not found')

    items, _ = utils.get_collection_handle("items")

    computer_component_fields = ["capacity", "speed"]
    clothing_fields = ["size", "colour"]
    monitor_fields = ["screen-size", "resolution", "refresh-rate"]
    snacks_fields = ["calories"]

    additional_info = {}
    for key in request.POST:
        if key.startswith('additional_info_'):
            if request.POST.get("category") == "Computer Components" and key.replace('additional_info_', '') in computer_component_fields or\
                request.POST.get("category") == "Clothings" and key.replace('additional_info_', '') in clothing_fields or\
                request.POST.get("category") == "Monitors" and key.replace('additional_info_', '') in monitor_fields or\
                request.POST.get("category") == "Snacks" and key.replace('additional_info_', '') in snacks_fields:
                additional_info[key.replace('additional_info_', '')] = request.POST.get(key)

    utils.data_insert('items', {
        'name': request.POST.get('name'),
        'description': request.POST.get('description'),
        'price': request.POST.get('price'),
        'seller': request.POST.get('seller'),
        'ratings': [],
        'reviews': [],
        'additional_info': additional_info,
        'image': request.POST.get('image'),
        'category': request.POST.get('category'),
    })

    return redirect('/admin.html')