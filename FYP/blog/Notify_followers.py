from .mail_file import MAIL_SENDIND

class Notify_follower():
    def __init__(self,author,blog):
        self.author =author
        self.blog =blog
        self.notify()
        
        
    def notify(self):
        print(self.blog.title)
        
        
        followers = self.author.followers.all()
        print(followers)
        for follower in followers:
            
            # MAIL_SENDIND(indent='post-notify',revicers_email=follower.email,username=self.author.username)
            MAIL_SENDIND(
                indent='post-notify',
                revicers_email=follower.email,
                username=self.author.username,
                title=self.blog.title,
                slug=self.blog.slug,
                doc=self.blog.created_at,
                )
            print(f"Mail sent to {follower.email}")
            
            print(
                
                f"Notify {follower.username}:"
                f"Notify email: {follower.email}:"
                f"New blog '{self.blog.title}' by {self.author.username}\n")