# Vegan Recipe Web Application

A Flask-based web application for browsing and viewing vegan recipes, featuring a clean interface and database-driven content management.

## 🌱 About

This vegan recipe application provides users with a curated collection of plant-based recipes organized by categories. The app features a modern, responsive design with recipe categorization, detailed recipe views, and ingredient listings.

## ✨ Features

- **Recipe Categories**: Browse recipes by type (appetizers, breakfast, soups, salads, sides, entrees, desserts)
- **Recipe Details**: View comprehensive recipe information including ingredients, preparation time, and cooking time
- **Featured Recipes**: Highlighted recipes on the homepage for inspiration
- **Responsive Design**: Mobile-friendly interface with Bootstrap styling
- **Database Integration**: SQL Server database for reliable data storage and retrieval

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Database**: Microsoft SQL Server
- **Database Connectivity**: pypyodbc
- **Frontend**: HTML5, CSS3, Bootstrap
- **Template Engine**: Jinja2

## 🗃️ Database Schema

The application connects to a SQL Server database with the following key tables:

- **recipes**: Main recipe information (ID, name, description, prep/cook time, author, type)
- **recipe_ingredient**: Junction table linking recipes to ingredients with quantities
- **ingredients**: Ingredient master data
- **measurement_units**: Units of measurement for ingredients
- **recipe_types**: Recipe categories/types

## 🚀 Installation & Setup

### Prerequisites

- Python 3.x
- Microsoft SQL Server
- SQL Server ODBC Driver

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd Recipe-App
   ```

2. **Install required packages:**
   ```bash
   pip install flask pypyodbc
   ```

3. **Database Configuration:**
   - Update the database connection settings in `server.py`:
     ```python
     DRIVER_NAME = 'SQL SERVER'
     SERVER_NAME = 'YOUR_SERVER_NAME'
     DATABASE_NAME = 'VeganRecipes'
     ```

4. **Database Setup:**
   - Create a SQL Server database named `VeganRecipes`
   - Set up the required tables (recipes, ingredients, measurement_units, recipe_ingredient, etc.)
   - Populate with sample data

5. **Run the application:**
   ```bash
   python server.py
   ```

6. **Access the application:**
   - Open your browser and navigate to `http://localhost:5000`

## 🌐 Routes & Endpoints

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Homepage with featured recipes |
| `/recipes-categories` | GET | Recipe categories listing |
| `/recipes/type/<recipe_type>` | GET | Recipes filtered by category |
| `/recipes/<int:recipe_id>` | GET | Individual recipe details |

### Supported Recipe Types

- `appetizers` (ID: 1)
- `breakfast` (ID: 2)
- `soups` (ID: 3)
- `salads` (ID: 5)
- `sides` (ID: 6)
- `entrees` (ID: 7)
- `desserts` (ID: 10)

## 💻 Usage

1. **Browse Categories**: Visit the categories page to see all available recipe types
2. **View Recipes by Category**: Click on a category to see all recipes in that category
3. **Recipe Details**: Click on any recipe card to view detailed information including ingredients and cooking instructions
4. **Featured Recipes**: Check the homepage for highlighted recipes

## 🎨 Styling & Design

The application uses a modern, clean design approach with:

- **Bootstrap Framework**: For responsive layout and components
- **Custom CSS**: Modular stylesheets for different page sections
- **Image Assets**: High-quality food photography for visual appeal
- **Brand Identity**: Plate Share logo and consistent color scheme

## 🔧 Configuration

### Database Connection

Update the connection string in `server.py`:

```python
DRIVER_NAME = 'SQL SERVER'
SERVER_NAME = 'YOUR_SERVER_NAME'
DATABASE_NAME = 'VeganRecipes'

connection_string = f"""
    DRIVER={{{DRIVER_NAME}}};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trust_Connection=yes;
"""
```

### Debug Mode

The application runs in debug mode by default. For production, modify:

```python
if __name__ == "__main__":
    app.run(debug=False)  # Set to False for production
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🐛 Known Issues

- Database connection is not pooled (consider implementing connection pooling for production)
- Error handling could be enhanced for better user experience
- Recipe images are static (consider dynamic image handling)

## 🔮 Future Enhancements

- [ ] User authentication and recipe submission
- [ ] Recipe search functionality
- [ ] User ratings and reviews
- [ ] Nutritional information display
- [ ] Recipe sharing capabilities
- [ ] Mobile app version
- [ ] Recipe export functionality (PDF/print)

## 📞 Support

For questions or support, please open an issue in the GitHub repository.

---

*Made with 🌱 for the vegan community*











____________________________________
<!-- 
- add, instructions, servings to database
- Search functionality 

-- added instructions table
-- added image_url and category_description columns to the recipe_type table 
-- updated the /recipes-categories route
-  updated the category_list.html file
-- added recipe_image_url column to the recipes table
-- updated the recipe_cards_list.html to use images from database
-- updated the /recipes/type/<recipe_type> route
-- updated the /recipes/<int:recipe_id> route to get instruction from database and simpler sql queries
-- update the recipe details html file
-- added sql query to get the ingredients
-- changed the layout of the recipe ingredients and instructions cards to have independent heights
-->