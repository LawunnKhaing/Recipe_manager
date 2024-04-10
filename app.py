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
            password="007",
            host="localhost"
        )
        self.cur = self.conn.cursor()

        # Create the GUI
        self.create_widgets()

        # Refresh the list of recipes
        self.refresh_recipes()
    
    def create_widgets(self):
        self.root.grid_columnconfigure(0, weight=1) 
        self.root.grid_rowconfigure(0, weight=1)
        self.root.resizable(True, True)

        self.recipe_listbox = tk.Listbox(self.root, width=50)
        self.recipe_listbox.grid(row=0, column=0, padx=10, pady=10, rowspan=4, sticky='nsew') 

        self.recipe_listbox.bind('<<ListboxSelect>>', self.show_recipe_details)
        
        self.refresh_button = tk.Button(self.root, text="Refresh", command=self.refresh_recipes)
        self.refresh_button.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')  
        
        self.add_button = tk.Button(self.root, text="Add Recipe", command=self.add_recipe)
        self.add_button.grid(row=1, column=1, padx=10, pady=10, sticky='nsew') 
        
        self.delete_button = tk.Button(self.root, text="Delete Recipe", command=self.delete_selected_recipe)
        self.delete_button.grid(row=2, column=1, padx=10, pady=10, sticky='nsew') 
        
        self.update_button = tk.Button(self.root, text="Update Recipe", command=self.update_selected_recipe)
        self.update_button.grid(row=3, column=1, padx=10, pady=10, sticky='nsew') 
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.refresh_recipes()
    
    def refresh_recipes(self):
        # Clear the listbox
        self.recipe_listbox.delete(0, tk.END)
        
        # Fetch recipes from the database
        self.cur.execute("SELECT id, title FROM recipes")
        recipes = self.cur.fetchall()
        for recipe in recipes:
            self.recipe_listbox.insert(tk.END, (recipe[0], recipe[1]))

    def add_recipe(self):
        title = simpledialog.askstring("Input", "What is the recipe name?")
        cooking_time = simpledialog.askstring("Input", "What is the cooking time?")
        instructions = simpledialog.askstring("Input", "What are the cooking hardwares?")
        cooking_hardware = simpledialog.askstring("Input", "What are the instructions?")

        # Check if the user has entered all the details
        if title and cooking_time and instructions and cooking_hardware:
            # Insert the new recipe into the database
            self.cur.execute("INSERT INTO recipes (title, cooking_time, instructions, cooking_hardware) VALUES (%s, %s, %s, %s)",
                             (title, cooking_time, instructions, cooking_hardware))
            self.conn.commit()

            # Refresh the list of recipes
            self.refresh_recipes()
        else:
            messagebox.showerror("Error", "You must enter all the details for the recipe")

    def delete_selected_recipe(self):
        # Get the selected index from the listbox
        selected_index = self.recipe_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "You must select a recipe to delete")
            return

<<<<<<< HEAD
        # Get the recipe ID of the selected recipe
        recipe_id, recipe_title = self.recipe_listbox.get(selected_index)[0], self.recipe_listbox.get(selected_index)[1]

        # Confirm deletion with user
        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the recipe '{recipe_title}'?")
        if not confirm:
            return

        try:
            # Execute the DELETE command
            self.cur.execute("DELETE FROM recipes WHERE id = %s", (recipe_id,))
            self.conn.commit()
            
            # Refresh the list of recipes
            self.refresh_recipes()

            messagebox.showinfo("Success", f"Recipe '{recipe_title}' deleted successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete recipe: {str(e)}")
    
    def update_selected_recipe(self):
        # Get the selected index from the listbox
        selected_index = self.recipe_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "You must select a recipe to update")
            return

        # Get the recipe ID and title of the selected recipe
        recipe_id, recipe_title = self.recipe_listbox.get(selected_index)[0], self.recipe_listbox.get(selected_index)[1]

        # Get new details from user
        new_title = simpledialog.askstring("Input", f"Enter new title")
        new_cooking_time = simpledialog.askstring("Input", f"Enter new cooking time")
        new_instructions = simpledialog.askstring("Input", f"Enter new instructions")
        new_cooking_hardware = simpledialog.askstring("Input", f"Enter new cooking hardware")

        try:
            # Execute the UPDATE command
            self.cur.execute("UPDATE recipes SET title = %s, cooking_time = %s, instructions = %s, cooking_hardware = %s WHERE id = %s", 
                             (new_title, new_cooking_time, new_instructions, new_cooking_hardware, recipe_id))
            self.conn.commit()

            # Refresh the list of recipes
            self.refresh_recipes()

            messagebox.showinfo("Success", f"Recipe '{recipe_title}' updated successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update recipe: {str(e)}")
=======
    def show_recipe_details(self, event):
        # Get the selected recipe name
        selected_recipe = self.recipe_listbox.get(self.recipe_listbox.curselection())

        # Fetch the details of the selected recipe from the database
        self.cur.execute("SELECT title, cooking_time, instructions, cooking_hardware FROM recipes WHERE title = %s", (selected_recipe,))
        recipe_details = self.cur.fetchone()

        messagebox.showinfo("Recipe Details", f"Title: {recipe_details[0]}\nCooking Time: {recipe_details[1]}\nInstructions: {recipe_details[2]}\nCooking Hardware: {recipe_details[3]}")
        
    def delete_recipe(self):
        # Implement deleting recipe functionality
        pass
    
    def update_recipe(self):
        # Implement updating recipe functionality
        pass
>>>>>>> 56e9918 (Add view)
    
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
