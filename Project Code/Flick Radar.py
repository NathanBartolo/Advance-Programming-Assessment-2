import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import requests

# Setup to fetch TMDB API key
API_KEY = "645f2c3f53c05e6e7dc711d040bce20b"  # Api Key
BASE_URL = "https://api.themoviedb.org/3/"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w200"  # Base URL for posters

# Created this function to fetch movies based on specific categories
def fetchMovies(category="popular", year=None, language="en-US"):
    url = f"{BASE_URL}movie/{category}"
    params = {"api_key": API_KEY, "language": language}#Parameters
    if year:#Year filter
        params["primary_release_year"] = year  # Filter by release year
    response = requests.get(url, params=params)#Requesting API

    if response.status_code == 200:#If successful respomse return the list of movies
        data = response.json()
        return data.get("results", [])
    else:#if not this will handle errors saying that the API request failed
        messagebox.showerror("Error", f"API request failed with status code {response.status_code}")
        return []

# Created to search movies by filters
def searchWithFilters():
    movie_name = entry1.get() #Get movie from movie name
    release_year = year_filter.get()  # Search movie by date released
    language = language_filter.get()  # Search movie by language

    if not movie_name:#if no input showwarning
        messagebox.showwarning("Input Required", "Please enter a movie name!")
        return
    #call API and parameters to search
    url = f"{BASE_URL}search/movie"
    params = {"api_key": API_KEY, "query": movie_name, "language": language}
    if release_year != "Any":  # If a year is selected add it to the search parameters
        params["primary_release_year"] = release_year
    #Request API
    response = requests.get(url, params=params)

    if response.status_code == 200:#if successful
        data = response.json()
        movies = data.get("results", [])#Return Result
        if movies:
            clear_results()
            result_label.config(text=f"Results for '{movie_name}':")
            for idx, movie in enumerate(movies[:4]):  # Limit to 4 results in a row
                movieCard(movie, idx)
        else: #Display no movies found
            result_label.config(text="No movies found!")
    else:#Handle API errors
        messagebox.showerror("Error", f"API request failed with status code {response.status_code}")

#dropdowns function for filters
def addFilters():
    filter_frame = ttk.Frame(root)#Created frames to hold dropdown widgets
    filter_frame.pack(pady=10)

    # Release Year Filter
    year_label = ttk.Label(filter_frame, text="Release Year:")
    year_label.pack(side=tk.LEFT, padx=10)
    years = [str(year) for year in range(2025, 2005, -1)] + ["Any"]  # Years 2025 to 2005
    global year_filter#Called global
    year_filter = ttk.Combobox(filter_frame, values=years, width=10)#position the dropdown
    year_filter.set("Any")  # Default option
    year_filter.pack(side=tk.LEFT, padx=10)

    # Language Filter
    language_label = ttk.Label(filter_frame, text="Language:")
    language_label.pack(side=tk.LEFT, padx=10)
    languages = ["en-US", "es-ES", "fr-FR", "de-DE", "it-IT", "ja-JP", "ko-KR", "pt-BR", "zh-CN"]  # Common languages
    global language_filter #Called global
    language_filter = ttk.Combobox(filter_frame, values=languages, width=10)#positioned the dropdown
    language_filter.set("en-US")  # Default option
    language_filter.pack(side=tk.LEFT, padx=10)

    # Search Button with filters
    filter_button = ttk.Button(filter_frame, text="Search with Filters", command=searchWithFilters,)
    filter_button.pack(side=tk.LEFT, padx=10,)



# Function to display movies on home page
def featureMovies():
    movies = fetchMovies("popular")  # Fetch popular movies from the first function
    if movies:
        clear_results()#return if success
        result_label.config(text="Featured Movies:")
        for idx, movie in enumerate(movies[:4]):  # I limit to 4 results in the middle
            movieCard(movie, idx)

#display upcoming movies
def upcomingMovies():
    movies = fetchMovies("upcoming")  # Fetch upcoming movies
    if movies:
        clear_results()
        result_label.config(text="Upcoming Movies:")
        for idx, movie in enumerate(movies[:4]):  # I limit to 4 results in the middle
            movieCard(movie, idx)

