# ShopCube

![alt text](https://github.com/VaithiSniper/ShopCube/blob/dev/logo.png?raw=true)


Copy paste config_demo.json to config.json in shopyo
Copy paste config_demo.json to config.py in shopyo and replace your SQLALCHEMY_DATABASE_URI details

After pip install requirements,

```
cd shopyo
python manage.py initialise
python manage.py rundebug
```

Current features:

-  cart
-  wishlist
-  stock
-  orders

Read the [shopyo](https://shopyo.readthedocs.io/en/latest/) docs to get more development insights


```
pip-compile --output-file=reqs/dev.txt reqs/dev.in 
```
