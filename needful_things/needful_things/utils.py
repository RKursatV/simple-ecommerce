from pymongo import MongoClient
from django.conf import settings as django_settings
import random
from faker import Faker
from django.conf import settings as django_settings
import requests
import base64
from bson import Decimal128, ObjectId
from datetime import datetime
from decimal import Decimal
from django.contrib.auth.hashers import make_password

fake = Faker('en_US')

def get_db_handle():

    client = MongoClient(django_settings.DATABASE_URL
                        )
    db_handle = client['store']
    return db_handle, client

def get_collection_handle(collection_name):
    db_handle, client = get_db_handle()
    collection_handle = db_handle[collection_name]
    return collection_handle, client

def get_all_documents(collection_name):
    collection_handle, client = get_collection_handle(collection_name)
    documents_handle = collection_handle
    return documents_handle

def get_document_by_id(collection_name, document_id):
    collection_handle, client = get_collection_handle(collection_name)
    document_id = ObjectId(document_id)
    document = collection_handle.find_one({"_id": document_id})
    client.close()
    return document

def data_insert(collection_name, data):
    collection_handle, client = get_collection_handle(collection_name)
    document = collection_handle.insert_one(data)
    client.close()
    return document

def data_bulk_insert(collection_name, data):
    collection_handle, client = get_collection_handle(collection_name)
    document = collection_handle.insert_many(data)
    client.close()
    return document

def update_document(collection_name, document_id, data):
    collection_handle, client = get_collection_handle(collection_name)
    document = collection_handle.update_one({"_id": document_id}, {"$set": data})
    client.close()
    return document


item_attributes = {
    "name": "name",
    "description": "description",
    "price": "price",
    "seller": "seller",
    "image": "image",
    "ratings": [],
    "reviews": [],
}

category_attributes = {
    "name": "name",
    "description": "description",
    "items": [],
}

def get_image_by_category(category):
    api_url = 'https://source.unsplash.com/random/900x700/?{}'.format(category)
    print(api_url)
    response = requests.get(api_url, headers={'Accept': 'image/jpg'}, stream=True)
    if response.status_code == requests.codes.ok:
        image = response.url
        return image
    else:
        print("Error:", response.status_code, response.text)

def generate_item_data(name_options, users):
        item_base = {}
        item_base["name"] = name_options.pop(random.randint(0, len(name_options)-1))
        item_base["description"] = fake.text(max_nb_chars=500)
        item_base["price"] = fake.random_int(min=1, max=1000)
        item_base["seller"] = fake.first_name() + " " + fake.last_name()
        item_base["ratings"] = []
        item_base["reviews"] = []
        rating_givers = random.sample(users, random.randint(0, len(users)))
        for rating_giver in rating_givers:
            item_base["ratings"].append({"rating": random.randint(1,5), "username": rating_giver["username"]})
        review_givers = random.sample(users, random.randint(0, len(users)))
        for review_giver in review_givers:
            item_base["reviews"].append({"review": fake.text(max_nb_chars=100), "username": review_giver["username"]})
        return item_base

