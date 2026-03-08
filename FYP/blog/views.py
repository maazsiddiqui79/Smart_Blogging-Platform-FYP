import random
import threading
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
from django.utils.html import strip_tags
from django.core.paginator import Paginator

# Local Application Imports
from .models import Blog, BlogKeyword,Comment,Bookmark
from .forms import ProfileUpdateForm, CommentForm
from .mail_file import MAIL_SENDIND
from .Notify_followers import Notify_follower

# ========================================================
#                   AUTHENTICATION SYSTEM
# ========================================================

User = get_user_model()

@login_required
def logout(request):
    auth_logout(request)
    request.session['isSigin']=True
    return redirect('home')  # or 'home'

def generate_otp():
    return str(random.randint(100000, 999999))

    

def fogretcred(request):
    """
    Handles forgotten credentials, including password reset and username recovery.

    This view manages multiple actions based on the 'unique-attr' POST parameter:
    - 'send-otp': Sends a password reset OTP to the user's email.
    - 'verify-otp': Verifies the OTP and updates the user's password.
    - 'recover-username': Sends the username to the user's email.
    """
    if request.method == 'POST':
        unique_attr:str = request.POST.get('unique-attr')
      # STEP 1: Send OTP for password reset
        if unique_attr == "send-otp":
            email = request.POST.get("email")

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, "No account found with this email")
                return redirect("forget-id-pass")

            otp = generate_otp()

            # Store OTP and email in the session for verification
            request.session["reset_email"] = email
            request.session["reset_otp"] = otp

            # Send OTP via email
            MAIL_SENDIND(revicers_email=email, indent="reset-password", otp=otp)
            x = MAIL_SENDIND(revicers_email=email,indent=unique_attr,username=user.username,otp=otp)



            request.session["otp_sent"] = True
            messages.success(request, "OTP sent to your email")
            return redirect("forget-id-pass")

        # STEP 2: Verify OTP and update the password
        if unique_attr == "verify-otp":
            entered_otp = request.POST.get("otp")
            password = request.POST.get("password")

            session_otp = request.session.get("reset_otp")
            email = request.session.get("reset_email")

            # Check if the entered OTP matches the one in the session
            if not session_otp or entered_otp != session_otp:
                messages.error(request, "Invalid OTP")
                return redirect("forget-id-pass")

            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()

            # Clean up session variables
            request.session.flush()

            messages.success(request, "Password updated successfully")
            return redirect("sign_in")

        # Handle username recovery
        if unique_attr.lower() == 'recover-username':
            email:str = request.POST.get("email")
            user = User.objects.get(email=email)
            # Send username to the user's email
            x = MAIL_SENDIND(revicers_email=email,indent=unique_attr,username=user.username)
            messages.success(request, "Mail sent")
            # print(x.status)
            return redirect('forget-id-pass')
        
        # Handle direct password update (requires email and new password)
        if unique_attr.lower() == 'pass-update':
            
            email:str = request.POST.get("email")
            password:str = request.POST.get("password")
            re_password:str = request.POST.get("re-password")
            
            # Check if passwords match
            if password == re_password:
                if not password or not re_password or not password.strip() or not re_password.strip():
                    messages.error(request,f"Enter your credentials to proceed.")
                    return redirect('forget-id-pass')
                try:
                    user = User.objects.get(email=email)
                except User.DoesNotExist:
                    messages.error(request,f"User Not Found")
                    return redirect('forget-id-pass')
                
                # Set the new password
                user.set_password(password)
                x = MAIL_SENDIND(revicers_email=email,indent=unique_attr)
                messages.success(request,f"Mail Sent")
                # print(x.revicers_email)
                user.save()
                return redirect('forget-id-pass')
            else:
                messages.error(request,f"Password Mismatch")
                return redirect('forget-id-pass')
        
    return render(request, 'fogretcred.html')

