import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import psycopg2

class RecipeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Recipe Management System")

        # Connect to the database
        self.conn = psycopg2.connect(
            dbname="recipetest",
            user="Lawunn",
            host="localhost"
        )
        self.cur = self.conn.cursor()

        # Create the GUI
        self.create_widgets()

        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)

    def create_widgets(self):
        # Create a frame for the navigation bar
        self.navbar = tk.Frame(self.root)
        self.navbar.grid(sticky="nsew")

        for i in range(6):
            self.navbar.columnconfigure(i, weight=1)

        # Place the search entry and button in the navigation bar
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(self.navbar, textvariable=self.search_var, width=30)
        self.search_entry.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")  # Use grid instead of pack

        # Place the buttons in the navigation bar

        self.search_button = tk.Button(self.navbar, text="Search by recipe", command=self.search_by_recipe)
        self.search_button.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.search_button = tk.Button(self.navbar, text="Search by ingredients", command=self.search_recipes_by_ingredient)
        self.search_button.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")  # Use grid instead of pack

        self.search_button = tk.Button(self.navbar, text="Search by category", command=self.search_recipes_by_category)
        self.search_button.grid(row=0, column=3, padx=10, pady=10, sticky="nsew")

        self.refresh_button = tk.Button(self.navbar, text="Refresh", command=self.refresh_recipes)
        self.refresh_button.grid(row=0, column=4, padx=10, pady=10, sticky="nsew")  # Use grid instead of pack

        self.add_button = tk.Button(self.navbar, text="Add Recipe", command=self.add_recipe)
        self.add_button.grid(row=0, column=5, padx=10, pady=10, sticky="nsew")  # Use grid instead of pack

        self.delete_button = tk.Button(self.navbar, text="Delete Recipe", command=self.delete_recipe)
        self.delete_button.grid(row=0, column=6, padx=10, pady=10, sticky="nsew")  # Use grid instead of pack

        # Place the update button in the navigation bar
        self.update_button = tk.Button(self.navbar, text="Update Recipe", command=self.update_recipe)
        self.update_button.grid(row=0, column=7, padx=10, pady=10, sticky="nsew")

        self.add_allergen_button = tk.Button(self.navbar, text="Add Allergen to Ingredient", command=self.add_allergen)
        self.add_allergen_button.grid(row=0, column=8, padx=10, pady=10, sticky="nsew")

        self.recipe_listbox = tk.Listbox(self.root, width=50)
        self.recipe_listbox.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.recipe_listbox.bind('<<ListboxSelect>>', self.show_recipe_details)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.refresh_recipes()

    def search_by_recipe(self):
        search_recipe = self.search_var.get()
        self.recipe_listbox.delete(0, tk.END)

        if search_recipe:
            self.cur.execute("SELECT title FROM recipes WHERE title = %s", (search_recipe,))
            recipe = self.cur.fetchone()
            if recipe:
                self.recipe_listbox.insert(tk.END, recipe[0])
            else:
                messagebox.showinfo("Search Results", "No recipes found with that name.")

    def search_recipes_by_ingredient(self):
        # Get the ingredient to search for
        search_ingredient = self.search_var.get()

        # Clear the listbox
        self.recipe_listbox.delete(0, tk.END)

        # Check if the search entry is not empty
        if search_ingredient:
            # Fetch recipes from the database that have the specified ingredient
            self.cur.execute("""
                SELECT DISTINCT r.title
                FROM recipes r
                INNER JOIN recipe_ingredients ri ON r.id = ri.recipe_id
                INNER JOIN ingredients i ON ri.ingredient_id = i.id
                WHERE i.name = %s
                """, (search_ingredient,))
            recipes = self.cur.fetchall()

            # Check if any recipes were found
            if recipes:
                for recipe in recipes:
                    self.recipe_listbox.insert(tk.END, recipe[0])
            else:
                messagebox.showinfo("Search Results", "No recipes found with that ingredient.")

    def search_recipes_by_category(self):
        # Get the category to search for
        search_category = self.search_var.get()

        # Clear the listbox
        self.recipe_listbox.delete(0, tk.END)

        # Check if the search entry is not empty
        if search_category:
            # Fetch recipes from the database that are in the specified category
            self.cur.execute("""
                SELECT DISTINCT r.title
                FROM recipes r
                INNER JOIN categories c ON r.category_id = c.id
                WHERE c.name = %s
                """, (search_category,))
            recipes = self.cur.fetchall()

            # Check if any recipes were found
            if recipes:
                for recipe in recipes:
                    self.recipe_listbox.insert(tk.END, recipe[0])
            else:
                messagebox.showinfo("Search Results", "No recipes found in that category.")

    def refresh_recipes(self):
        # Clear the listbox
        self.recipe_listbox.delete(0, tk.END)

        # Fetch recipes from the database
        self.cur.execute("SELECT title FROM recipes")
        recipes = self.cur.fetchall()
        for recipe in recipes:
            self.recipe_listbox.insert(tk.END, recipe[0])

    def add_recipe(self):
        title = simpledialog.askstring("Input", "What is the recipe name?")
        cooking_time = simpledialog.askstring("Input", "What is the cooking time in minutes?")
        instructions = simpledialog.askstring("Input", "What are the instructions?")
        cooking_hardware = simpledialog.askstring("Input", "What are the cooking hardwares?")
        ingredients = simpledialog.askstring("Input", "What are the ingredients?")
        category_name = simpledialog.askstring("Input", "What is the category?")

        # Check if the category exists, if not, insert it
        self.cur.execute("SELECT id FROM categories WHERE name = %s", (category_name,))
        category_id = self.cur.fetchone()
        if not category_id:
            self.cur.execute("INSERT INTO categories (name) VALUES (%s) RETURNING id", (category_name,))
            category_id = self.cur.fetchone()[0]
        else:
            category_id = category_id[0]

        # Insert recipe
        self.cur.execute("INSERT INTO recipes (title, cooking_time, instructions, category_id) VALUES (%s, %s, %s, %s) RETURNING id",
                     (title, cooking_time, instructions, category_id))
        recipe_id = self.cur.fetchone()[0]

        # Insert cooking hardware
        hardware_list = cooking_hardware.split(",")
        for hardware in hardware_list:
            hardware = hardware.strip()
            self.cur.execute("SELECT id FROM cooking_hardware WHERE name = %s", (hardware,))
            existing_hardware = self.cur.fetchone()
            if not existing_hardware:
                self.cur.execute("INSERT INTO cooking_hardware (name) VALUES (%s)", (hardware,))
                self.conn.commit()  # Commit after each insertion to ensure hardware ID is available
                self.cur.execute("SELECT id FROM cooking_hardware WHERE name = %s", (hardware,))
                existing_hardware = self.cur.fetchone()
            self.cur.execute("INSERT INTO recipe_hardware (recipe_id, hardware_id) VALUES (%s, %s)",
                         (recipe_id, existing_hardware[0]))

        # Insert ingredients
        ingredient_list = ingredients.split(",")
        for ingredient in ingredient_list:
            ingredient = ingredient.strip()
            self.cur.execute("SELECT id FROM ingredients WHERE name = %s", (ingredient,))
            existing_ingredient = self.cur.fetchone()
            if not existing_ingredient:
                self.cur.execute("INSERT INTO ingredients (name) VALUES (%s)", (ingredient,))
                self.conn.commit()  # Commit after each insertion to ensure ingredient ID is available
                self.cur.execute("SELECT id FROM ingredients WHERE name = %s", (ingredient,))
                existing_ingredient = self.cur.fetchone()
            self.cur.execute("INSERT INTO recipe_ingredients (recipe_id, ingredient_id) VALUES (%s, %s)",
                         (recipe_id, existing_ingredient[0]))

        self.conn.commit()
        messagebox.showinfo("Success", "Recipe added successfully.")

        self.refresh_recipes()

    def show_recipe_details(self, event=None):
        # Get the selected recipe name
        selected_index = self.recipe_listbox.curselection()
        if not selected_index:
            return
        selected_recipe = self.recipe_listbox.get(selected_index)

        # Fetch the details of the selected recipe from the database
        self.cur.execute("""
            SELECT 
                recipes.title, 
                recipes.cooking_time, 
                recipes.instructions, 
                categories.name, 
                ARRAY_AGG(DISTINCT ingredients.name), 
                ARRAY_AGG(DISTINCT cooking_hardware.name)
            FROM recipes
            INNER JOIN categories ON recipes.category_id = categories.id
            LEFT JOIN recipe_ingredients ON recipes.id = recipe_ingredients.recipe_id
            LEFT JOIN ingredients ON recipe_ingredients.ingredient_id = ingredients.id
            LEFT JOIN recipe_hardware ON recipes.id = recipe_hardware.recipe_id
            LEFT JOIN cooking_hardware ON recipe_hardware.hardware_id = cooking_hardware.id
            WHERE recipes.title = %s
            GROUP BY recipes.title, recipes.cooking_time, recipes.instructions, categories.name
        """, (selected_recipe,))
        recipe_details = self.cur.fetchone()

        # Display basic recipe details
        recipe_info = 'N/A'  # Default value in case no details are found
        if recipe_details:
            title = recipe_details[0]
            cooking_time = recipe_details[1]
            instructions = recipe_details[2]
            category = recipe_details[3]
            ingredients = ', '.join(filter(None, recipe_details[4])) if recipe_details[4] else 'N/A'
            cooking_hardware = ', '.join(filter(None, recipe_details[5])) if recipe_details[5] else 'N/A'
            recipe_info = f"Title: {title}\nCooking Time: {cooking_time}\nInstructions: {instructions}\nCategory: {category}\nIngredients: {ingredients}\nCooking Hardware: {cooking_hardware}"

        messagebox.showinfo("Recipe Details", recipe_info)


    def delete_recipe(self):
    # Get the selected recipe name
        selected_recipe = self.recipe_listbox.get(self.recipe_listbox.curselection())

    # Confirm the deletion with the user
        confirmation = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the recipe '{selected_recipe}'?")

        if confirmation:
        # Get the ID of the recipe to be deleted
            self.cur.execute("SELECT id FROM recipes WHERE title = %s", (selected_recipe,))
            recipe_id = self.cur.fetchone()[0]

        try:
            # Delete related records from the recipe_ingredients table
            self.cur.execute("DELETE FROM recipe_ingredients WHERE recipe_id = %s", (recipe_id,))
            # Delete related records from the recipe_hardware table
            self.cur.execute("DELETE FROM recipe_hardware WHERE recipe_id = %s", (recipe_id,))
            # Delete the recipe from the recipes table
            self.cur.execute("DELETE FROM recipes WHERE id = %s", (recipe_id,))
            self.conn.commit()
            # Refresh the list of recipes
            self.refresh_recipes()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete recipe: {e}")

        # Refresh the list of recipes
        self.refresh_recipes()

    def update_recipe(self):
    # Get the selected recipe name
        selected_recipe = self.recipe_listbox.get(self.recipe_listbox.curselection())
    
    # Fetch the ID of the selected recipe
        self.cur.execute("SELECT id FROM recipes WHERE title = %s", (selected_recipe,))
        recipe_id = self.cur.fetchone()
        if not recipe_id:
            messagebox.showerror("Error", "Selected recipe not found.")
            return
        recipe_id = recipe_id[0]

    # Prompt the user to enter updated details
        updated_title = simpledialog.askstring("Input", "Enter updated recipe name:")
        updated_cooking_time = simpledialog.askstring("Input", "Enter updated cooking time in minutes:")
        updated_instructions = simpledialog.askstring("Input", "Enter updated instructions:")
        updated_category = simpledialog.askstring("Input", "Enter updated category:")

    # Check if the updated category already exists in the database, if not, insert it
        self.cur.execute("SELECT id FROM categories WHERE name = %s", (updated_category,))
        category_id = self.cur.fetchone()
        if not category_id:
            self.cur.execute("INSERT INTO categories (name) VALUES (%s) RETURNING id", (updated_category,))
            category_id = self.cur.fetchone()[0]
        else:
            category_id = category_id[0]

    # Update the recipe details in the database
        try:
            self.cur.execute("UPDATE recipes SET title = %s, cooking_time = %s, instructions = %s, category_id = %s WHERE id = %s",
                         (updated_title, updated_cooking_time, updated_instructions, category_id, recipe_id))
            self.conn.commit()
            messagebox.showinfo("Success", "Recipe updated successfully.")
            self.refresh_recipes()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update recipe: {e}")


    def add_allergen(self):
        ingredient_name = simpledialog.askstring("Input", "What is the ingredient name?")
        allergen = simpledialog.askstring("Input", "What is the allergen?")

        # Fetch the ingredient
        self.cur.execute("SELECT allergens FROM ingredients WHERE name = %s", (ingredient_name,))
        existing_allergens = self.cur.fetchone()
        if existing_allergens is None:
            messagebox.showinfo("Error", "Ingredient not found.")
            return

        # Add the allergen
        existing_allergens = existing_allergens[0]
        if existing_allergens:
            new_allergens = existing_allergens + "," + allergen
        else:
            new_allergens = allergen

        # Update the ingredient
        self.cur.execute("UPDATE ingredients SET allergens = %s WHERE name = %s", (new_allergens, ingredient_name))

        self.conn.commit()
        messagebox.showinfo("Success", "Allergen added successfully.")

    def on_close(self):
        # Close the database connection
        self.cur.close()
        self.conn.close()

        # Close the application
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = RecipeApp(root)
    root.mainloop()
