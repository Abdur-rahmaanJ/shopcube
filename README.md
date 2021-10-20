# ShopCube

![alt text](https://github.com/VaithiSniper/ShopCube/blob/dev/logo.png?raw=true)


Copy paste config_demo.json to config.json in shopyo
Copy paste config_demo.py to config.py in shopyo and replace your SQLALCHEMY_DATABASE_URI details

install requirements

```
pip install -r reqs/app.txt
pip install -r reqs/dev.txt
```


```
cd shopyo
python manage.py initialise
python manage.py rundebug
```


browse around and go to /dashboard with login admin@domain.com and password pass

Current features:

-  cart
-  wishlist
-  stock
-  orders

Read the [shopyo](https://shopyo.readthedocs.io/en/latest/) docs to get more development insights