def sign_in(request):
    """
    Handles user authentication.
    """
    if request.method == 'POST':

        email:str = request.POST.get('email')
        password:str = request.POST.get('password')
        if not email or not password:
            if not email.strip() or not password.strip():
                messages.error(request,f"Enter your credentials to proceed.")
                return redirect('sign_in')            
            
        
        try:
            # Allow login with either email or username
            user_obj = User.objects.get(Q(email=email) | Q(username=email))
        except User.DoesNotExist:
            messages.error(request,"Invalid username or password. Please try again.")
            return redirect('sign_in')            
        if user_obj is not None:
            if user_obj.check_password(password):
                login(request,user_obj)
                request.session['isSigin']=False
                return redirect('dashboard')            
        messages.error(request, "Invalid username or password. Please try again, or create an account if you don’t have one.")
        return redirect('sign_in')            
            
            
        # user = authenticate(request,username)
                
    return render(request, 'login_signin.html')

def sign_up(request):
    """
    Handles new user registration.
    """
    if request.method == 'POST':
        username:str = request.POST.get('username')
        email:str = request.POST.get('email')
        password:str = request.POST.get('password')
        full_name:str = request.POST.get('full_name')
        website:str = request.POST.get('website')
        instagram_link:str = request.POST.get('instagram_link')
        x_link:str = request.POST.get('x_link')
        git_link:str = request.POST.get('git_link')
        bio:str = request.POST.get('bio')
        
        # Check for existing user with the same email or username
        if (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists() ):
            messages.error(request,"Email or Username already exists try some thing new")
            return redirect('sign_up')

        user = User(username=username,
        email=email,
        password=password,
        full_name=full_name,
        website=website,
        instagram_link=instagram_link,
        x_link=x_link,
        git_link=git_link,
        bio=bio)
        user.set_password(password)
        messages.success(request, "Account created successfully!")
        user.save()
        # print(username,email,password,full_name,website,instagram_link,x_link,git_link,bio)
        # print("ADDED SUCCESSFULY")
        return redirect('sign_up')
    return render(request, 'register_signup.html')



# ========================================================
#                   CORE BLOG LOGIC
# ========================================================

from django.db.models import Count

def home(request):
    blog_list = Blog.objects.filter(
        status="PUBLISHED"
    ).order_by("-created_at")

    # Trending blog (most liked)
    latest_blogs = []

    blog = (
        Blog.objects
        .filter(status="PUBLISHED")
        .annotate(likes_count=Count("likes"))
        .order_by("-likes_count")
        .first()
    )

    if blog:
        latest_blogs.append(blog)

    return render(
        request,
        "home.html",
        {
            "blogs": blog_list,
            "latest_blogs": latest_blogs,
        }
    )

from django.db.models import OuterRef, Subquery
@login_required
def dashboard(request):

    blog_list = Blog.objects.filter(
        status="PUBLISHED"
    ).order_by("-created_at")

    # category filter
    category = request.GET.get("category")
    if category and category != "all":
        blog_list = blog_list.filter(category=category)

    # search
    query = request.GET.get("q")
    if query:
        blog_list = blog_list.filter(title__icontains=query)

    # trending blog (most likes)
    trending_blog = (
        Blog.objects
        .filter(status="PUBLISHED")
        .annotate(likes_count=Count("likes"))
        .order_by("-likes_count")
        .first()
    )

    # pagination
    paginator = Paginator(blog_list, 8)
    page_number = request.GET.get("page")
    blogs = paginator.get_page(page_number)

    user = request.user
    following_users = user.following.all()

    latest_blogs = []

    for author in following_users:

        blog = (
            Blog.objects
            .filter(author=author, status="PUBLISHED")
            .order_by("-created_at")
            .first()
        )

        if blog:
            latest_blogs.append(blog)

    bookmarked_blogs = Blog.objects.filter(
        bookmarked_by__user=request.user
    ).distinct()

    return render(
        request,
        "dashboard.html",
        {
            "blogs": blogs,
            "latest_blogs": latest_blogs,
            "bookmarked_blogs": bookmarked_blogs,
            "trending_blog": trending_blog,
            "selected_category": category,
        }
    )
    
