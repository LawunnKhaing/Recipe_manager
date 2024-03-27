import psycopg2

# Connect to the database
conn = psycopg2.connect(
    dbname="recipe_database",
    user="your_username",
    password="your_password",
    host="localhost"
)

# Create a cursor object
cur = conn.cursor()

# Example: Insert a new recipe
cur.execute("INSERT INTO recipes (title, cooking_time, instructions) VALUES (%s, %s, %s)", 
            ("Spaghetti Carbonara", "00:30:00", "1. Boil water\n2. Cook pasta\n3. Fry bacon and garlic\n4. Mix everything together"))
conn.commit()

# Example: Fetch all recipes
cur.execute("SELECT * FROM recipes")
recipes = cur.fetchall()
for recipe in recipes:
    print(recipe)

# Close cursor and connection
cur.close()
conn.close()
