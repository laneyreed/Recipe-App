# Technical Overview - PlateShare Recipe Application

## Architecture & Implementation

### 1. Backend Implementation (Flask)

#### Application Structure
The backend is built using **Flask**, a lightweight Python web framework that follows the WSGI standard. The application uses a traditional server-side rendering approach with Jinja2 templating.

```python
# Core Flask application setup
app = Flask(__name__)

# Database connection configuration
DRIVER_NAME = 'SQL SERVER'
SERVER_NAME = 'SHANNONHP\MSSQLSERVER01'
DATABASE_NAME = 'VeganRecipes'
```

#### Database Integration
- **Database Engine**: Microsoft SQL Server
- **Connection Library**: pypyodbc (Python ODBC interface)
- **Connection Management**: Single persistent connection with cursor-based query execution
- **Security**: Trusted authentication using Windows Authentication

#### Route Implementation

**1. Home Route (`/`)**
```python
@app.route("/")
def home():
    return render_template("index.html")
```
- Simple static route serving the homepage template
- No database interaction required

**2. Recipe Categories (`/recipes-categories`)**
```python
@app.route("/recipes-categories")
def get_recipe_categories():
    # Database query execution with proper cursor management
    local_cursor = conn.cursor()
    try:
        recipes_cursor = local_cursor.execute("SELECT * FROM recipe_types")
        # Data processing and list conversion
    finally:
        local_cursor.close()
```
- Implements proper resource management with try/finally blocks
- Converts database rows to Python lists for template rendering

**3. Dynamic Recipe Filtering (`/recipes/type/<recipe_type>`)**
```python
@app.route("/recipes/type/<recipe_type>")
def get_recipes_by_type(recipe_type):
    # Input validation against allowed recipe types
    valid_recipe_types = ["appetizers", "breakfast", "soups", "salads", ...]
    if recipe_type not in valid_recipe_types:
        return f"Unknown recipe type: {recipe_type}", 404
```
- URL parameter validation for security
- Parameterized queries to prevent SQL injection
- RESTful URL structure

**4. Recipe Details (`/recipes/<int:recipe_id>`)**
```python
@app.route("/recipes/<int:recipe_id>")
def get_recipe_details(recipe_id):
    # Multiple related database queries
    # 1. Recipe basic information with author join
    # 2. Recipe ingredients with measurement units
    # 3. Cooking instructions ordered by step number
```
- Complex multi-table JOIN operations
- Integer type conversion and validation
- Three separate optimized queries for different data aspects

**5. Search Functionality (`/query_search_results`)**
```python
def search_recipes_query():
    query_search_term = request.args.get('querySearchTerm', default='', type=str).strip()
    # Input sanitization for security
    if not all(c.isalnum() or c.isspace() for c in query_search_term):
        return "Invalid search term...", 400
```
- GET parameter handling with Flask's request object
- Input validation and sanitization
- LIKE queries with wildcard matching

### 2. Database Schema Design

#### Core Tables Structure
Based on the SQL queries in the application:

```sql
-- Recipe Types (Categories)
recipe_types: recipe_type_id, recipe_type_name

-- Authors
authors: author_id, author_name

-- Recipes (Main entity)
recipes: recipe_id, recipe_name, recipe_description, prep_time, 
         cook_time, author_id, recipe_type_id, recipe_image_url

-- Ingredients
ingredients: ingredient_id, ingredient_name

-- Measurement Units
measurement_units: measurement_unit_id, measurement_unit_name

-- Recipe-Ingredient Junction (Many-to-Many)
recipe_ingredient: recipe_id, ingredient_id, quantity, measurement_unit_id

-- Instructions
instructions: recipe_id, step_number, instruction_text
```

#### Relationship Design
- **One-to-Many**: Authors → Recipes, Recipe Types → Recipes
- **Many-to-Many**: Recipes ↔ Ingredients (via recipe_ingredient table)
- **Composite Keys**: Instructions use (recipe_id, step_number)

### 3. Frontend Implementation

#### Template Architecture
**Base Template Pattern**
```html
<!-- base.html - Master template -->
<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Bootstrap 5.3.8 CDN integration -->
    <!-- Custom CSS modular loading -->
</head>
<body>
    <!-- Fixed navigation with dropdown menus -->
    <!-- Content blocks for inheritance -->
    <!-- Footer with subscription form -->
</body>
```

**Template Inheritance Structure**
- `base.html`: Master template with navigation, footer, and block definitions
- Child templates extend base and override specific content blocks
- Reusable components in `includes/` folder for modularity

#### Responsive Design Implementation
**CSS Architecture**
```
static/css/
├── main.css           # Global styles, layout, navigation
├── base.css           # Base component styles
├── category-cards.css # Recipe category grid styling  
├── featured.css       # Homepage featured section
└── recipe.css         # Recipe detail page styles
```

**Bootstrap Integration**
- Bootstrap 5.3.8 for responsive grid system
- Custom CSS overrides for brand-specific styling
- Mobile-first responsive approach
- Component-based styling (cards, navigation, forms)

#### JavaScript Functionality
- Bootstrap JavaScript bundle for interactive components
- Dropdown menu functionality
- Responsive navigation toggle
- Form handling for search functionality

### 4. Security Implementation

#### SQL Injection Prevention
```python
# Parameterized queries throughout the application
local_cursor.execute("SELECT * FROM recipes WHERE recipe_id = ?", [recipe_id])
```

#### Input Validation
```python
# Search term sanitization
if not all(c.isalnum() or c.isspace() for c in query_search_term):
    return "Invalid search term...", 400
```

#### Type Safety
- Flask route decorators with type hints (`<int:recipe_id>`)
- Explicit type conversion and validation
- Error handling with appropriate HTTP status codes

### 5. Performance Considerations

#### Database Optimization
- **Cursor Management**: Proper resource cleanup with try/finally blocks
- **Query Optimization**: JOINs instead of multiple queries where possible
- **Indexed Lookups**: Primary key and foreign key relationships

#### Frontend Performance  
- **CDN Usage**: Bootstrap loaded from CDN for caching benefits
- **Modular CSS**: Separate stylesheets to reduce unnecessary loading
- **Image Optimization**: Resized logo variants for different contexts

### 6. Development Patterns

#### Error Handling
- Database connection error recovery
- 404 responses for invalid routes/parameters
- Input validation with user-friendly error messages

#### Code Organization
- Single-file Flask application (appropriate for project size)
- Separation of concerns: routing, data processing, presentation
- Consistent naming conventions throughout codebase

#### Template Rendering
- Server-side rendering for better SEO and performance
- Jinja2 templating with loops, conditionals, and filters
- Data passed as Python lists/dictionaries to templates

**This architecture provides a solid foundation the recipe application with room for future enhancements like user authentication, recipe submission, and advanced search capabilities.**