@login_required
def create_blog_func(request):
    """
    Handles the creation of a new blog post.

    - Processes the submitted form data to create a new blog instance.
    - Associates keywords with the blog.
    - Notifies the author's followers about the new post in a separate thread.
    """
    if request.method == 'POST':
        # Retrieve blog data from the POST request
        title = request.POST.get('title')
        title_bg = request.POST.get('color')
        slug = request.POST.get('slug')
        short_description = request.POST.get('short_description')
        category = request.POST.get('category')
        keywords_raw = request.POST.get('keywords')  # comma separated
        content = request.POST.get('content')
        status = request.POST.get('visibility')
        cover_image = request.FILES.get('cover_image')

        # Create the blog instance first, as it's needed for ManyToMany relationships
        blog = Blog.objects.create(
            author=request.user,
            title=title,
            title_bg_color=title_bg,
            slug=slug,
            short_description=short_description,
            content=content,
            category=category,
            status=status,
            cover_image=cover_image
        )
        # Increment the author's total post count
        request.user.total_posts +=1
        request.user.save()
        
        # Notify followers in a non-blocking background thread
        threading.Thread(
            target=Notify_follower,
            args=(request.user, blog),
            daemon=True).start()


        # If the blog is published, set the publication timestamp
        if status == "PUBLISHED":
            
            blog.published_at = timezone.now()
            blog.save(update_fields=["published_at"])

        # Process and associate keywords with the blog
        if keywords_raw:
            keyword_list = [k.strip() for k in keywords_raw.split(",") if k.strip()]
            for word in keyword_list:
                # Get or create the keyword and add it to the blog's keywords
                keyword_obj, _ = BlogKeyword.objects.get_or_create(name=word)
                blog.keywords.add(keyword_obj)

        

        # Debugging output (optional)
        print("STATUS:", status)
        print("PLAIN CONTENT:", strip_tags(content))
        if status == "PUBLISHED":
            messages.success(request, "Blog published successfully.")
            return render(request, "create_blog_file.html", {"blog": blog})


    return render(request, "create_blog_file.html")

@login_required
def delete_blog_func(request, id):
    """
    Deletes a blog post. Ensures that only the author of the blog can delete it.
    """
    if request.method != 'POST':
        return redirect('user_profile')

    blog = get_object_or_404(
        Blog,
        id=id,
        author=request.user
    )
    request.user.total_posts -=1
    request.user.save()

    blog.delete()
    messages.success(request, "Blog deleted successfully.")
    return redirect('user_profile')
    
    
@login_required
def change_visibility(request, id,status):
    """
    Changes the visibility of a blog post (e.g., from 'DRAFT' to 'PUBLISHED').
    """
    

    blog = get_object_or_404(
        Blog,
        id=id,
        author=request.user
    )
    blog.status=status
    blog.save()

    print(blog)
    print(blog.status)
    
    print(id)
    print(status)
    messages.success(request, "Blog Visibility Changed Successfully.")
    return redirect('user_profile')
    
    
@login_required
def access_blog(request, id):
    blog = get_object_or_404(Blog, id=id)
    comments = blog.comments.all()

    # ✅ ADD THIS BLOCK
    is_bookmarked = Bookmark.objects.filter(
        user=request.user,
        blog=blog
    ).exists()

    if request.method == 'POST':
        Blog.objects.filter(id=blog.id)\
            .update(total_comments=F("total_comments") + 1)

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.author = request.user
            comment.save()
            return redirect('access_blog', id=blog.id)
    else:
        form = CommentForm()

    context = {
        'blog': blog,
        'comments': comments,
        'form': form,
        'is_bookmarked': is_bookmarked,  # ✅ PASS TO TEMPLATE
    }

    return render(request, 'access_blog.html', context)
@login_required
def access_blog_slug(request, slug):
    blog = get_object_or_404(Blog, slug=slug)

    return redirect('access_blog',id=blog.id)

    
    
@login_required
def edit_blog(request, blog_id):
    """
    Handles editing of an existing blog post.
    """
    blog = get_object_or_404(Blog, id=blog_id, author=request.user)

    if request.method == "POST":
        blog.title = request.POST.get("title")
        blog.title_bg_color = request.POST.get("title_bg_color", "NONE")
        blog.slug = request.POST.get("slug")
        blog.short_description = request.POST.get("short_description")
        blog.category = request.POST.get("category")
        blog.content = request.POST.get("content")
        blog.status = request.POST.get("visibility")

        if request.FILES.get("cover_image"):
            blog.cover_image = request.FILES["cover_image"]

        blog.save()
        messages.success(request, "Blog updated successfully.")

    return redirect(request.META.get("HTTP_REFERER", "/user-profile/"))


