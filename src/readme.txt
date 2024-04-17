============ Automatic Blog Generator (using OpenAI API) =================

1. Settings file (with API keys and local repository folders): ".env"
2. Blog generation initial prompt and model parameters: "blog.txt" 
   (must me filled out)
3. Program files: "blog.py" and "parser.py"
4. To run: "python blog.py" 
   (some dependencies like apenai, dotenv, git, etc. must be installed)

Description: Generates blog and image according to GPT-prompt and title
Blog location: http://sd12key.github.io

Example contents of a GPT prompt and parameters file "blog.txt":
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
prompt="Art showing female rhythmic gymnast in a competition",
size="1024x1024",
quality="standard",
style="natural",
n=1,
--------------------------------------------------------------------------
this corresponds to the following OpenAI API calls:
