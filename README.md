# PlateShare - Vegan Recipe Web Application

A comprehensive Flask-based web application for browsing, searching, and viewing vegan recipes with a modern, responsive interface and robust database integration.

## 🌱 Project Overview

PlateShare is a full-stack web application designed to showcase and organize a curated collection of vegan recipes. The application follows a traditional MVC architecture using Flask as the backend framework, with SQL Server providing data persistence and Bootstrap ensuring responsive frontend design.

### 🎯 Core Functionality

**Recipe Management**
- Display recipes organized by categories (appetizers, breakfast, soups, salads, sides, entrees, desserts)
- Detailed recipe views with ingredients, cooking instructions, prep/cook times
- Featured recipes section for highlighting popular or seasonal content

**User Experience**  
- Responsive navigation with dropdown menu system
- Recipe search functionality across the database
- Clean, mobile-friendly interface using Bootstrap components
- Modular CSS architecture for maintainable styling

**Data Layer**
- SQL Server database integration using pypyodbc
- Structured data relationships for recipes, categories, ingredients, and instructions
- Database connection management and query execution

## ✨ Features

- **Recipe Categories**: Browse recipes by type (appetizers, breakfast, soups, salads, sides, entrees, desserts)
- **Recipe Details**: View comprehensive recipe information including ingredients, preparation time, and cooking time
- **Search Functionality**: Search for recipes by name or description
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
- [ ] User ratings and reviews
- [ ] Nutritional information display
- [ ] Recipe sharing capabilities
- [ ] Recipe export functionality (PDF/print)


---

*Made with 🌱 for the vegan community*











____________________________________
<!-- 
-- added Search functionality
-- added search results html file
-- changed recipe cards html file to be used for both search results and recipies by category
-- added all recipes html file
-- added drop down menu for recipes
-->