def search_blogs(request):
    """
    Searches for blogs based on a query string provided by the user.

    """
    
    query = request.GET.get('q')
    blogs = Blog.objects.filter(status="PUBLISHED").order_by("-created_at")
    if query:
        blogs = blogs.filter(
            Q(title__icontains=query) |
            Q(short_description__icontains=query) |
            Q(content__icontains=query) |
            Q(category__icontains=query)
        ).distinct()

    context = {
        'blogs': blogs,
        'query': query,
    }
    return render(request, 'search_results.html', context)


# ========================================================
#                   SOCIAL & PROFILE LAYER
# ========================================================

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Blog
from .forms import ProfileUpdateForm


@login_required
def user_profile(request):
    """
    Handles the user profile page.

    - Displays profile details and user's blogs (GET).
    - Updates profile details including image (POST).
    """

    # Fetch blogs created by the logged-in user (latest first)
    blogs = Blog.objects.filter(author=request.user).order_by('-created_at')

    # Users that the current user follows
    following_users = request.user.following.all()
    followers = request.user.followers.all() 


    if request.method == 'POST':
        form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user
        )

        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('user_profile')

        else:
            messages.error(request, "Please correct the errors below.")

    else:
        form = ProfileUpdateForm(instance=request.user)

    context = {
        'blogs': blogs,
        'form': form,
        'following_users': following_users,
        'followers': followers,

    }

    return render(request, 'profile.html', context)



@login_required
def public_profile(request, username):
    """
    Displays the public profile of a user, showing their published blogs.
    """
    author = get_object_or_404(User, username=username)
    author_likes = (
        Blog.objects
        .filter(author=author)
        .aggregate(total=Sum("total_likes"))
        .get("total") or 0
    )
    total_comments = (
        Blog.objects
        .filter(author=author)
        .aggregate(total=Sum("total_comments"))
        .get("total") or 0
    )
    print(author_likes)
    blogs = Blog.objects.filter(
        author=author,
        status="PUBLISHED"
    ).order_by("-published_at")
    
    context = {
        'author': author,
        'blogs': blogs,
        'author_likes':author_likes,
        'total_comments':total_comments,
    }
    

    return render(request,'public_profile.html', context)


@login_required
def follow_user(request, username):
    """
    Toggles the follow status of a user.
    """
    target_user = get_object_or_404(User, username=username)

    # Prevent users from following themselves
    if request.user == target_user:
        return redirect("public_profile",username=username)
    
    # If already following, unfollow. Otherwise, follow.
    if request.user in target_user.followers.all():
        target_user.followers.remove(request.user)
    else:
        target_user.followers.add(request.user)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

from django.db.models import F
from django.db.models import Sum

@login_required
def like_blog(request, id):
    blog = get_object_or_404(Blog, id=id)

    if blog.likes.filter(id=request.user.id).exists():
        blog.likes.remove(request.user)
        Blog.objects.filter(id=blog.id, total_likes__gt=0)\
            .update(total_likes=F("total_likes") - 1)
    else:
        blog.likes.add(request.user)
        Blog.objects.filter(id=blog.id)\
            .update(total_likes=F("total_likes") + 1)

    return redirect("access_blog", id=blog.id)



from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.db.models import F
from .models import Blog






@login_required
def add_blog_bm(request, id):
    blog = get_object_or_404(Blog, id=id)

    bookmark = Bookmark.objects.filter(
        user=request.user,
        blog=blog
    ).first()

    if bookmark:
        bookmark.delete()
    else:
        Bookmark.objects.create(
            user=request.user,
            blog=blog
        )

    return redirect(request.META.get('HTTP_REFERER', 'access_blog'), id=blog.id)
# ========================================================
#                   SOCIAL & PROFILE LAYER
# ========================================================

