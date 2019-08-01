<h1 align="center">
  <br>
  <a href="https://github.com/Abdur-rahmaanJ"><img src="https://github.com/Abdur-rahmaanJ/shopyo/blob/master/shopyo.png" alt="shopyo" width="300px" height="300px"></a>
  <br>
  Shopyo
  <br>
</h1>

🎁 Open inventory management  and Point of sales (powered by python) for small shops. 

- :ok_hand: Crisp UI
- :heartpulse: Intuitive
- :sparkler: Instant lookup
- :pencil2: Towards customisation

# ⚗️ Stability

**alpha** - highly volatile, core features not yet finished

# 💌 Contributing Countries

🇲🇺 🇩🇪 🇨🇳 🇬🇧

# 🔥 Just Added Features

- Confirmation before deleting section
- Settings fully operationable
- Apply settings works for existing and non-existing db

# Testimonial

# 📖 History

Months ago i was searching github, looking for a point of sales solution using Python. What pricked me was that a good many had an annoying point. Some mandatorily required Posgres as though it ships with your computer, others' codebases were a tkinter spaghetti mess, yet others were django-based accounting monsters ...

I decided to give it a try, modelling it after a client request i once got. Made it flask-based with sqlalchemy+sqlite. You can instantly get started with no hassle, switching to something powerful when you want to (since it uses an ORM)

For the UI, we used the latest, bootstrap4, fa5 and jq3. Interestingly enough, i had two shop owners try it, the usage simplicity was praised

It's still in dev and supports instant lookup. Long story short, with some programming skills, you can solve some everyday problems. And yes, no cdn, all libs are bundled so that you can use it completely offline

See [this](https://www.linkedin.com/feed/update/urn:li:activity:6551367967978979328) linked-in article!

# ♨️ Contributing

If you want to contribute, go ahead, we ❤️ it. We follow a 💯 % first-timers-friendly policy.

- Add your country flag in readme after accepted PR

# 💬 Community: Discord
[https://discord.gg/k37Ef6w](https://discord.gg/k37Ef6w)

# 🔧 Install instructions

- download python3.7
- clone and cd into project
- run ```python -m pip install -r requirements.txt```

# 👟 Run instructions
run initialise.py

```python
python initialise.py
```

```python
python apply_settings.py
```

then run the app in shopyo/shopyo

```python
python app.py
```

the go to the indicated url

# :construction: Developing a template.

Each landing page and subsection should contain the following headers.


``{% extends "base/main_base.html" %}`` //  extends the base.html file.

``{% set active_page = "sectionName" %}`` // sets the active section (change section name).



#### Create the main landing page of a new section in the template folder.

Inside the template folder create a file ending ``_index.html``.

```
/template
    /base
    /<changeme> (swap <changeme> for section name).
        index.html
```

#### Create a subsection template.

Inside the template folder create a new file.

```
/template 
    /base
    /<changeme> (swap <changeme> for subsection name).
        index.html
        anotherfile.html 
```

#### Create navigation elements for a new section.


Inside the template folder create a file with the same section name as ``index.html``. Changing ``index.html`` for ``nav.html``.

```
/template
    /base
    /example_section_name
        index.html
        nav.html
```

In the  ```nav.html```  file elements for the navigation can be created.


#### To display the navagation elements.

Open the template ``/base`` folder and locate the ``nav_base.html``.

In the ``nav_bar_log([])`` array. Enter the section name last in the list.


```python3
{% set nav_bar_log = [
  ('section0'),
  ('section1'),
  ('new_section')
  ] %}

Now enter a new elif statement containing a reference to the _nav.html

    {% elif active_page == nav_bar_log[0] %}
      {% include "section0/nav.html" %}
      
    {% elif active_page == nav_bar_log[1] %}
      {% include "section1/nav.html" %}

    {% elif active_page == nav_bar_log[2] %} <- - - Add 1 to index.
      {% include "new_section/nav.html" %}
```

Then the navagation elements will be displayed in the new section.

# Windows Deployment

[Abdur-rahmaanJ/shopyo-windows](https://github.com/Abdur-rahmaanJ/shopyo-windows)

[youtube demo](https://youtu.be/fOUEyuMgZ0U)

## 🍳 In Action
![](shopyo_min.gif)



