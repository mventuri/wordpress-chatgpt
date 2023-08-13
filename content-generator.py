import openai
import requests
import random

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
    # Prompt for generating the article. Taken from this webpage: https://www.learnprompt.org/chat-gpt-prompts-for-blog-posts-writing/
    # prompt = "I want you to act as a blogger and write a blog post about wristwatch, with a friendly and approachable tone that engages readers. Your target audience is individuals who are interested in buying wristwatch or they're just fans. Write in a personal style using singular first-person pronouns only. Please include the keywords 'wristwatch', 'wristwatch for men', and 'wristwatch for women' throughout the article. Format your response using markdown. Use headings, subheadings, bullet points, and bold to organize the information. Be sure the post ends with a full sentence followed by a period. post's minimum length must be 500 words. Maximum 800."
    #prompt = "Write an article aimed at helping readers select the perfect wristwatch to gift to their loved ones. Offer advice on understanding the recipient's preferences, occasions, and budget considerations. Highlight the sentimental value of a well-chosen wristwatch gift. Ensure the article is SEO-friendly and conveys a friendly and helpful tone throughout. End the article by expressing the significance of giving a wristwatch as a gift—a timeless gesture that not only marks special moments but also becomes a cherished symbol of the bond shared between the giver and the recipient."
    article_prompts = [
    "Generate an article about wristwatches that provides valuable advice and tips for watch enthusiasts. The article should have a friendly and informative tone, and it should focus on helping readers make informed decisions when it comes to choosing and maintaining wristwatches. Please ensure the article is SEO-friendly and contains approximately 500 words. Conclude the article by summarizing the key takeaways and encouraging readers to explore different types of wristwatches that suit their preferences and needs.",
    "Write an article about the different styles and features of wristwatches that watch enthusiasts should consider. Highlight the importance of matching the watch style with one's personal fashion preferences and occasions. Include tips on selecting the right watch size, material, and dial design. Please make the article SEO-oriented and maintain a friendly and approachable tone. Wrap up the article by reminding readers that choosing the perfect watch style is a reflection of their unique personality, and encourage them to experiment with different styles to find the one that resonates with them.",
    "Create an informative article about wristwatch maintenance and care. Share tips on how readers can keep their wristwatches in top condition for years to come. Include advice on cleaning, storing, and servicing watches regularly. Emphasize the longevity that proper care can add to a wristwatch's lifespan. Ensure the article is SEO-friendly and written in a helpful and approachable manner. Conclude the article by stressing the rewarding experience of owning a well-maintained wristwatch and how these simple care practices can keep their timepieces ticking for generations to come.",
    "Generate an article that delves into the art of watch collecting. Provide insights for both beginners and seasoned collectors on how to start, curate, and expand their wristwatch collections. Discuss factors such as rarity, brand reputation, and historical significance. Make the article informative, SEO-oriented, and maintain a warm and welcoming tone. Conclude the article by encouraging readers to embark on their own watch-collecting journey, reminding them that each watch they add to their collection tells a unique story and becomes a cherished piece of their personal history.",
    "Write an article aimed at helping readers select the perfect wristwatch to gift to their loved ones. Offer advice on understanding the recipient's preferences, occasions, and budget considerations. Highlight the sentimental value of a well-chosen wristwatch gift. Ensure the article is SEO-friendly and conveys a friendly and helpful tone throughout. End the article by expressing the significance of giving a wristwatch as a gift—a timeless gesture that not only marks special moments but also becomes a cherished symbol of the bond shared between the giver and the recipient."
]

    blog_post_titles = [
    "The Art of Wristwatch Styling: 7 Tips to Master Your Look",
    "From Casual to Formal: Matching Your Wristwatch to Any Outfit",
    "Wearing a Wristwatch with Bracelets: Dos and Don'ts",
    "Rocking a Sporty Wristwatch with Elegance: How to Pull it Off",
    "Wristwatch Etiquette: When and Where to Wear Different Styles",
    "Making a Statement: Bold Wristwatches and Outfit Pairings",
    "Dressing for Success: Elevating Your Professional Image with a Wristwatch",
    "Timeless Elegance: Pairing Vintage Wristwatches with Modern Attire",
    "Casual Chic: Integrating Leather Strap Wristwatches into Your Wardrobe",
    "Wristwatch and Cufflinks: Achieving the Perfect Formal Look",
    "Mixing Metals: Coordinating Your Wristwatch with Jewelry and Accessories",
    "Fitness and Fashion: Styling a Sports Wristwatch for Everyday Wear",
    "Leather or Metal? Choosing the Right Wristwatch Strap for Your Outfit",
    "Day to Night Transition: Adapting Your Wristwatch to Different Occasions",
    "Playing with Color: Adding a Pop of Vibrancy with Your Wristwatch",
    "Your Guide to Wristwatch Movements: Quartz vs. Mechanical",
    "Investment or Accessory? Factors to Consider When Buying a Wristwatch",
    "Diving into the Details: Understanding Water Resistance in Wristwatches",
    "Dressing Your Wrist: Choosing the Ideal Watch Size for Your Wrist",
    "Beyond Timekeeping: Exploring Complications in Luxury Wristwatches",
    "Iconic or Unique? Navigating the World of Wristwatch Designs",
    "Metal Matters: Comparing Stainless Steel, Titanium, and Gold Watches",
    "High-End Horology: Selecting a Wristwatch from Prestigious Watchmakers",
    "Vintage vs. Modern: Pros and Cons of Different Wristwatch Eras",
    "A Gift of Time: Finding the Perfect Wristwatch for a Loved One",
    "Wristwatch Crystals Unveiled: Sapphire vs. Mineral vs. Acrylic",
    "Trendy vs. Timeless: Ensuring Longevity in Your Wristwatch Choice",
    "Your Wrist, Your Style: Customization Options for Wristwatches",
    "Smart Choices: Incorporating Smartwatch Features into Your Lifestyle",
    "Beyond the Brand: Exploring Independent Wristwatch Makers",
    "A Brief History of Wristwatches: From WWI to Modern Times",
    "The Craftsmanship Behind Luxury Wristwatches: Artistry in Every Detail",
    "Watch Care 101: Essential Maintenance Tips for Your Wristwatch",
    "The Evolution of Wristwatch Materials: Innovation in Watchmaking",
    "Behind the Scenes: Unveiling the Wristwatch Manufacturing Process",
    "Wristwatches as Heirlooms: Passing Down Timepieces Through Generations",
    "Famous Wristwatches in Pop Culture: From James Bond to Hollywood Icons",
    "Exploring the World of Limited Edition Wristwatches: Rarity and Value",
    "Horology and Beyond: How Wristwatches Have Transformed Our Lives",
    "The Psychology of Wristwatches: What Your Choice Says About You",
    "Watch Enthusiast's Paradise: Must-Visit Museums and Exhibitions",
    "Wristwatches and the Art of Collecting: Starting and Nurturing a Collection",
    "Time Travel through Wristwatches: Vintage Pieces and Their Stories",
    "Sustainable Horology: Eco-Friendly Practices in the Wristwatch Industry",
    "Iconic Watch Design Elements: Hands, Indices, and Dials That Stand Out",
]

    blog_post_images = [
        "1508",
        "1673",
        "1554",
        "1446",
        "1388",
        "1382",
        "1380",
        "1372",
        "1390",
        "1400",
    ]
    
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
