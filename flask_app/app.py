from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from utils import search_articles, fetch_article_content, concatenate_content, generate_answer

# Load environment variables from .env file
load_dotenv()

# Make sure OPENAI_API_KEY is set in your environment
if not os.getenv('OPENAI_API_KEY'):
    print("Warning: OPENAI_API_KEY environment variable is not set")

app = Flask(__name__)

# Initialize conversation memory
conversation_history = []

@app.route('/query', methods=['POST'])
def query():
    """
    Handles the POST request to '/query'. Extracts the query from the request,
    processes it through the search, concatenate, and generate functions,
    and returns the generated answer.
    """
    # get the data/query from streamlit app
    data = request.json
    query = data.get('query', '')
    print("Received query: ", query)
    
    # Step 1: Search and scrape articles based on the query
    print("Step 1: searching articles")
    articles = search_articles(query)
    
    if not articles:
        return jsonify({'answer': "Sorry, I couldn't find any relevant articles for your query."})
    
    article_contents = []
    for article in articles[:5]:  # Limit to top 5 articles to avoid overloading
        url = article.get('link')
        if url:
            content = fetch_article_content(url)
            if content:
                article_contents.append({
                    'title': article.get('title', ''),
                    'content': content
                })
    
    # Step 2: Concatenate content from the scraped articles
    print("Step 2: concatenating content")
    concatenated_content = concatenate_content(article_contents)
    
    # Step 3: Generate an answer using the LLM with conversation history
    print("Step 3: generating answer")
    
    # Add current query to conversation history
    conversation_history.append({"role": "user", "content": query})
    
    # Generate answer considering conversation history
    answer = generate_answer(concatenated_content, query, conversation_history)
    
    # Add answer to conversation history
    conversation_history.append({"role": "assistant", "content": answer})
    
    # Keep only the last 10 exchanges to avoid token limits
    if len(conversation_history) > 20:
        conversation_history.pop(0)
        conversation_history.pop(0)
    
    # return the jsonified text back to streamlit
    return jsonify({'answer': answer})

@app.route('/reset', methods=['POST'])
def reset_conversation():
    """Reset the conversation history"""
    global conversation_history
    conversation_history = []
    return jsonify({'status': 'Conversation history cleared'})

if __name__ == '__main__':
    app.run(host='localhost', port=5000) #Note: Change port number accordingly, if system has 5000 port already in use we will get a 404 error