import datetime, os, shutil, json, requests
from openai import OpenAI
from dotenv import dotenv_values
from pathlib import Path
from git import Repo
import parser

#get keys from the .env file
config = dotenv_values(".env")
git_repo_path = Path(config["LOCAL_PATH"])
mainpage_path = git_repo_path.parent
blogs_path = Path(config["BLOGS_PATH"])
git_token=config["GIT_TOKEN"]
input_file = Path(config["BLOG_INPUT_FILE"])

def update_git_repo():
    repo = Repo(git_repo_path)
    repo.git.add(all=True)
    repo.index.commit("Blog post update")
    #set up the remote URL with the token
    origin = repo.remote(name='origin')
    origin_url = origin.url  # Get the current URL to replace user info
    #print(origin_url)
    #insert the token only if it is not already there
    if 'x-access-token' not in origin_url:
        new_url = origin_url.replace('https://', f'https://x-access-token:{git_token}@')
        origin.set_url(new_url)  # Set the new URL with the token temporarily
    #push changes
    origin.push()
    origin.set_url(origin_url)

def create_blog_post(blog_title,blog_contents,blog_image):
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d-%H-%M-%S")
    formatted_datetime_index = current_datetime.strftime("%d %b '%y (%I:%M%p)")
    formatted_datetime_index = formatted_datetime_index.replace('AM', 'am').replace('PM', 'pm')
    blog_image_path=blogs_path/f"{formatted_datetime}-image.jpg"
    if not os.path.exists(blog_image_path):
        shutil.copy(Path(blog_image), blog_image_path)
    else:
        raise FileExistsError(f"Image {blog_image_path} already exists!")

    blog_html_path=blogs_path/f"{formatted_datetime}-post.html"
    if not os.path.exists(blog_html_path):
        shutil.copy(Path(config["BLANK_BLOG_HTML"]), blog_html_path)
        with open(blog_html_path, "r") as f:
            html_content = f.read()
        html_content = html_content.replace("BLOGTITLE", blog_title)
        html_content = html_content.replace("BLOGIMAGE", Path(blog_image_path).name)
        html_paragraphs = ''.join(f"<p>{line}</p>\n" for line in blog_contents.split('\n'))
        html_content = html_content.replace("<p>BLOGCONTENTS</p>", html_paragraphs)
        # Write the updated HTML to a new file
        html_content_utf8 = html_content.encode('utf-8')
        html_content = html_content_utf8.decode('utf-8')
        with open(blog_html_path, "w") as f:
            f.write(html_content)    
        print(f"Blog post <{blog_title}> created successfully!")
    else:
        raise FileExistsError(f"Blog post {blog_title} already exists!")
    
    git_blog_path = Path(Path(blog_html_path).parent.name)/Path(blog_html_path).name
    #print(git_blog_path)
    hyperlink_html = f'\n\n<h2><a href="{git_blog_path}"><span style="font-size: 60%;">{formatted_datetime_index}</span></a> {blog_title}</h2>'
    main_index_html = Path(mainpage_path)/"index.html" 
    with open(main_index_html, "r") as f:
        index_html_content = f.read()
    div_index = index_html_content.find("<div")
    if div_index != -1:
        # Find the closing '>' of the first <div
        closing_div_index = index_html_content.find(">", div_index) + 1
        # Insert the hyperlink right after the closing '>'
        updated_html_content = index_html_content[:closing_div_index] + hyperlink_html + index_html_content[closing_div_index:]
        # Write the updated content back into the index.html file
        with open(main_index_html, "w") as file:
            file.write(updated_html_content)
        print("Hyperlink inserted successfully.")
    else:
        print("Could not find a <div> tag in the file.")

    return [blog_html_path,blog_title,current_datetime]
    
#print(blogs_path)
#print(mainpage_path)
#print(input_file)

parameters = parser.parse_parameters(input_file)
print("\nCheck the parameters from blog input file:")
print(json.dumps(parameters, indent=4))
if parser.wait_for_key():
    print("Continuing...")
else:
    print("Aborted.")
    exit()

#create OpenAI client with OPENAI_API_KEY
client = OpenAI(api_key = config["OPENAI_API_KEY"])
response = client.chat.completions.create(
    model=parameters['chatgpt']['model'],
    messages=[
        {
            "role": "system",
            "content": parameters['chatgpt']['system']
        },
        {
            "role": "user",
            "content": parameters['chatgpt']['user']
        }
    ],
    temperature=parameters['chatgpt']['temperature'],
    max_tokens=parameters['chatgpt']['max_tokens'],
    top_p=parameters['chatgpt']['top_p'],
    frequency_penalty=parameters['chatgpt']['frequency_penalty'],
    presence_penalty=parameters['chatgpt']['presence_penalty']
)    

blog_text=response.choices[0].message.content
blog_text_utf8=blog_text.encode('utf-8')
blog_text=blog_text_utf8.decode('utf-8')
ascii_blog_text = parser.convert_to_ascii(blog_text)
blog_text = ascii_blog_text
#print(blog_text)

response = client.images.generate(
  model=parameters['dalle']['model'],
  prompt=parameters['dalle']['prompt'],
  size=parameters['dalle']['size'],
  quality=parameters['dalle']['quality'],
  style=parameters['dalle']['style'],
  n=parameters['dalle']['n'],
)

image_url = response.data[0].url
#print(image_url,"\n\n")
#print(response,"\n\n")

image_data = requests.get(image_url)
image_path = "blog.png"
if image_data.status_code == 200:
    with open(image_path, 'wb') as file:
        file.write(image_data.content)
    print("Image saved successfully.")
else:
    print("Failed to retrieve image.")

print("Creating a new blog post...")
new_blog=create_blog_post(parameters['chatgpt']['title'],blog_text,image_path)
#print(new_blog)

update_git_repo()

exit()
