import streamlit as st
import pickle
import pandas as pd

# Recommendation Function
def recommend_books(book_title):
    try:
        # Find the index of the selected book
        book_index = books[books['title'] == book_title].index[0]
        # Get the feature vector for the selected book
        book_features = feature_matrix[book_index].reshape(1, -1)
        # Find the 5 most similar books
        distances, indices = similarity.kneighbors(book_features, n_neighbors=6)
        
        # Retrieve the titles of the recommended books
        recommended_books = [books.iloc[idx].title for idx in indices[0] if idx != book_index]
        return recommended_books
    except IndexError:
        return ["No recommendations available. Please try another book."]
    except Exception as e:
        return [f"Error: {str(e)}"]

# Load Data
# Load book titles (list) and convert to DataFrame
with open('D:\\project\\Book_recommendation\\book_titles.pkl', 'rb') as f:
    book_titles = pickle.load(f)
books = pd.DataFrame(book_titles, columns=['title'])

# Load feature matrix (used for recommendations)
with open('D:\\project\\Book_recommendation\\feature_matrix.pkl', 'rb') as f:
    feature_matrix = pickle.load(f)

# Load similarity model (Nearest Neighbors)
with open('D:\\project\\Book_recommendation\\similarity_model.pkl', 'rb') as f:
    similarity = pickle.load(f)

# Streamlit Title and Header
st.set_page_config(page_title="📚 Book Recommendation System 📖", page_icon="📘")
st.markdown("""
    <style>
    .title {
        font-size: 40px;
        font-weight: bold;
        color: #8A2BE2;
        text-align: center;
    }
    .button {
        background-color: #8A2BE2;
        color: white;
        border-radius: 10px;
        font-size: 18px;
        padding: 12px 24px;
        border: none;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        transition: background-color 0.3s ease;
    }
    .button:hover {
        background-color: #6A1B9A;
    }
    .recommender {
        text-align: center;
        margin-top: 30px;
    }
    .book-title {
        font-size: 16px;
        font-weight: bold;
        color: #4CAF50;
        text-align: center;
    }
    .footer {
        text-align: center;
        font-size: 14px;
        color: #888;
        margin-top: 50px;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar for book selection with emoji
st.sidebar.header("📚 **Select Your Favorite Book!**")
selected_book_name = st.sidebar.selectbox('📖 Choose a book you enjoyed', books['title'].values)

# Recommendation Button with emoji
if st.sidebar.button('🔍 **Recommend Similar Books** 🔍', key='recommend_button'):
    recommended_books = recommend_books(selected_book_name)

    # Displaying the recommendation section with emojis and styling
    st.markdown("<h2 style='color:#8A2BE2;'>📘 Discover Your Next Read 📚</h2>", unsafe_allow_html=True)
    st.write("✨ Here's a curated list of books you might love! ✨")

    # Display recommendations on different lines, each with an emoji
    for book in recommended_books:
        st.markdown(f"📖 **{book}** 📚")
        st.write("---")