# Created a function to generate random movies
def generate_random_movies():
    movies = fetchMovies("popular")  # Fetch popular movies
    if movies:
        clear_results()
        result_label.config(text="Randomly Generated Movies:")
        for idx, movie in enumerate(movies[:4]):  # Limit to 4 results in the middle
            movieCard(movie, idx)

# Function to search for movies by name
def searchMovies():
    movie_name = entry1.get()#get from entry search bar
    if not movie_name:#if error display input required
        messagebox.showwarning("Input Required", "Please enter a movie name!")
        return
    #Called API URL 
    url = f"{BASE_URL}search/movie"
    params = {"api_key": API_KEY, "query": movie_name}
    response = requests.get(url, params=params)#Request API Link

    if response.status_code == 200:#If Successful pring result
        data = response.json()
        movies = data.get("results", [])
        if movies:
            clear_results()
            result_label.config(text=f"Results for '{movie_name}':")
            for idx, movie in enumerate(movies[:4]):  # Limit to 4 results in the middle
                movieCard(movie, idx)
        else:
            result_label.config(text="No movies found!")
    else:
        messagebox.showerror("Error", f"API request failed with status code {response.status_code}")

# Function to clear results
def clear_results():
    for widget in results_frame.winfo_children():#Destroy the page
        widget.destroy()
#Function for the movie card to be displayed in home page
def movieCard(movie, idx):
    # Create a frame for each movie
    movie_frame = ttk.Frame(results_frame, padding=10)
    
    # Add the frame to the grid
    row = 4  # Only 1 row to center the movies in the middle
    col = idx  # Place movies in the 4 columns
    movie_frame.grid(row=row, column=col, padx=5, pady=5)

    # Fetch poster image
    poster_path = movie.get("poster_path")
    if poster_path:
        poster_url = f"{IMAGE_BASE_URL}{poster_path}"
        poster_image = fetchImage(poster_url)
        if poster_image:
            poster_label = tk.Label(movie_frame, image=poster_image)
            poster_label.image = poster_image  # Keep a reference to avoid garbage collection
            poster_label.pack()

    # Add movie title
    title = movie.get("title", "Unknown Title")
    title_label = ttk.Label(movie_frame, text=title, wraplength=150, justify="center", font=("Helvetica", 10, "bold"))
    title_label.pack(pady=5)

    # Add movie rating (if available)
    rating = movie.get("vote_average", "N/A")  # Fetch the movie rating
    rating_label = ttk.Label(movie_frame, text=f"Rating: {rating}/10", font=("Helvetica", 9, "italic"))
    rating_label.pack(pady=5)  # Rating aligned below the title

    # Add a button to view details
    details_button = ttk.Button(movie_frame, text="View Details", command=lambda: show_movie_details(movie))
    details_button.pack()

    #function to get cast info
def fetchCast(movie_id):
    cast_url = f"{BASE_URL}/movie/{movie_id}/credits?api_key={API_KEY}"#Called API URL link
    response = requests.get(cast_url)
    if response.status_code == 200:# if successful, return result
        cast_data = response.json().get("cast", [])
        return cast_data
    else:
        return []
