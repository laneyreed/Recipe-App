from flask import Flask, render_template, request
import pypyodbc as odbc
# import requests


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

@app.route("/all-recipes")
def all_recipes():
    local_cursor = conn.cursor()
    try:
        all_recipes_cursor = local_cursor.execute("SELECT recipe_id, recipe_name, recipe_description, recipe_image_url FROM recipes")
        all_recipes_list = []
        for row in all_recipes_cursor:
            all_recipes_list.append(list(row))
    finally:
        local_cursor.close()

    return render_template("all_recipes.html", recipes=all_recipes_list)




@app.route("/recipes-categories")
def get_recipe_categories():
    local_cursor = conn.cursor()
    try:
        recipes_cursor = local_cursor.execute("SELECT * FROM recipe_types")
        recipeCategoriesList = []
        for row in recipes_cursor:
            recipeCategoriesList.append(list(row))
    finally:
        local_cursor.close()
    return render_template("category_list.html", categories=recipeCategoriesList)


@app.route("/recipes/type/<recipe_type>")
def get_recipes_by_type(recipe_type):
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
                recipes_list.append(list(row))
    finally:
         local_cursor.close()

    template_path = "recipes_by_category_list.html"
    return render_template(template_path, recipes=recipes_list, category_title=recipe_type)

@app.route("/recipes/<int:recipe_id>")
def get_recipe_details(recipe_id):
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

    finally:
        local_cursor.close()
    return render_template("recipe_detail.html", recipe_info=recipe_info_list, ingredients=recipe_ingredients_list, instructions=recipe_instructions_list)


@app.route("/query_search_results") # Example: http://localhost:5001/query_search_results?querySearchTerm=pasta
def search_recipes_query():
    query_search_term = request.args.get('querySearchTerm', default='', type=str).strip()
    #validate input to prevent SQL injection
    # only allow alphanumeric and spaces
    if not all(c.isalnum() or c.isspace() for c in query_search_term):
        return "Invalid search term. Only alphanumeric characters and spaces are allowed.", 400
    
    local_cursor = conn.cursor()
    if not query_search_term:
        search_results_list = []
        search_results_cursor = local_cursor.execute("SELECT recipe_id, recipe_name, recipe_description, recipe_image_url FROM recipes")
        for row in search_results_cursor:
            search_results_list.append(list(row))
        #print(search_results_list)
        return render_template("search_results.html", recipes=search_results_list)

    
    try:
        search_results_cursor = local_cursor.execute(
            """
            SELECT recipe_id, recipe_name, recipe_description, recipe_image_url FROM recipes
            WHERE recipe_name LIKE ? OR recipe_description LIKE ?;
            """, [f'%{query_search_term}%', f'%{query_search_term}%']
        )

        search_results_list = []
        for row in search_results_cursor:
            search_results_list.append(list(row))
        #print(search_results_list)
    finally:
        local_cursor.close()

    return render_template("search_results.html", recipes=search_results_list, search_term=query_search_term)

if __name__ == "__main__":
    app.run(debug=True)
