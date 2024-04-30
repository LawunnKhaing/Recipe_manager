---
title: Food Recipe Management System
output: 
  pdf_document:
    latex_engine: pdflatex
    toc: true
    toc_depth: 2
    number_sections: true
geometry: margin=1in
fontsize: 11pt
linestretch: 1.2
---

# The Final Project of Databases: Food Recipe Management System

Created by: Lawunn Khaing, Jesse Sillman, Huy Tran, Tran Truong (ITMI22SP)

## Introduction

This report examines the application of SQL in structuring relational databases via PostgreSQL, complemented by a Python-based graphical user interface (GUI) to facilitate user interaction with the database. The application's purpiose is to catalog recipes along with their necessary ingredients, cooking hardware, and categories. This system not only allows for the storage and retrieval of recipe data but also supports features like recipe updating, deletion, and advanced searching capabilities based on ingredients and categories.

## Table of Contents

1. [Database Schema Overview](#database-schema-overview)
   - [Design Choices](#design-choices)
   - [Creation of Table](#creation-of-tables)
   - [Explanation of Columns](#explanation-of-columns)
   - [Inserting Data](#ingredients-table)
   - [Updating and Deleting](#)
   - [ER-Diagram](#er-diagram)
2. [SQL Commands and Queries with Python](#sql-commands-and-queries-with-python)
   - [Searching Recipes by Ingredient](#searching-recipes-by-ingredient)
   - [Searching Recipes by Category](#searching-recipes-by-category)
   - [Refresing Recipes](#refresing-recipes)
   - [Add Recipe](#add-recipe)
   - [Delete Recipe](#delete-recipe)
   - [Update Recipe](#update-recipe)
   - [Add Allergen to an Ingredient](#add-allergen-to-an-ingredient)
   - [Displaying Allergens in a Warning](#displaying-allergens-in-a-warning)
   
## Database Schema Overview

In designing the database schema for the Food Recipe Management System, we aimed for normalization to minimize redundancy and ensure data integrity. The key entities identified were `recipes`, `ingredients`, `cooking hardware`, and `categories`.

### Design Choices

- **Normalization**: By separating entities into their own tables and using junction tables for many-to-many relationships, we ensure that the database is normalized, reducing redundancy and minimizing the risk of data inconsistencies.

- **Flexibility**: The chosen design allows for flexibility in managing recipes, ingredients, cooking hardware, and categories. New recipes can be easily added, and existing recipes can be updated or deleted without affecting other parts of the system.

- **Data Integrity**: By enforcing foreign key constraints and using junction tables to represent complex relationships, we maintain data integrity within the database. This ensures that only valid and consistent data is stored.

- **Scalability**: The modular design of the database schema allows for scalability as the system grows. Additional features and entities can be added without major modifications to the existing structure.

- **Ease of Maintenance**: Separating entities into their own tables and using meaningful foreign keys improves the maintainability of the database. It becomes easier to troubleshoot issues, update data, and add new functionality.

### Creation of Tables

The following SQL Query was used to create the table:

```sql
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE recipes (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    cooking_time TEXT NOT NULL,
    instructions TEXT NOT NULL,
    category_id INTEGER NOT NULL REFERENCES categories(id)
);

CREATE TABLE ingredients (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    allergens TEXT
);

CREATE TABLE cooking_hardware (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE recipe_ingredients (
    recipe_id INTEGER NOT NULL REFERENCES recipes(id),
    ingredient_id INTEGER NOT NULL REFERENCES ingredients(id),
    PRIMARY KEY (recipe_id, ingredient_id)
);

CREATE TABLE recipe_hardware (
    recipe_id INTEGER NOT NULL REFERENCES recipes(id),
    hardware_id INTEGER NOT NULL REFERENCES cooking_hardware(id),
    PRIMARY KEY (recipe_id, hardware_id)
);

```

### Explanation of Columns

#### Categories Table

- `id`: An auto-incrementing integer serving as the primary key for the table, uniquely identifying each category.
- `name`: A text field storing the name of the category. This field is marked as `NOT NULL` to ensure that every category has a name associated with it.

#### Recipes Table

- `id`: Similar to the categories table, this is an auto-incrementing integer serving as the primary key for the table, uniquely identifying each recipe.
- `title`: A text field storing the title or name of the recipe. This field is marked as `NOT NULL` to ensure that every recipe has a title.
- `cooking_time`: A text field storing the cooking time required for the recipe.
- `instructions`: A text field storing the instructions or steps to prepare the recipe.
- `category_id`: An integer field serving as a foreign key referencing the `id` column of the categories table. This establishes a relationship between recipes and categories, indicating the category to which each recipe belongs.

#### Ingredients Table

- `id`: An auto-incrementing integer serving as the primary key for the table, uniquely identifying each ingredient.
- `name`: A text field storing the name of the ingredient. This field is marked as `NOT NULL` to ensure that every ingredient has a name.
- `allergens`: A text field storing any allergens associated with the ingredient. This field can contain information about allergens to help users with dietary restrictions or allergies.

#### Cooking Hardware Table

- `id`: An auto-incrementing integer serving as the primary key for the table, uniquely identifying each piece of cooking hardware.
- `name`: A text field storing the name of the cooking hardware (e.g., oven, stove). This field is marked as `NOT NULL` to ensure that every piece of cooking hardware has a name.

#### Recipe Ingredients Table

- `recipe_id`: An integer field serving as a foreign key referencing the `id` column of the recipes table. This establishes a relationship between recipes and ingredients, indicating which ingredients are used in each recipe.
- `ingredient_id`: An integer field serving as a foreign key referencing the `id` column of the ingredients table. This establishes a relationship between recipes and ingredients, indicating which ingredients are used in each recipe.
- `PRIMARY KEY (recipe_id, ingredient_id)`: This constraint ensures that each combination of `recipe_id` and `ingredient_id` is unique, preventing duplicate entries and maintaining data integrity.

#### Recipe Hardware Table

- `recipe_id`: An integer field serving as a foreign key referencing the `id` column of the recipes table. This establishes a relationship between recipes and cooking hardware, indicating which cooking hardware is used in each recipe.
- `hardware_id`: An integer field serving as a foreign key referencing the `id` column of the cooking hardware table. This establishes a relationship between recipes and cooking hardware, indicating which cooking hardware is used in each recipe.
- `PRIMARY KEY (recipe_id, hardware_id)`: This constraint ensures that each combination of `recipe_id` and `hardware_id` is unique, preventing duplicate entries and maintaining data integrity.



### Inserting Data

Here is a sample code of how we can insert data into tables.



### ER-Diagram 
  ![ER Diagram](./docs/er-diagram.png)



## SQL Commands and Queries with Python

This part covers the SQL commands and queries used within the Pyton code to interact with the PostgreSQL database and manage data within the Recipe Manage System GUI.

### Searching Recipes by Ingredient

The following query retrieves the titles of recipes from `recipes` table where ingredients match a specified ingredient:

```sql
SELECT r.title
FROM recipes r
INNER JOIN i ON r.id=i.recipe_id
WHERE i.name = %s;
```

Here's the breakdown of the query:

- `SELECT r.title`: Selects the `title` column from the `recipes` table.
- `FROM recipes r`: This specifies that the data is being retrieved from the `recipes` table and assigns it an alias `r`.
- `INNER JOIN ingredients i ON r.id = i.recipe.id`: This clause joins the `recipes` table (`r`) with the `ingredients` (`i`) table based on the condition that the `id` column matches the `recipe_id` column in `ingredients`.
- `WHERE i.name = %s`: This condition filters the joined result set to only include rows where the `name` column in the `ingredients` table matches the specified ingredient name (represented by %s).

**Note: In Python programming, `%s` is a placeholder used in SQL queries to represent a value that will be provided later due to prevent SQL injection attacks and to make the code more readable and maintainable.**

### Searching Recipes by Category

To search recipes based on their category, we utilized a SQL query similar to the one used for ingredient-based searching, as following:

```sql
SELECT r.title
FROM recipes r
WHERE r.category = %s;
```

This query retrieves the titles from the `recipes` table where the category matches a specified category value.

### Refresing Recipes

The following method refreshes the recipe listbox by clearing its contents and fetching all recipe titles from the database:

```sql
SELECT title FROM recipes
```

### Add Recipe

The following SQL query inserts a new recipe into the `recipes` table with the provided details and returns the ID of the inserted recipe:

```sql
INSERT INTO recipes (title, cooking_time, ingredients, instructions, cooking_hardware, category)
VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;
```

Here's the breakdown of the query:

- `INSERT INTO recipes`: Specifies that we are inserting data into the `recipes` table.
- `(title, cooking_time, ingredients, instructions, cooking_hardware, category)`: Lists the columns into which we are inserting data.
- `VALUES (%s, %s, %s, %s, %s, %s)`: Defines that we are providing values for each of the columns listed above.
- `RETURNING id`: This clause is used to return the ID of the newly inserted row.

### Delete Recipe

To delete a recipe, we typically use the DELETE statement:

```sql
DELETE FROM recipes WHERE title = %s;
```

Here's the breakdown of the query:

- `DELETE FROM recipes`: Specifies that we are deleting data from the `recipes` table.
- `WHERE title = %s`: Inserts a condition that filters the rows to be deleted, targeting the recipe with a specific title.

### Update Recipe

To update a recipe, we typically use the UPDATE statement:

```sql
UPDATE recipes
SET title = %s,
    cooking_time = %s,
    ingredients = %s,
    instructions = %s,
    cooking_hardware = %s,
    category = %s
WHERE title = %s;
```

Here's the breakdown of the query:

- `UPDATE recipes`: Specifies the `recipes` table to be updated.
- `SET`: Specifies the columns the user wants to update.
- `WHERE title = %s`: Specifies the condition for which rows should be updated. In this case, it updates the rows where the `title` matches the specified value.

### Add Allergen to an Ingredient

To add an allergen to an existing ingredient in the `ingredients` table, we can use the UPDATE statement similarly to update a recipe:

```sql
UPDATE ingredients 
SET allergens = %s 
WHERE name = %s;
```

### Displaying Allergens in a Warning

To display allergens in a warning message, we can use the following SQL query:

```sql
SELECT allergens FROM ingredients WHERE name = %s;
```

Here's the breakdown of the query:

- `SELECT allergens`: Selects the `allergens` column from the `ingredients` table.
- `FROM ingredients`: Specifies the `ingredients` table from which to retrieve data.
- `WHERE name = %s`: Specifies the condition for which rows to select. In this case, it selects the row where the `name` of the igredeient matches the specified value.

For each ingredient in the recipe, the application checks if there are any associated allergens. If an ingredient is found to have allergens, the application appends a warning to the recipe details.

---

This document was created from the `docs/REPORT.md` from this
[github repository](https://github.com/LawunnKhaing/Recipe_manager/tree/main).
