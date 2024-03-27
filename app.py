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
            user="postgres",
            host="localhost"
        )
        self.cur = self.conn.cursor()
        
        # Create the GUI
        self.create_widgets()
    
    def create_widgets(self):
        self.root.grid_columnconfigure(0, weight=1) 
        self.root.grid_rowconfigure(0, weight=1)  

        self.recipe_listbox = tk.Listbox(self.root, width=50)
        self.recipe_listbox.grid(row=0, column=0, padx=10, pady=10, rowspan=4, sticky='nsew') 
        
        self.refresh_button = tk.Button(self.root, text="Refresh", command=self.refresh_recipes)
        self.refresh_button.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')  
        
        self.add_button = tk.Button(self.root, text="Add Recipe", command=self.add_recipe)
        self.add_button.grid(row=1, column=1, padx=10, pady=10, sticky='nsew') 
        
        self.delete_button = tk.Button(self.root, text="Delete Recipe", command=self.delete_recipe)
        self.delete_button.grid(row=2, column=1, padx=10, pady=10, sticky='nsew') 
        
        self.update_button = tk.Button(self.root, text="Update Recipe", command=self.update_recipe)
        self.update_button.grid(row=3, column=1, padx=10, pady=10, sticky='nsew') 
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
    
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
        pass
    
    def delete_recipe(self):
        # Implement deleting recipe functionality
        pass
    
    def update_recipe(self):
        # Implement updating recipe functionality
        pass
    
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
