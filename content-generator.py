import openai
import requests
import random
import os
from article_prompts import article_prompts

# Set up OpenAI API credentials
openai.api_key = os.environ["OPENAI_API_KEY"]

# Set up WordPress credentials
wordpress_url = os.environ["WORDPRESS_URL"]
wordpress_username = os.environ["WORDPRESS_USERNAME"]
wordpress_password = os.environ["WORDPRESS_PASSWORD"]

# Function to generate an article prompt using ChatGPT
def generate_article_prompt(prompt):
    try:
        response = openai.Completion.create(
            engine='gpt-3.5-turbo-instruct', # Specifies the GPT model to use
            prompt=prompt, # The prompt to generate content from
            max_tokens=1200, # Maximum length of the generated content
            n=1,# Number of completions to generate
            stop=None, # Token(s) that signify the end of a completion
            temperature=0.7 # Creativity of the response; lower values are more deterministic
        )
        return response.choices[0].text.strip() # Returns the generated text, stripped of leading/trailing whitespace
    except Exception as e:
        print(f"Error generating article: {str(e)}")
        return None


# Function to create a new WordPress post
def create_wordpress_post(content):
    try:

        content_json = json.loads(content) # Loads the article content into a JSON object
        
        endpoint = f"{wordpress_url}/wp-json/wp/v2/posts" # WordPress API endpoint for creating new posts

        
        headers = {
            'Content-Type': 'application/json' # Set headers for the request
        }

        # Payload
        data = {                              
            'title': content_json["title"],
            'content': content_json["content"],
            'status': 'publish'
        }

        # Set authentication credentials
        auth = (wordpress_username, wordpress_password)

        # Send the POST request to create the post
        response = requests.post(endpoint, headers=headers, json=data, auth=auth)

        # Check the response status code and return the post ID if successful
        if response.status_code == 201:
            return response.json()['id']
        else:
            print("Failed to create a new post.")
            return None
    except Exception as e:
        print(f"Error creating WordPress post: {str(e)}")
        print(response.text)
        return None

# Main script
def main():
    prompt = random.choice(article_prompts)

    # Generate the article using ChatGPT
    article = generate_article_prompt(prompt)

    print(article)
    
    if article:

        # Create the WordPress post
        post_id = create_wordpress_post(article)

        # Check if the post was created successfully
        if post_id:
            print(f"Successfully created a new post with ID: {post_id}")
        else:
            print("Failed to create a new post.")
    else:
        print("Failed to generate the article.")

# Ensures that the main function runs only if the script is executed directly, not when imported
if __name__ == '__main__':
    main()
