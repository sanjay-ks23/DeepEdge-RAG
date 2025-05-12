import os
import requests
from bs4 import BeautifulSoup
import re
from openai import OpenAI
from dotenv import load_dotenv

# Load API keys from environment variables
load_dotenv()
SERPER_API_KEY = os.getenv('SERPER_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

def search_articles(query):
    """
    Searches for articles related to the query using Serper API.
    Returns a list of dictionaries containing article URLs, headings, and text.
    """
    # Endpoint for Serper API
    url = "https://google.serper.dev/search"
    
    # Headers for the API request
    headers = {
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
    }
    
    # Request payload
    payload = {
        'q': query,
        'gl': 'us',
        'hl': 'en',
        'num': 5  # Number of results to return
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        # Parse the JSON response
        data = response.json()
        
        # Extract organic search results
        articles = data.get('organic', [])
        
        return articles
    except Exception as e:
        print(f"Error searching articles: {e}")
        return []

def fetch_article_content(url):
    """
    Fetches the article content, extracting headings and text.
    """
    try:
        # Add http:// if not present
        if not url.startswith('http'):
            url = 'https://' + url
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(['script', 'style', 'footer', 'nav', 'aside']):
            script.extract()
        
        # Extract headings (h1, h2, h3)
        headings = soup.find_all(['h1', 'h2', 'h3'])
        heading_text = [heading.get_text().strip() for heading in headings]
        
        # Extract paragraphs
        paragraphs = soup.find_all('p')
        paragraph_text = [p.get_text().strip() for p in paragraphs if p.get_text().strip()]
        
        # Combine headings and paragraphs
        content = "\n\n".join(heading_text + paragraph_text)
        
        # Remove excessive whitespace and normalize text
        content = re.sub(r'\s+', ' ', content).strip()
        
        return content
    except Exception as e:
        print(f"Error fetching article content from {url}: {e}")
        return ""

def concatenate_content(articles):
    """
    Concatenates the content of the provided articles into a single string.
    """
    full_text = ""
    
    for i, article in enumerate(articles, 1):
        title = article.get('title', f"Article {i}")
        content = article.get('content', "")
        
        # Format the article with a title and content
        article_text = f"ARTICLE {i}: {title}\n\n{content}\n\n"
        full_text += article_text
    
    # Limit content to avoid token overuse
    max_chars = 16000 # Adjust as needed
    if len(full_text) > max_chars:
        full_text = full_text[:max_chars] + "...[content truncated due to length]"
    
    return full_text.strip()

def generate_answer(content, query, conversation_history=None):
    """
    Generates an answer from the concatenated content using GPT models.
    The content, user's query, and conversation history are used to generate a contextual answer.
    """
    # Create the base system prompt instructing the model how to respond
    system_prompt = """You are a helpful assistant that answers questions based on the provided content. 
    Use only the information from the content to answer the question. 
    If the information is not in the content, admit that you don't know rather than making up an answer.
    Keep your answers accurate, helpful, and concise."""
    
    # Format the conversation history for inclusion in the prompt
    history_text = ""
    if conversation_history and len(conversation_history) > 0:
        history_segments = []
        for message in conversation_history[:-1]:  # Exclude the current query
            role = "User" if message["role"] == "user" else "Assistant"
            history_segments.append(f"{role}: {message['content']}")
        
        if history_segments:
            history_text = "Previous conversation:\n" + "\n".join(history_segments) + "\n\n"
    
    # Create the prompt with history, content, and current query
    full_prompt = f"{history_text}CONTENT:\n{content}\n\nCURRENT QUESTION: {query}\n\nAnswer:"
    
    try:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": full_prompt}
        ]

        try:
            # Attempt to use the GPT-4o model first
            # Note: Adjust model type as per your OpenAI account's access 
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.5,
                max_tokens=1000,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            # Extract the content from the response
            answer = response.choices[0].message.content.strip()
        except Exception as model_error:
            print(f"Error with GPT-4o model: {model_error}")
            # Fallback to GPT-3.5 if GPT-4o fails
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.5,
                max_tokens=1000,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            answer = response.choices[0].message.content.strip()
        
        return answer
    except Exception as e:
        print(f"Error generating answer: {e}")
        return "I'm sorry, but I encountered an error while generating your answer. Please try again."