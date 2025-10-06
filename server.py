from flask import Flask, render_template
import pypyodbc as odbc
import requests


app = Flask(__name__)

DRIVER_NAME = 'SQL SERVER'
SERVER_NAME = 'SHANNONHP\MSSQLSERVER01'
DATABASE_NAME = 'VeganRecipes'


connection_string = f"""
    DRIVER={{{DRIVER_NAME}}};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trust_Connection=yes;
"""




conn = odbc.connect(connection_string)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/recipes-categories")
def get_recipe_categories():
    local_cursor = conn.cursor()
    try:
        recipes_cursor = local_cursor.execute("SELECT * FROM recipe_types")
        recipeCategoriesList = []
        for row in recipes_cursor:
            #make the tuple into a list and append to recipeCategoriesList
            recipeCategoriesList.append(list(row))
        # recipeCategoriesList is a list of lists, each inner list contains the fields of a recipe category
        # [recipe_type_id, recipe_type_name, image_url, category_description]
        #print(recipeCategoriesList)
    finally:
        local_cursor.close()
    return render_template("category_list.html", categories=recipeCategoriesList)


@app.route("/recipes/type/<recipe_type>")
def get_recipes_by_type(recipe_type):
    # Validate the recipe_type to prevent SQL injection
    # without this validation, a malicious user could potentially manipulate the SQL query by injecting SQL code through the recipe_type parameter
    # this validation ensures that only known recipe types are processed
    # this is a simple validation, in a real-world application, you might want to implement a more robust validation mechanism
    # for example, you could check against a list of recipe types fetched from the database
    valid_recipe_types = ["appetizers", "breakfast", "soups", "salads", "sides", "entrees", "desserts", "beverages"]
    if recipe_type not in valid_recipe_types:
        return f"Unknown recipe type: {recipe_type}", 404

    local_cursor = conn.cursor()
    try:
         recipes_cursor = local_cursor.execute("""
                                               SELECT * FROM recipes
                                               WHERE recipe_type_id = (
                                               SELECT recipe_type_id FROM recipe_types WHERE recipe_type_name = ?
                                               );
                                               """, [recipe_type])
         

         recipes_list = []
         for row in recipes_cursor:
                recipes_list.append(list(row)) # make the tuple into a list and append to recipes_list
            # recipes_list is a list of lists, each inner list contains the fields of a recipe
            # [recipe_id, recipe_name, recipe_description, recipe_prep_time, recipe_cook_time, recipe_author_id, recipe_type_id, recipe_image_url]
            #print(recipes_list)
    finally:
         local_cursor.close()

    template_path = "recipe_cards_list.html"
    return render_template(template_path, recipes=recipes_list, category_title=recipe_type)


#create a route to display a specific recipe
@app.route("/recipes/<int:recipe_id>")
def get_recipe_details(recipe_id):
    local_cursor = conn.cursor()
    try:

        # Fetch the recipe details
        recipe_cursor = local_cursor.execute(
            "SELECT * FROM recipes WHERE recipe_id = ?", [recipe_id]
        )
        recipe = recipe_cursor.fetchone()
        #print(recipe)# (recipe_id, recipe_name, recipe_description, recipe_prep_time, recipe_cook_time, recipe_author_id, recipe_type_id)
        if recipe is None:
            return f"Recipe with ID {recipe_id} not found.", 404
        recipe_details_list = []
        # Use slicing over individual assignments
        #  appending each field individually is a valid approach, it is verbose and prone to error if the number of desired fields changes
        # this single line slicing operation accomplishes the same goal more efficiently and elegantly
        # it is the "Pythonic" way to handle such a task
        recipe_details_list = list(recipe[:7])# this will get the first 7 fields of the recipe tuple and convert it to a list


        # Fetch the ingredients for the recipe
        ingredients_cursor = local_cursor.execute(
            """
            SELECT ri.quantity, mu.measurement_unit_name, i.ingredient_name
            FROM recipes AS r
            INNER JOIN recipe_ingredient AS ri ON r.recipe_id = ri.recipe_id
            INNER JOIN measurement_units AS mu ON ri.measurement_unit_id = mu.measurement_unit_id
            INNER JOIN ingredients AS i ON ri.ingredient_id = i.ingredient_id
            WHERE r.recipe_id = ?
            """, [recipe_id]
        )
        recipe_ingredients = ingredients_cursor.fetchall()
        if recipe_ingredients is None:
            return f"Recipe with ID {recipe_id} ingredients not found.", 404
        
        #Fetch the author name for the recipe
        author_cursor = local_cursor.execute(
            """
            SELECT author_name
            FROM authors
            WHERE author_id = ?
            """, [recipe[5]] # recipe[5] is the author_id from the recipe details
        )
        author = author_cursor.fetchone()
        if author is None:
            return f"Recipe with ID {recipe_id} author not found.", 404
        recipe_details_list.append(author[0])  # Append the author name to the recipe details
        print(recipe_details_list)  # For debugging purposes
    finally:
        local_cursor.close()
    return render_template("recipe_detail.html", recipe=recipe_details_list, ingredients=recipe_ingredients)



if __name__ == "__main__":
    app.run(debug=True)
