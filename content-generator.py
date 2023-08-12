import openai
import requests

# Set up OpenAI API credentials
openai.api_key = '<OPENAI_API_KEY>'

# Set up WordPress credentials
wordpress_url = '<WORDPRESS_URL>'
wordpress_username = '<WORDPRESS_USERNAME>'
wordpress_password = '<WORDPRESS_APPLICATION_KEY>'

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
def create_wordpress_post(title, content):
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
            'featured_media': '1576'
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
    # Prompt for generating the article. Taken from this webpage: https://www.learnprompt.org/chat-gpt-prompts-for-blog-posts-writing/
    prompt = "I want you to act as a blogger and write a blog post about wristwatch, with a friendly and approachable tone that engages readers. Your target audience is individuals who are interested in buying wristwatch or they're just fans. Write in a personal style using singular first-person pronouns only. Please include the keywords 'wristwatch', 'wristwatch for men', and 'wristwatch for women' throughout the article. Format your response using markdown. Use headings, subheadings, bullet points, and bold to organize the information. Be sure the post ends with a full sentence followed by a period. post's minimum length must be 500 words. Maximum 800."
    prompt_title = "I want you to act as a blogger and write the tile of a blog post about wristwatch, with a friendly and approachable tone that engages readers. Length must be between 5 and 8 words."
    
    # Generate the article using ChatGPT
    article = generate_article_prompt(prompt)
    article_title = generate_article_prompt(prompt_title)

    if article:
        # Title for the new WordPress post
        #post_title = article_title

        # Create the WordPress post
        post_id = create_wordpress_post(article_title, article)

        # Check if the post was created successfully
        if post_id:
            print(f"Successfully created a new post with ID: {post_id}")
        else:
            print("Failed to create a new post.")
    else:
        print("Failed to generate the article.")

if __name__ == '__main__':
    main()