@login_required
def email_verify(request):

    # 🔹 GET → Send OTP
    if request.method == "GET":
        print('Enter GET')
        otp = generate_otp()
        request.session["verify_email_otp"] = otp
        request.session["verify_email_id"] = request.user.email

        MAIL_SENDIND(revicers_email=request.user.email, indent="verify-email", otp=otp)
        # x = MAIL_SENDIND(revicers_email=email,indent=unique_attr,username=user.username,otp=otp)

        request.session["email_otp_sent"] = True
        messages.success(request, "OTP sent to your email")
        
        print('Exit GET')
        return redirect("user_profile")

    # 🔹 POST → Verify OTP
    if request.method == "POST":
        print('Enter POST')
        user_otp = request.POST.get("otp")
        session_otp = request.session.get("verify_email_otp")
        session_email = request.session.get("verify_email_id")
        check_mail_sent = request.session.get("email_otp_sent")

        if not user_otp or not session_otp:
            messages.error(request, "OTP not found. Please try again.")
            return redirect("user_profile")

        if user_otp == session_otp and request.user.email == session_email:
            if check_mail_sent==True:
                request.user.email_verified = True
                request.user.save(update_fields=["email_verified"])

                # cleanup
                del request.session["verify_email_otp"]
                del request.session["verify_email_id"]

                messages.success(request, "Email verified successfully.")
        else:
            messages.error(request, "Invalid OTP.")

        print('Exit POST')
        return redirect("user_profile")  
    
      
def guide(request): 
    
    return render(request,'guide.html')



@login_required
def delete_acc(request):
    if request.method == "POST":
        user = request.user
        
        commented_blogs = Blog.objects.filter(comments__author=user).distinct()
        for blog in commented_blogs:
            count = Comment.objects.filter(blog=blog, author=user).count()
            blog.total_comments = max(0, blog.total_comments - count)
            blog.save(update_fields=["total_comments"])
        # 🔹 Remove likes by this user
        liked_blogs = Blog.objects.filter(likes=user)
        for blog in liked_blogs:
            blog.total_likes = max(0, blog.total_likes - 1)
            blog.save(update_fields=["total_likes"])
            blog.likes.remove(user)

        # 🔹 Delete user's blogs (CASCADE already deletes comments)
        Blog.objects.filter(author=user).delete()

        auth_logout(request)
        user.delete()

        return redirect("home")
    
    return redirect("user_profile")
    
# ------------------------------------------------------------------------------------
def terms_n_condtion(request):
    return render(request,'terms.html')


def privacy(request):
    return render(request,'privacy.html')


def custom_404_view(request, exception=None):
    
    return HttpResponse("""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Page Not Available | Smart Blogger</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">

  <!-- Bootstrap CSS -->
  <link
    href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css"
    rel="stylesheet"
  >

  <style>
    body {
      background: #f8f9fc;
      font-family: "Segoe UI", system-ui, -apple-system, BlinkMacSystemFont;
      color: #1f2937;
    }

    .error-wrapper {
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .error-card {
      background: #ffffff;
      border-radius: 16px;
      padding: 3rem 2.5rem;
      max-width: 520px;
      width: 100%;
      box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08);
      text-align: center;
    }

    .error-code {
      font-size: 4.5rem;
      font-weight: 800;
      color: #0d6efd;
      letter-spacing: 2px;
    }

    .error-title {
      font-size: 1.4rem;
      font-weight: 600;
      margin-top: 0.5rem;
    }

    .error-desc {
      font-size: 0.95rem;
      color: #6b7280;
      margin-top: 1rem;
      line-height: 1.6;
    }

    .info-box {
      background: #f1f5ff;
      border-left: 4px solid #0d6efd;
      padding: 1rem;
      border-radius: 8px;
      margin-top: 1.5rem;
      text-align: left;
      font-size: 0.9rem;
    }

    .btn-home {
      margin-top: 2rem;
      padding: 0.6rem 1.6rem;
      border-radius: 30px;
      font-weight: 500;
    }

    .footer-note {
      margin-top: 1.5rem;
      font-size: 0.8rem;
      color: #9ca3af;
    }
  </style>
</head>

<body>

  <div class="error-wrapper">
    <div class="error-card">

      <div class="error-code">404</div>

      <div class="error-title">
        Page Not Found
      </div>

      <p class="error-desc">
        The page you are trying to access does not exist, has been removed,
        or is temporarily unavailable. This can happen if the link is outdated
        or the content has been moved.
      </p>

      <div class="info-box">
        <strong>What you can do:</strong>
        <ul class="mb-0 mt-2">
          <li>Check the URL for typing errors</li>
          <li>Return to the homepage and continue browsing</li>
          <li>Access content from your dashboard</li>
        </ul>
      </div>

      <a href="/" class="btn btn-primary btn-home">
        Go Back to Home
      </a>

      <div class="footer-note">
        Smart Blogger · Intelligent Blogging Platform
      </div>

    </div>
  </div>

</body>
</html>

""", status=404)