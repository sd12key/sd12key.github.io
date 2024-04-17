============ Automatic Blog Generator (using OpenAI API) =================

1. Settings file (with API keys and local repository folders): ".env"
2. Blog generation initial prompt and model parameters: "blog.txt" (must me filled out)
3. Program file: "blog.py" (imports "parser.py")
4. To run: "python blog.py" (some dependencies like openai, dotenv, git, etc. must be installed)

Description: Generates blog with a given title and corresponding image.
Adds link to a newly generated blof to the main page.
(some experimenting with GPT-prompt is reqired, YMMV)

Blog location: http://sd12key.github.io

Example of a "blog.txt" file contents (GPT prompt and model parameters):
--------------------------------------------------------------------------
CHATGPT
model="gpt-4-turbo"
title="Blog Title",
system="You are an expert blog writer",
user="""I'm a blogger needing your help in writing a small story.
Blog title: {title}
Blog contents: """,
temperature=1.0,
max_tokens=100,
top_p=1,
frequency_penalty=0,
presence_penalty=0,

DALLE
model="dall-e-3",
prompt="Art about {title}",
size="1024x1024",
quality="standard",
style="natural",
n=1,
--------------------------------------------------------------------------
This corresponds to the following OpenAI API calls:
({title} is replaced with blog title text).
--------------------------------------------------------------------------

==GhatGPT==
response = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[
        {
            "role": "system",
            "content": "You are an expert blog writer"
        },
        {
            "role": "user",
            "content": "I'm a blogger needing your help in writing a small story.\nBlog title: Blog Title\nBlog contents: "
        }
    ],
    temperature=1.0,
    max_tokens=100,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
)    

==DALL-E==
response = client.images.generate(
	model="dall-e-3",
	prompt="Art about Blog Title",
	size="1024x1024",
	quality="standard",
	style="natural",
	n=1,
)

