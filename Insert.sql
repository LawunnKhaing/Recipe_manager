-- Insert categories
INSERT INTO categories (name) VALUES ('Desserts'), ('Pizza'), ('Pasta');

-- Insert ingredients
INSERT INTO ingredients (name, allergens) VALUES ('Flour', NULL), ('Sugar', NULL), ('Eggs', 'Gluten');

-- Insert cooking hardware
INSERT INTO cooking_hardware (name) VALUES ('Oven'), ('Stove'), ('Mixer');

-- Insert recipes
INSERT INTO recipes (title, cooking_time, instructions, category_id)
VALUES ('Chocolate Cake', '60', 'Bake at 350°F for 30 minutes', 1),
       ('Margherita Pizza', '20', 'Bake at 400°F for 15 minutes', 2),
       ('Spaghetti Carbonara', '30', 'Boil pasta, fry bacon, mix with egg sauce', 3);

-- Insert recipe-ingredient relationships
INSERT INTO recipe_ingredients (recipe_id, ingredient_id) VALUES (1, 1), (1, 2), (1, 3);

-- Insert recipe-hardware relationships
INSERT INTO recipe_hardware (recipe_id, hardware_id) VALUES (1, 1), (2, 1), (3, 2);

