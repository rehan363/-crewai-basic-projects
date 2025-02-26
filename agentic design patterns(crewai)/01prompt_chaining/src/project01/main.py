from dotenv import load_dotenv
from crewai.flow.flow import Flow, start, listen
from litellm import completion
import os


load_dotenv()

class Blog(Flow):               #inheritance from Flow class
    model= "gemini/gemini-1.5-flash"
    print("starting blog generator...")
    @start()
    def generate_blog(self):
        result = completion(
            model= self.model,
            api_key= os.getenv("GEMINI_API_KEY"),
            messages= [
                {
                    'role': 'user',
                    'content': 'you are a blog generator. please generate a blog post for me on latest 2025 trending topic.'
                }
            ]

        )
        blog_post = result['choices'][0]['message']['content']
        print("generated blog post: ", blog_post)
        self.state['blog_post'] = blog_post
        return blog_post
    
    @listen(generate_blog)
   
    def summarization(self, blog_post):
        result = completion(
            model= self.model,
            api_key= os.getenv("GEMINI_API_KEY"),
            messages= [
                {
                    'role': 'user',
                    'content': f'summarize the given blog {blog_post} in 1 line.'
                }
            ]
        )
        summary = result['choices'][0]['message']['content']
        print("summary: ", summary)
        self.state['summary'] = summary
        return summary
    
    @listen(summarization)
    def save_blog_post_and_summary(self):
        with open('blog_post.txt', 'w') as file:
            file.write(f"**Blog post:**\n{self.state['blog_post']}\n\n")
            file.write("==========x=============x==========x============x===\n")
            file.write(f"==**Summary of the blog post:**\n{self.state['summary']}==")

def kickoff(): 
    flow = Blog()
    result = flow.kickoff()
    return result
    # print("generated blog post: ", result['blog_post'])
    # print("summary: ", result['summary'])
        



