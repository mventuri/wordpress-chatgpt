import openai
import requests
import random
from post_titles import blog_post_titles
from post_images import blog_post_images
from article_prompts import article_prompts

# Set up OpenAI API credentials
openai.api_key = ''

# Set up WordPress credentials
wordpress_url = ''
wordpress_username = ''
wordpress_password = ''


# ChatGPT API call
def generate_article_prompt(prompt):
    try:
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=prompt,
            max_tokens=200,
            n=1,
            stop=None,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error generating article: {str(e)}")
        return None

# Create a new WordPress post
def create_wordpress_post(title, content, image):
    try:
        # WordPress API endpoint for creating new posts
        endpoint = f"{wordpress_url}/wp-json/wp/v2/posts"

        # Set headers for the request
        headers = {
            'Content-Type': 'application/json'
        }

        # Set data for the new post
        data = {
            'title': title,
            'content': content,
            'status': 'publish',
            'featured_media': image
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
        return None

# Main script
def main():
    prompt = random.choice(article_prompts)
    
    # Generate the article using ChatGPT
    article = generate_article_prompt(prompt)
    
    article_title = random.choice(blog_post_titles)
    article_image = random.choice(blog_post_images)

    if article:

        # Create the WordPress post
        post_id = create_wordpress_post(article_title, article, article_image)

        # Check if the post was created successfully
        if post_id:
            print(f"Successfully created a new post with ID: {post_id}")
        else:
            print("Failed to create a new post.")
    else:
        print("Failed to generate the article.")

if __name__ == '__main__':
    main()
