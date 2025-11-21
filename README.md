Features:

✔ Search recipes based on ingredients you own
✔ Simple and clean web interface
✔ Built-in dataset of 100 recipes
✔ Lightweight recommendation logic (no machine learning required)
✔ Runs locally in your browser
✔ Easy to extend with your own recipes

How It Works:

Fridge Chef uses a CSV file (recipes.csv) containing 100 recipes.
When you enter ingredients:

1. The input is cleaned and split into individual items.
2. Each recipe is scored based on ingredient overlap with your list.
3. The top matching recipes are displayed with:
     - Recipe name
     - Ingredient list
     - Description

Installation & Setup
1. Clone this repository
  git clone https://github.com/your-username/fridge-chef.git
  cd fridge-chef

2. Install dependencies
  Make sure Python is installed.
  Then run:
  pip install flask
  (Or if pip isn’t recognised):
  python -m pip install flask

3. Run the app
  python app.py

4. Open in browser
  Visit:
  http://127.0.0.1:5000/

You now have your recipe recommender running locally!
This project is open-source and free to use, modify, and share.
