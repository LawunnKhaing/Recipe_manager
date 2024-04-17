import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import psycopg2

class RecipeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Recipe Management System")

        # Connect to the database
        self.conn = psycopg2.connect(
            dbname="recipe",
            user="ejesi",
            host="localhost"
        )
        self.cur = self.conn.cursor()

        self.cur.execute("CREATE SEQUENCE IF NOT EXISTS recipe_id_seq")
        self.cur.execute("CREATE SEQUENCE IF NOT EXISTS ingredient_id_seq")
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
        self.search_button = tk.Button(self.navbar, text="Search by ingredients", command=self.search_recipes_by_ingredient)
        self.search_button.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")  # Use grid instead of pack

        self.search_button = tk.Button(self.navbar, text="Search by category", command=self.search_recipes_by_category)
        self.search_button.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        self.refresh_button = tk.Button(self.navbar, text="Refresh", command=self.refresh_recipes)
        self.refresh_button.grid(row=0, column=3, padx=10, pady=10, sticky="nsew")  # Use grid instead of pack

        self.add_button = tk.Button(self.navbar, text="Add Recipe", command=self.add_recipe)
        self.add_button.grid(row=0, column=4, padx=10, pady=10, sticky="nsew")  # Use grid instead of pack

        self.delete_button = tk.Button(self.navbar, text="Delete Recipe", command=self.delete_recipe)
        self.delete_button.grid(row=0, column=5, padx=10, pady=10, sticky="nsew")  # Use grid instead of pack

        # Place the update button in the navigation bar
        self.update_button = tk.Button(self.navbar, text="Update Recipe", command=self.update_recipe)
        self.update_button.grid(row=0, column=6, padx=10, pady=10, sticky="nsew")

        self.add_allergen_button = tk.Button(self.navbar, text="Add Allergen to Ingredient", command=self.add_allergen)
        self.add_allergen_button.grid(row=0, column=7, padx=10, pady=10, sticky="nsew")

        self.recipe_listbox = tk.Listbox(self.root, width=50)
        self.recipe_listbox.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.recipe_listbox.bind('<<ListboxSelect>>', self.show_recipe_details)



        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.refresh_recipes()

    def search_recipes_by_ingredient(self):
        # Get the ingredient to search for
        search_ingredient = self.search_var.get()

    # Clear the listbox
        self.recipe_listbox.delete(0, tk.END)

    # Check if the search entry is not empty
        if search_ingredient:
        # Fetch recipes from the database that have the specified ingredient
            self.cur.execute("""
                SELECT r.title
                FROM recipes r
                INNER JOIN ingredients i ON r.id = i.recipe_id
                WHERE i.name = %s
                """, (search_ingredient,))
            recipes = self.cur.fetchall()

        # Check if any recipes were found
        if recipes:
            for recipe in recipes:
                self.recipe_listbox.insert(tk.END, recipe[0])
        else:
            messagebox.showinfo("Search Results", "No recipes found with that ingredient.")

        # Refresh the recipes list if the search field is empty
        self.refresh_recipes()

    def search_recipes_by_category(self):

        # Get the category to search for
        search_category = self.search_var.get()

        # Clear the listbox
        self.recipe_listbox.delete(0, tk.END)

        # Check if the search entry is not empty
        if search_category:
        # Fetch recipes from the database that are in the specified category
            self.cur.execute("""
                SELECT r.title
                FROM recipes r
                WHERE r.category = %s
                """, (search_category,))
            recipes = self.cur.fetchall()

        # Check if any recipes were found
        if recipes:
            for recipe in recipes:
                self.recipe_listbox.insert(tk.END, recipe[0])
        else:
            messagebox.showinfo("Search Results", "No recipes found in that category.")

        self.refresh_recipes()


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
       ingredients_input = simpledialog.askstring("Input", "What are the ingredients?")
       instructions = simpledialog.askstring("Input", "What are the instructions?")
       cooking_hardware = simpledialog.askstring("Input", "What are the cooking hardwares?")
       category = simpledialog.askstring("Input", "What is the category?")

    
       self.cur.execute("INSERT INTO recipes (title, cooking_time, ingredients, instructions, cooking_hardware, category) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
                       (title, cooking_time, ingredients_input, instructions, cooking_hardware, category))
       recipe_id = self.cur.fetchone()[0]  # Get the ID of the inserted recipe

           
           # Split ingredients string and insert into ingredients table
       for ingredient in ingredients_input.split(","):
            ingredient = ingredient.strip()  # Remove leading/trailing whitespace
               
               # Check if the ingredient already exists in the ingredients table
            self.cur.execute("SELECT id FROM ingredients WHERE name = %s", (ingredient,))
            existing_ingredient = self.cur.fetchone()
               
            if not existing_ingredient:
                # Insert the ingredient into the ingredients table
                self.cur.execute("INSERT INTO ingredients (name, recipe_id) VALUES (%s, %s)", (ingredient, recipe_id))
           
            self.conn.commit()

            # Refresh the list of recipes
            self.refresh_recipes()


    def show_recipe_details(self, event):
       # Get the selected recipe name
       selected_index = self.recipe_listbox.curselection()
       if not selected_index:
          return
       selected_recipe = self.recipe_listbox.get(selected_index)

       # Fetch the details of the selected recipe from the database
       self.cur.execute("""
       SELECT title, cooking_time, ingredients, instructions, cooking_hardware, category
       FROM recipes
       WHERE title = %s""", (selected_recipe,))
       recipe_details = self.cur.fetchone()

       # Display basic recipe details
       recipe_info = f"Title: {recipe_details[0]}\n\nCooking Time: {recipe_details[1]}\n\nIngredients: {recipe_details[2]}\n\nInstructions: {recipe_details[3]}\n\nCooking Hardware: {recipe_details[4]}\n\nCategory: {recipe_details[5]}"

       # Check for allergens in the ingredients
       allergen_warning = ""
       ingredients = recipe_details[2].split(',')
       for ingredient in ingredients:
           ingredient = ingredient.strip()
           self.cur.execute("SELECT allergens FROM ingredients WHERE name = %s", (ingredient,))
           result = self.cur.fetchone()
           if result and result[0]:
                allergen_warning += f"\n\nWarning: {ingredient} contains allergens {result[0]}"

       if allergen_warning:
           recipe_info += allergen_warning

       messagebox.showinfo("Recipe Details", recipe_info)

    def reset_sequence(self, table_name):
    # Find the minimum available ID that is not currently in use
        self.cur.execute(f"SELECT COALESCE((SELECT MIN(id) FROM generate_series(1, (SELECT MAX(id) FROM {table_name})) AS s LEFT JOIN {table_name} t ON s = t.id WHERE t.id IS NULL), 1)")
        next_id = self.cur.fetchone()[0]
    
    # Reset the sequence for the specified table
        self.cur.execute(f"SELECT setval(pg_get_serial_sequence('{table_name}', 'id'), {next_id}, false)")
        self.conn.commit()

    def delete_recipe(self):
        # Get the selected recipe name
        selected_recipe = self.recipe_listbox.get(self.recipe_listbox.curselection())

        # Confirm the deletion with the user
        confirmation = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the recipe '{selected_recipe}'?")

        if confirmation:
        # Get the ID of the recipe to be deleted
            self.cur.execute("SELECT id FROM recipes WHERE title = %s", (selected_recipe,))
            recipe_id = self.cur.fetchone()[0]

        # Delete the ingredients of the recipe from the ingredients table
            self.cur.execute("DELETE FROM ingredients WHERE recipe_id = %s", (recipe_id,))

        # Delete the recipe from the recipes table
            self.cur.execute("DELETE FROM recipes WHERE id = %s", (recipe_id,))
        
            self.conn.commit()

            self.reset_sequence("recipes")
            self.reset_sequence("ingredients")

            # Refresh the list of recipes
            self.refresh_recipes()

    def update_recipe(self):
        # Create a new window for updating the recipe
        update_window = tk.Toplevel(self.root)
        update_window.title("Update Recipe")

        # Create labels and entry fields for the recipe details
        title_label = tk.Label(update_window, text="Recipe Name:")
        title_label.grid(row=0, column=0, padx=10, pady=10)
        title_entry = tk.Entry(update_window)
        title_entry.grid(row=0, column=1, padx=10, pady=10)

        cooking_time_label = tk.Label(update_window, text="Cooking Time:")
        cooking_time_label.grid(row=1, column=0, padx=10, pady=10)
        cooking_time_entry = tk.Entry(update_window)
        cooking_time_entry.grid(row=1, column=1, padx=10, pady=10)

        ingredients_label = tk.Label(update_window, text="Ingredients:")
        ingredients_label.grid(row=2, column=0, padx=10, pady=10)
        ingredients_entry = tk.Entry(update_window)
        ingredients_entry.grid(row=2, column=1, padx=10, pady=10)

        instructions_label = tk.Label(update_window, text="Instructions:")
        instructions_label.grid(row=3, column=0, padx=10, pady=10)
        instructions_entry = tk.Entry(update_window)
        instructions_entry.grid(row=3, column=1, padx=10, pady=10)

        cooking_hardware_label = tk.Label(update_window, text="Cooking Hardware:")
        cooking_hardware_label.grid(row=4, column=0, padx=10, pady=10)
        cooking_hardware_entry = tk.Entry(update_window)
        cooking_hardware_entry.grid(row=4, column=1, padx=10, pady=10)

        category_label = tk.Label(update_window, text="Category:")
        category_label.grid(row=5, column=0, padx=10, pady=10)
        category_entry = tk.Entry(update_window)
        category_entry.grid(row=5, column=1, padx=10, pady=10)

        # Get the selected recipe name
        selected_recipe = self.recipe_listbox.get(self.recipe_listbox.curselection())

        # Fetch the details of the selected recipe from the database
        self.cur.execute("SELECT title, cooking_time, ingredients, instructions, cooking_hardware, category FROM recipes WHERE title = %s", (selected_recipe,))
        recipe_details = self.cur.fetchone()

        # Set the initial values of the entry fields to the current recipe details
        title_entry.insert(tk.END, recipe_details[0])
        cooking_time_entry.insert(tk.END, recipe_details[1])
        if recipe_details[2] is not None and isinstance(recipe_details[2], str):
            ingredients_entry.insert(tk.END, recipe_details[2])
        instructions_entry.insert(tk.END, recipe_details[3])
        cooking_hardware_entry.insert(tk.END, recipe_details[4])
        category_entry.insert(tk.END, recipe_details[5])

        def update_recipe_details():
            # Get the updated recipe details from the entry fields
            updated_title = title_entry.get()
            updated_cooking_time = cooking_time_entry.get()
            updated_ingredients = ingredients_entry.get()
            updated_instructions = instructions_entry.get()
            updated_cooking_hardware = cooking_hardware_entry.get()
            updated_category = category_entry.get()

            # Update the recipe in the database
            self.cur.execute("UPDATE recipes SET title = %s, cooking_time = %s, ingredients = %s, instructions = %s, cooking_hardware = %s , category = %s WHERE title = %s",
                             (updated_title, updated_cooking_time, updated_ingredients, updated_instructions, updated_cooking_hardware, updated_category, selected_recipe))
            self.conn.commit()


            self.cur.execute("SELECT id FROM recipes WHERE title = %s", (updated_title,))
            recipe_id = self.cur.fetchone()[0]

            # Split updated ingredients string and update ingredients table
            for ingredient in updated_ingredients.split(","):
                ingredient = ingredient.strip()  # Remove leading/trailing whitespace

            # Check if the ingredient already exists in the ingredients table
            self.cur.execute("SELECT id FROM ingredients WHERE name = %s AND recipe_id = %s", (ingredient, recipe_id))
            existing_ingredient = self.cur.fetchone()

            if not existing_ingredient:
                # Insert the ingredient into the ingredients table
                self.cur.execute("INSERT INTO ingredients (name, recipe_id) VALUES (%s, %s)", (ingredient, recipe_id))
            else:
                # Update the ingredient in the ingredients table
                self.cur.execute("UPDATE ingredients SET name = %s WHERE id = %s", (ingredient, existing_ingredient[0]))

            self.conn.commit()

            # Refresh the list of recipes
            self.refresh_recipes()

            # Close the update window
            update_window.destroy()

        # Create the update button
        update_button = tk.Button(update_window, text="Update", command=update_recipe_details)
        update_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    def add_allergen(self):
        # Create a new window for adding allergens
        allergen_window = tk.Toplevel(self.root)
        allergen_window.title("Add Allergen to Ingredient")

        # Create labels and entry fields for the allergen details
        ingredient_label = tk.Label(allergen_window, text="Ingredient:")
        ingredient_label.grid(row=0, column=0, padx=10, pady=10)
        ingredient_entry = tk.Entry(allergen_window)
        ingredient_entry.grid(row=0, column=1, padx=10, pady=10)

        allergen_label = tk.Label(allergen_window, text="Allergen:")
        allergen_label.grid(row=1, column=0, padx=10, pady=10)
        allergen_entry = tk.Entry(allergen_window)
        allergen_entry.grid(row=1, column=1, padx=10, pady=10)

        def add_allergen_to_ingredient():

            ingredient_name = ingredient_entry.get().strip()
            allergen_name = allergen_entry.get().strip()

            # Fetch the details of the selected ingredient from the database
            self.cur.execute("SELECT allergens FROM ingredients WHERE name = %s", (ingredient_name,))
            ingredient = self.cur.fetchone()

            if ingredient:
               # Append the new allergen information to the existing allergens
                existing_allergens = ingredient[0] or ''
                new_allergens = existing_allergens + (', ' if existing_allergens else '') + allergen_name
                self.cur.execute("UPDATE ingredients SET allergens = %s WHERE name = %s",
                            (new_allergens, ingredient_name))
                self.conn.commit()
                messagebox.showinfo("Success", f"Allergen '{allergen_name}' added successfully to the ingredient '{ingredient_name}'.")
            else:
                messagebox.showerror("Error", "The specified ingredient does not exist.")

        ok_button = tk.Button(allergen_window, text="OK", command=add_allergen_to_ingredient)
        ok_button.grid(row=2, column=0, padx=10, pady=10)

        cancel_button = tk.Button(allergen_window, text="Cancel", command=allergen_window.destroy)  
        cancel_button.grid(row=2, column=1, padx=10, pady=10)

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
