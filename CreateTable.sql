CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE recipes (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    cooking_time TEXT NOT NULL,
    instructions TEXT NOT NULL,
    category_id INTEGER NOT NULL REFERENCES categories(id),
    UNIQUE (title, category_id)
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