#Function to display details of the movie
def show_movie_details(movie):
    # Print the full movie data to check
    print(movie)

    # Get the movie_id from the movie data
    movie_id = movie.get("id")

    # get cast data from the movie's credits 
    cast_data = fetchCast(movie_id)

    # Create a new top-level window (pop-up) for the info to be shown
    detail_window = tk.Toplevel(root)
    detail_window.title(movie["title"])
    detail_window.geometry("500x350")  
    detail_window.resizable(0, 0)

    # Frame for movie details
    detail_frame = ttk.Frame(detail_window, padding=10)
    detail_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Movie Poster and Text Section
    text_frame = ttk.Frame(detail_frame)  # Frame for the title, description, and actors
    text_frame.pack(side=tk.LEFT, padx=10, pady=10)

    poster_path = movie.get("poster_path")
    if poster_path:
        poster_url = f"{IMAGE_BASE_URL}{poster_path}"
        poster_image = fetchImage(poster_url)
        if poster_image:
            poster_label = tk.Label(detail_frame, image=poster_image)
            poster_label.image = poster_image  # Keep a reference to avoid garbage collection
            poster_label.pack(side=tk.LEFT, padx=10, pady=10)  # Pack the poster to the left

    # Movie Title and Description
    title = movie.get("title", "Unknown Title")
    description = movie.get("overview", "No description available.")#Get description
    release_date = movie.get("release_date", "Release date not available.")  # Get the release date

    title_label = ttk.Label(text_frame, text=title, font=("Helvetica", 16,"bold"))
    title_label.pack(anchor="w", padx=10, pady=5)  # Title aligned to the left

    description_label = ttk.Label(text_frame, text=description, wraplength=400, justify="left", font=("Helvetica", 12))
    description_label.pack(anchor="w", padx=10, pady=10)  # Description aligned to the left

    # Release Date (if available)
    release_date_label = ttk.Label(text_frame, text=f"Release Date: {release_date}", font=("Helvetica", 10))
    release_date_label.pack(anchor="w", padx=10, pady=5)  # Release date aligned to the left

    # Actor Names (if available)
    if cast_data:
        actor_names = ", ".join([actor.get("name", "Unknown Actor") for actor in cast_data[:5]])  # Limit to first 5 actors
        actor_label = ttk.Label(text_frame, text=f"Cast: {actor_names}", font=("Helvetica", 10))
        actor_label.pack(anchor="w", padx=10, pady=5)  # Actor names aligned to the left
    else:
        # If no cast data is available, show a message
        actor_label = ttk.Label(text_frame, text="Cast information not available.", font=("Helvetica", 10))
        actor_label.pack(anchor="w", padx=10, pady=5)


# Function to fetch an image from a URL in the DB
def fetchImage(url):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            img_data = response.raw
            image = Image.open(img_data)
            image = image.resize((150, 225))  # Resize poster to fit the card
            return ImageTk.PhotoImage(image)
        else:
            return None
    except Exception as e:
        print(f"Error fetching image: {e}")
        return None

# Function to show the actor search page
def show_actor_search_page():
    # Clear the current results frame
    clear_results()

    # Add the search bar and button for actors
    actor_search_label = ttk.Label(results_frame, text="Search for Actors", font=("Helvetica", 14,"bold"))
    actor_search_label.grid(row=0, column=0, columnspan=4, pady=10)

    actor_search_entry = ttk.Entry(results_frame, width=40, font=("Arial", 12))
    actor_search_entry.grid(row=1, column=0, columnspan=3, padx=5, pady=5)
    actor_search_entry.bind("<Return>", lambda event: searchMovies())



    actor_search_button = ttk.Button(results_frame, text="Search Actors", command=lambda: search_actors(actor_search_entry.get()))
    actor_search_button.grid(row=1, column=3, padx=5, pady=5)

#Function to show actors image card
def add_actor_card(actor, idx):
    # Create a frame for each actor
    actor_frame = ttk.Frame(results_frame, padding=10)
    
    #Created column and row to align cards
    row = idx // 4  # Two cards per row
    col = idx % 2  # First column (0) and second column (1)
    
  
    actor_frame.grid(row=row, column=col, padx=5, pady=5)

    # Actor's name
    actor_name = actor.get("name", "Unknown Actor")
    actor_name_label = ttk.Label(actor_frame, text=actor_name, font=("Helvetica", 12, "bold"))
    actor_name_label.pack(pady=5)

    # Actor's profile picture
    profile_path = actor.get("profile_path")
    if profile_path:
        profile_url = f"{IMAGE_BASE_URL}{profile_path}"
        profile_image = fetchImage(profile_url)
        if profile_image:
            profile_label = tk.Label(actor_frame, image=profile_image)
            profile_label.image = profile_image  # Keep a reference to avoid garbage collection
            profile_label.pack()
        else:
            # In case the image is not found, show a default "no image" label or placeholdere", font=("Arial", 10))
            placeholder_label.pack()
    else:
        # No profile picture available, show placeholder
        placeholder_label = ttk.Label(actor_frame, text="No Image Available", font=("Arial", 10))
        placeholder_label.pack()