def insert_default_data():
    # generate users
    users = []
    for i in range(30):
        user = fake.profile()
        # fake_pw = fake.password(length=10, digits=True, upper_case=True, lower_case=True)
        user["password"] = make_password("p455w0rd")
        user["birthdate"] = datetime.combine(user["birthdate"], datetime.min.time())
        user["role"] = "user"
        del user["current_location"]
        users.append(user)

    data_bulk_insert("users", users)
    # generate items for categories

    # clothing names
    clothing_names = ["T-Shirt", "Shirt", "Pants", "Shorts", "Socks", "Underwear", "Sweater", "Jacket", "Coat", "Dress", "Skirt", "Shoes", "Hat", "Gloves", "Scarf", "Sunglasses", "Belt", "Tie", "Swimwear", "Sweatshirt", "Sweatpants", "Jumpsuit", "Robe", "Pajamas", "Bathing Suit", "Bikini", "Tank Top", "Hoodie", "Sweatshirt", "Sweatpants", "Jumpsuit", "Robe", "Pajamas", "Bathing Suit", "Bikini", "Tank Top", "Hoodie", "Sweatshirt", "Sweatpants", "Jumpsuit", "Robe", "Pajamas", "Bathing Suit", "Bikini", "Tank Top", "Hoodie", "Sweatshirt", "Sweatpants", "Jumpsuit", "Robe", "Pajamas", "Bathing Suit", "Bikini", "Tank Top", "Hoodie", "Sweatshirt", "Sweatpants", "Jumpsuit", "Robe", "Pajamas", "Bathing Suit", "Bikini", "Tank Top", "Hoodie", "Sweatshirt", "Sweatpants", "Jumpsuit", "Robe", "Pajamas", "Bathing Suit", "Bikini", "Tank Top", "Hoodie", "Sweatshirt", "Sweatpants", "Jumpsuit", "Robe", "Pajamas", "Bathing Suit", "Bikini", "Tank Top", "Hoodie", "Sweatshirt", "Sweatpants", "Jumpsuit", "Robe", "Pajamas", "Bathing Suit", "Bikini", "Tank Top", "Hoodie", "Sweatshirt", "Sweatpants", "Jumpsuit", "Robe", "Pajamas", "Bathing Suit", "Bikini", "Tank Top", "Hoodie", "Sweatshirt", "Sweatpants", "Jumpsuit", "Rob"]
    clothing_names = list(set(clothing_names))
    # computer component names
    computer_component_names = ["Ram", "Ssd", "Hdd"]
    # monitor names
    monitor_names = ["LED Monitor", "LCD Monitor", "Curved Monitor", "Computer Monitor", "Television"]
    # snack names
    snack_names = ["Candy", "Chips", "Cookies", "Cereal", "Ice Cream", "Fruit", "Popcorn", "Nuts", "Fruit Snacks", "Granola Bars", "Trail Mix", "Crackers", "Pretzels", "Noodles", "Rice", "Bread", "Canned Goods", "Spices", "Condiments", "Pasta", "Peanut Butter", "Jelly", "Jam", "Honey", "Syrup", "Juice", "Milk", "Eggs", "Cheese", "Butter", "Yogurt", "Soda", "Water", "Tea", "Coffee", "Alcohol", "Beverages", "Soup", "Canned Goods", "Spices", "Condiments", "Pasta", "Peanut Butter", "Jelly", "Jam", "Honey", "Syrup", "Juice", "Milk", "Eggs", "Cheese", "Butter", "Yogurt", "Soda", "Water", "Tea", "Coffee", "Alcohol", "Beverages", "Soup", "Canned Goods", "Spices", "Condiments", "Pasta", "Peanut Butter", "Jelly", "Jam", "Honey", "Syrup", "Juice", "Milk", "Eggs", "Cheese", "Butter", "Yogurt", "Soda", "Water", "Tea", "Coffee", "Alcohol", "Beverages", "Soup", "Canned Goods", "Spices", "Condiments", "Pasta", "Peanut Butter", "Jelly", "Jam", "Honey", "Syrup", "Juice", "Milk", "Eggs", "Cheese", "Butter", "Yogurt", "Soda", "Water", "Tea", "Coffee", "Alcohol", "Beverages", "Soup", "Canned Goods", "Spices", "Condiments", "Pasta", "Peanut Butter", "Jelly", "Jam", "Honey", "Syrup", "Juice", "Milk", "Eggs", "Cheese", "Butter", "Yogurt", "Soda"]
    snack_names = list(set(snack_names))

    clothing_items = []
    for i in range(15):
        cloth_item = generate_item_data(clothing_names, users)
        cloth_item["additional_info"] = {}
        cloth_item["additional_info"]["size"] = random.choice(["XS", "S", "M", "L", "XL", "XXL"])
        cloth_item["additional_info"]["colour"] = random.choice(["Red", "Orange", "Yellow", "Green", "Blue", "Purple", "Pink", "Black", "White", "Brown", "Grey", "Tan", "Cyan", "Magenta", "Violet", "Indigo", "Gold", "Silver", "Bronze", "Copper", "Lavender", "Teal", "Maroon", "Navy", "Mint", "Rose", "Lilac", "Plum", "Peach", "Olive", "Coral", "Ivory", "Khaki", "Beige", "Burgundy", "Crimson", "Turquoise", "Aquamarine", "Lime", "Amber", "Azure", "Cerise", "Cerulean", "Fuchsia", "Mauve", "Saffron", "Sepia", "Ultramarine", "Verdigris", "Vermilion", "Viridian", "Chestnut", "Cinnamon", "Cobalt", "Copper", "Coral", "Crimson", "Cyan", "Fuchsia", "Gold", "Goldenrod", "Gray", "Green", "Indigo", "Ivory", "Khaki", "Lavender", "Lemon", "Lime", "Magenta", "Maroon", "Mauve", "Navy", "Olive", "Orange", "Orchid", "Peach", "Pear", "Periwinkle", "Pine", "Plum", "Prussian", "Purple", "Raspberry", "Red", "Rose", "Salmon", "Sangria", "Sapphire", "Scarlet", "Silver", "Tan", "Teal", "Turquoise", "Vermilion", "Violet", "Viridian", "White", "Yellow"])
        cloth_item["image"] = get_image_by_category('clothing,'+cloth_item["name"])
        cloth_item["category"] = "Clothings"
        clothing_items.append(cloth_item)

    # computer components

    computer__componenet_items = []    
    for i in range(3):
        computer_component_base = generate_item_data(computer_component_names, users)
        computer_component_base["image"] = get_image_by_category('computer,'+computer_component_base["name"])
        computer_component_base["additional_info"] = {}
        computer_component_base["additional_info"]["capacity"] = str(2**fake.random_int(min=1, max=10)) + " GB"
        computer_component_base["additional_info"]["speed"] = str(fake.random_int(min=1, max=10)) + " GHz"
        computer_component_base["category"] = "Computer Components"
        computer__componenet_items.append(computer_component_base)

    # monitors
    monitor_items = []
    for i in range(4):
        monitor_base = generate_item_data(monitor_names, users)
        monitor_base["additional_info"] = {}
        monitor_base["additional_info"]["screen-size"] = str(fake.random_int(min=10, max=100)) + " inch"
        monitor_base["additional_info"]["resolution"] = str(fake.random_int(min=100, max=10000)) + " x " + str(fake.random_int(min=100, max=10000))
        monitor_base["additional_info"]["refresh-rate"] = str(fake.random_int(min=60, max=500)) + " Hz"
        monitor_base["image"] = get_image_by_category('hardware,accessorries,'+monitor_base["name"])
        monitor_base["category"] = "Monitors"
        monitor_items.append(monitor_base)

    # snacks
    snack_items = []
    for i in range(12):
        snack_base = generate_item_data(snack_names, users)
        snack_base["additional_info"] = {}
        snack_base["additional_info"]["calories"] = str(fake.random_int(min=10, max=1000)) + " kcal"
        snack_base["image"] = get_image_by_category('snack,'+snack_base["name"])
        snack_base["category"] = "Snacks"
        snack_items.append(snack_base)


    items = clothing_items + computer__componenet_items + monitor_items + snack_items

    data_bulk_insert("items", items)


# remove all data from mongodb database
# db_handle, client = get_db_handle()
# db_handle.drop_collection("users")
# db_handle.drop_collection("items")
# insert_default_data()