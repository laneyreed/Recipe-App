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
         recipes_cursor = local_cursor.execute(
             """
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
    #Validate recipe_id to prevent SQL injection
    if not isinstance(recipe_id, int) or recipe_id <= 0:
        return f"Invalid recipe ID: {recipe_id}", 404
    
    local_cursor = conn.cursor()
    try:

        # RECIPE INFO---------------------------------------------------------------------------------------------
        # get recipe_info: recipe_id, recipe_name, recipe_description, prep_time, cook_time, author_name
        recipe_info = local_cursor.execute(
            """
            SELECT r.recipe_id, r.recipe_name, r.recipe_description, r.prep_time, r.cook_time, a.author_name
            FROM recipes r
            JOIN authors a ON r.author_id = a.author_id
            WHERE r.recipe_id = ?;
            """, [recipe_id]
        )

        # make recipe_info into a list: [recipe_id, recipe_name, recipe_description, prep_time, cook_time, author_name]
        recipe_info_list = list(recipe_info.fetchone())

        # RECIPE INGREDIENTS---------------------------------------------------------------------------------------------
        # get ingredients for the recipe
        recipe_ingredients = local_cursor.execute(
            """
            SELECT ri.quantity, mu.measurement_unit_name, i.ingredient_name
            FROM recipe_ingredient ri
            JOIN measurement_units mu ON ri.measurement_unit_id = mu.measurement_unit_id
            JOIN ingredients i ON ri.ingredient_id = i.ingredient_id
            WHERE ri.recipe_id = ?;
            """, [recipe_id]
        )

        # make recipe_ingredients into a list of lists
        recipe_ingredients_list = []
        for row in recipe_ingredients:
            recipe_ingredients_list.append(list(row))
        # print(recipe_ingredients_list)

        # RECIPE INSTRUCTIONS---------------------------------------------------------------------------------------------
        # get instructions for the recipe
        recipe_instructions = local_cursor.execute(
            """
            SELECT step_number, instruction_text
            FROM instructions
            WHERE recipe_id = ?
            ORDER BY step_number;
            """, [recipe_id]
        )

        # make recipe_instructions into a list of lists
        recipe_instructions_list = []
        for row in recipe_instructions:
            recipe_instructions_list.append(list(row))
        # print(recipe_instructions_list)

    finally:
        local_cursor.close()
    # return render_template("recipe_detail.html", recipe=recipe_info_list, ingredients=recipe_ingredients)
    return render_template("recipe_detail.html", recipe_info=recipe_info_list, ingredients=recipe_ingredients_list, instructions=recipe_instructions_list)



if __name__ == "__main__":
    app.run(debug=True)