# Created a function to clear results
def clear_results():
    for widget in results_frame.winfo_children():
        widget.destroy()
    canvas.config(scrollregion=canvas.bbox("all")) 

# Function to search for actors
def search_actors(actor_name):
    if not actor_name:
        messagebox.showwarning("Input Required", "Please enter an actor name!")
        return

    url = f"{BASE_URL}search/person"
    params = {"api_key": API_KEY, "query": actor_name}
    response = requests.get(url, params=params)#Request for API Link

    if response.status_code == 200:#If successful print result
        data = response.json()
        actors = data.get("results", [])
        if actors:
            clear_results()
            result_label.config(text=f"Results for '{actor_name}':")
            for idx, actor in enumerate(actors[:4]):  # I limit it to 4 actors
                add_actor_card(actor, idx)
        else:#show this if no actors dound
            result_label.config(text="No actors found!")
    else:
        messagebox.showerror("Error", f"API request failed with status code {response.status_code}")


# GUI Setup
root = tk.Tk()
root.title("Flick Radar")
root.geometry("800x700")
root.configure(bg="#f4f4f4")#Clean tone color
#Made it resizable for the so the layount wont change
root.resizable(0,0)

#Called a placeholder for the styling of the GUI
style = ttk.Style()
#Style for the frame
style.configure("TFrame", background="#f4f4f4")
#Style for the labels
style.configure("TLabel", background="#f4f4f4", foreground="black", font=("Helvetica", 12, 'bold',))
#Style for the buttons
style.configure("TButton", background="#f4f4f4", foreground="black",relief= "groove", font=("Helvetica", 12), padding=6, bd= 20)
#Style for the entries
style.configure("TEntry", background="#f4f4f4", foreground="black", font=("Arial", 12), padding=6)
#Style for the box
style.configure("TCombobox", background="#f4f4f4", foreground="black", font=("Helvetica", 12))

addFilters()#Called the dropdown filter here

# Title Label
title_label = ttk.Label(root, text="Flick Radar",font=("Helvetica", 18, 'bold'), style="TLabel")
title_label.pack(pady=10)

# Search Bar
entry_frame = ttk.Frame(root, style="TFrame")
entry_frame.pack(pady=10)
entry1 = ttk.Entry(entry_frame, width=40, style="TEntry")
entry1.pack(side=tk.LEFT, padx=5)
entry1.bind("<Return>", lambda event: searchMovies())

search_button = ttk.Button(entry_frame, text="Search", command=searchMovies, style="TButton")
search_button.pack(side=tk.LEFT)

# Buttons 
button_frame = ttk.Frame(root, style="TFrame")
button_frame.pack(pady=10)
upcoming_button = ttk.Button(button_frame, text="Upcoming Movies", command=upcomingMovies, style="TButton")
upcoming_button.pack(side=tk.LEFT, padx=10)
generate_button = ttk.Button(button_frame, text="Generate Movies", command=generate_random_movies, style="TButton")
generate_button.pack(side=tk.LEFT, padx=10)
search_actors_button = ttk.Button(button_frame, text="Search Actors", command=show_actor_search_page, style="TButton")
search_actors_button.pack(side=tk.LEFT, padx=10)

# Results Label
result_label = ttk.Label(root, text="Search results will appear here.", style="TLabel")
result_label.pack(pady=10)

# Canvas for results
canvas = tk.Canvas(root, bg="#f4f4f4")
scrollbar = ttk.Scrollbar(root,)
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side=tk.RIGHT, fill="y")
canvas.pack(fill=tk.BOTH, expand=True)

# Frame to hold the results
results_frame = ttk.Frame(canvas, style="TFrame")
canvas.create_window((0, 0), window=results_frame, anchor="nw")

# Update the scrolling region after adding widgets
results_frame.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))


# Display featured movies on startup
featureMovies()

#close the root to run application
root.mainloop()