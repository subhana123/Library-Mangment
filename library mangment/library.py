import json  
import streamlit as st
import pandas as pd

# In-memory library (a list of books)
library = []

# Load library from file (if exists)
def load_library(filename='library.json'):
    global library
    try:
        with open(filename, 'r') as file:
            library = json.load(file)
    except FileNotFoundError:
        library = []

# Save library to file
def save_library(filename='library.json'):
    with open(filename, 'w') as file:
        json.dump(library, file, indent=4)

# Calculate Statistics
def calculate_statistics():
    total_books = len(library)
    if total_books == 0:
        return total_books, 0.0
    read_books = len([book for book in library if book['Read Status'] == 'Read'])
    percentage_read = (read_books / total_books) * 100
    return total_books, percentage_read

# Load the library
load_library()

# Apply Animated Background Styling
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(45deg, #6bff6b, #6bafff, #ff6b6b);
        background-size: 600% 600%;
        animation: gradientAnimation 10s ease infinite;
    }

    @keyframes gradientAnimation {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    .main {
        background-color: rgba(255, 255, 255, 0.8); 
        padding: 20px;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Main Container
st.markdown('<div class="main">', unsafe_allow_html=True)

# Streamlit UI
st.title("📚 Enhanced Personal Library Manager")

# Sidebar Menu
menu = ["Add Book", "View All Books", "Remove Book", "Search Books", "Edit Book", "Display Statistics", "Import/Export", "Exit"]
choice = st.sidebar.selectbox("Menu", menu)

# Add Book Section
if choice == "Add Book":
    st.subheader("Add a New Book")
    title = st.text_input("Title")
    author = st.text_input("Author")
    year = st.number_input("Publication Year", min_value=0, max_value=2100, value=2023)
    genre = st.text_input("Genre")
    read_status = st.selectbox("Read Status", ["Read", "Unread"])
    
    if st.button("Add Book"):
        if title and author:
            book = {
                'Title': title,
                'Author': author,
                'Year': year,
                'Genre': genre,
                'Read Status': read_status
            }
            library.append(book)
            save_library()
            st.success(f"Book '{title}' added successfully!")
        else:
            st.error("Title and Author are required!")

# View All Books Section
elif choice == "View All Books":
    st.subheader("All Books")
    if library:
        st.write(pd.DataFrame(library))
    else:
        st.info("No books in the library.")

# Remove Book Section
elif choice == "Remove Book":
    st.subheader("Remove a Book")
    
    if library:
        titles = [book['Title'] for book in library]
        title_to_remove = st.selectbox("Select a book to remove", titles)
        
        if st.button("Remove Book"):
            library = [book for book in library if book['Title'] != title_to_remove]
            save_library()
            st.success(f"Book '{title_to_remove}' removed successfully!")
    else:
        st.info("No books available to remove.")

# Edit Book Section
elif choice == "Edit Book":
    st.subheader("Edit a Book")
    
    if library:
        titles = [book['Title'] for book in library]
        title_to_edit = st.selectbox("Select a book to edit", titles)
        
        if title_to_edit:
            book = next(book for book in library if book['Title'] == title_to_edit)
            new_title = st.text_input("Title", value=book['Title'])
            new_author = st.text_input("Author", value=book['Author'])
            new_year = st.number_input("Publication Year", min_value=0, max_value=2100, value=int(book['Year']))
            new_genre = st.text_input("Genre", value=book['Genre'])
            new_status = st.selectbox("Read Status", ["Read", "Unread"], index=0 if book['Read Status'] == "Read" else 1)
            
            if st.button("Save Changes"):
                book.update({
                    'Title': new_title,
                    'Author': new_author,
                    'Year': new_year,
                    'Genre': new_genre,
                    'Read Status': new_status
                })
                save_library()
                st.success(f"Book '{new_title}' updated successfully!")
    else:
        st.info("No books to edit.")

# Search Books Section
elif choice == "Search Books":
    st.subheader("Search Books")
    
    search_query = st.text_input("Search by Title or Author:")
    
    if st.button("Search"):
        results = [book for book in library if search_query.lower() in book['Title'].lower() or search_query.lower() in book['Author'].lower()]
        
        if results:
            st.write(pd.DataFrame(results))
        else:
            st.warning("No matching books found.")

# Display Statistics Section
elif choice == "Display Statistics":
    st.subheader("Library Statistics")
    total_books, percentage_read = calculate_statistics()
    
    st.write(f"**Total books:** {total_books}")
    st.write(f"**Percentage read:** {percentage_read:.2f}%")

# Import/Export Library Section
elif choice == "Import/Export":
    st.subheader("Import/Export Library")
    
    uploaded_file = st.file_uploader("Upload a JSON file", type="json")
    if uploaded_file:
        library = json.load(uploaded_file)
        save_library()
        st.success("Library imported successfully!")
    
    if st.button("Export Library"):
        json_data = json.dumps(library, indent=4)
        st.download_button(label="Download Library", data=json_data, file_name="library.json", mime="application/json")

# Exit Option
elif choice == "Exit":
    save_library()
    st.success("Library saved to file. Goodbye! 👋")

# Close Main Container
st.markdown('</div>', unsafe_allow_html=True)
