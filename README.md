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
- [ ] Recipe export functionality (PDF/print)


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