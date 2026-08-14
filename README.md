# 📌 SmartBlogger — AI-Powered Blog Platform with Intelligent Chatbot


## 📑 Table of Contents

- [📖 Overview](#-overview)
- [🎯 Objectives](#-objectives)
- [✨ Key Features](#-key-features)
  - [🤖 AI Chatbot System](#-ai-chatbot-system)
  - [📊 Blog Analytics Dashboard](#-blog-analytics-dashboard)
  - [📚 Blog Platform Features](#-blog-platform-features)
- [🧠 System Workflow](#-system-workflow)
- [📊 Analytics Features](#-analytics-features)
- [🏗 System Architecture](#-system-architecture)
- [🗄️ Database Structure](#️-database-structure)
- [🖥️ Project Screenshots](#️-project-screenshots)
- [🛠 Technology Stack](#-technology-stack)
- [⚙️ Installation & Setup](#️-installation--setup)
- [📂 Project Modules](#-project-modules)
- [🚀 Future Enhancements](#-future-enhancements)
- [👥 Team Members](#-team-members)
- [🎓 Project Information](#-project-information)
- [📌 Project Status](#-project-status)
- [📜 License](#-license)

---

# 📖 Overview

An **SmartBlogger — AI-Powered Blog Platform** integrated with an intelligent chatbot that answers user questions using blog content as its primary knowledge base.

The chatbot analyzes blog data to provide accurate responses. If the requested information is not available in the blog, the system performs **external web search** and provides **reference links**.

The platform also includes a **professional analytics dashboard** that tracks user engagement, blog views, reading behavior, and audience activity.

> 🎓 Developed as a **Final Year Diploma Project in Computer Engineering**

---

# 🎯 Objectives

- Deliver instant answers from blog content using AI  
- Improve reader engagement through conversational interaction  
- Provide source-aware responses with blog references  
- Reduce manual searching for blog information  
- Provide bloggers with insights about reader behavior and engagement  

---

# ✨ Key Features

## 🤖 AI Chatbot System

- AI-powered chatbot integrated into the blog platform  
- Uses blog content as the main knowledge base  
- Context-aware question answering  
- Direct navigation to the relevant blog section  
- External web search with reference links when content is unavailable  

---

## 📊 Blog Analytics Dashboard

- Blog **views tracking system**
- Engagement metrics for **likes and comments**
- **Peak traffic time analysis**
- **Traffic by hour visualization**
- **Returning vs new readers insights**
- Centralized **analytics dashboard for bloggers**

---

## 📚 Blog Platform Features

- Blog creation and management system  
- Comment system for reader interaction  
- Blog engagement tracking  
- Fully responsive user interface  
- Clean and intuitive user experience  

---

# 🧠 System Workflow

### Step 1
User asks a question through the chatbot interface.

### Step 2
The chatbot searches the **blog knowledge database** for relevant information.

### Step 3
If the answer exists within the blog:

- The chatbot returns the response  
- Provides a **direct link to the relevant blog section**

### Step 4
If the answer is not found:

- The system performs **external web search**
- Displays the result with **reference source links**

### Step 5
User interactions such as **views, likes, and comments** are automatically tracked.

### Step 6
The analytics system processes this data to generate **engagement insights and traffic analysis**.

---

# 📊 Analytics Features

| Feature | Description |
|-------|-------------|
| Blog Views | Tracks how many times each blog is read |
| Likes Tracking | Measures user appreciation and engagement |
| Comment Tracking | Monitors reader discussion and interaction |
| Peak Traffic Time | Identifies the hours when most readers are active |
| Traffic by Hour | Visual chart of reading activity |
| Returning vs New Readers | Measures audience loyalty and community growth |
| Engagement Dashboard | Central analytics panel for bloggers |

---

# 🏗 System Architecture

```

                    User
                     │
                     ▼
              Django Application
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
   Blog System   Chatbot System  Analytics
        │            │            │
        ▼            ▼            ▼
    Database    Retrieval Layer  Analytics DB
                     │
              ┌──────┴──────┐
              ▼             ▼
        Blog Content    Web Search

```

### Analytics System

```

User Interaction
→ Views
→ Likes
→ Comments
→ Reading Time
→ Traffic Analysis

```

---

# 🗄️ Database Structure

The Smart Blogging Platform uses Django ORM to manage application data and database relationships.

The database is organized around users, blog content, engagement, bookmarks, comments, and analytics.

## 👤 User

The `User` model is the custom authentication and profile model used throughout the platform.

| Field | Type | Description |
|-------|------|-------------|
| `id` | BigAutoField | Primary key |
| `username` | CharField | Unique username |
| `email` | EmailField | Unique email address used for authentication |
| `password_updated_at` | DateTimeField | Stores the last password update time |
| `role` | CharField | Defines whether the account is a normal user or blogger |
| `is_staff` | BooleanField | Determines whether the user can access staff functionality |
| `email_verified` | BooleanField | Stores email verification status |
| `full_name` | CharField | User's full name |
| `bio` | TextField | User biography |
| `profile_image` | ImageField | User profile image |
| `website` | URLField | Personal website URL |
| `instagram_link` | URLField | Instagram profile URL |
| `x_link` | URLField | X profile URL |
| `git_link` | URLField | GitHub profile URL |
| `total_posts` | PositiveIntegerField | Total number of posts created |
| `total_views` | PositiveBigIntegerField | Total views received by the user's blogs |
| `total_likes` | PositiveBigIntegerField | Total likes received by the user's blogs |
| `is_approved_blogger` | BooleanField | Indicates whether the user is approved as a blogger |
| `created_at` | DateTimeField | Account creation timestamp |
| `updated_at` | DateTimeField | Last account update timestamp |
| `last_active_at` | DateTimeField | Last recorded user activity |
| `timezone` | CharField | User timezone preference |
| `language_preference` | CharField | Preferred interface language |

### Relationships

- A user can follow multiple users.
- A user can have multiple followers.
- A user can create multiple blogs.
- A user can write multiple comments.
- A user can bookmark multiple blogs.
- A user can like multiple blogs.

---

## 📝 Blog

The `Blog` model stores blog posts created by bloggers.

| Field | Type | Description |
|-------|------|-------------|
| `id` | BigAutoField | Primary key |
| `author` | ForeignKey | References the user who created the blog |
| `title` | CharField | Blog title |
| `title_bg_color` | CharField | Background color preference for the title |
| `slug` | SlugField | Unique URL-friendly identifier |
| `short_description` | TextField | Short description of the blog |
| `content` | TextField | Blog content stored as CKEditor HTML |
| `cover_image` | ImageField | Blog cover image |
| `keywords` | CharField | Keywords associated with the blog |
| `category` | CharField | Blog category |
| `likes` | ManyToManyField | Users who liked the blog |
| `nation` | CharField | Optional geographical targeting information |
| `status` | CharField | Blog publication status |
| `is_comments_enabled` | BooleanField | Enables or disables comments |
| `views` | IntegerField | Blog view count |
| `total_views` | PositiveBigIntegerField | Total recorded views |
| `total_likes` | PositiveBigIntegerField | Total recorded likes |
| `total_comments` | PositiveBigIntegerField | Total recorded comments |
| `total_bookmarks` | PositiveBigIntegerField | Total bookmarks |
| `published_at` | DateTimeField | Blog publication timestamp |
| `created_at` | DateTimeField | Blog creation timestamp |
| `updated_at` | DateTimeField | Last blog update timestamp |

### Relationships

- Each blog belongs to one user through `author`.
- A blog can have multiple comments.
- A blog can be liked by multiple users.
- A blog can be bookmarked by multiple users.
- A blog can have multiple view events.

### Blog Status

| Status | Description |
|--------|-------------|
| `DRAFT` | Blog is saved but not publicly published |
| `PUBLISHED` | Blog is published and available to readers |

---

## 🏷️ BlogKeyword

The `BlogKeyword` model stores unique keywords that can be associated with blog content.

| Field | Type | Description |
|-------|------|-------------|
| `id` | BigAutoField | Primary key |
| `name` | CharField | Unique keyword name |
| `created_at` | DateTimeField | Keyword creation timestamp |

---

## 💬 Comment

The `Comment` model stores comments submitted by users on blog posts.

| Field | Type | Description |
|-------|------|-------------|
| `id` | BigAutoField | Primary key |
| `blog` | ForeignKey | Blog associated with the comment |
| `author` | ForeignKey | User who submitted the comment |
| `content` | TextField | Comment content |
| `created_at` | DateTimeField | Comment creation timestamp |

### Relationships

- Each comment belongs to one blog.
- Each comment belongs to one user.
- A blog can contain multiple comments.
- Comments are ordered by newest first.

---

## 🔖 Bookmark

The `Bookmark` model stores blogs saved by users for later access.

| Field | Type | Description |
|-------|------|-------------|
| `user` | ForeignKey | User who created the bookmark |
| `blog` | ForeignKey | Blog that was bookmarked |
| `created_at` | DateTimeField | Bookmark creation timestamp |


---

## 🔗 Entity Relationships

The major database relationships can be summarized as follows:

```text
                         ┌──────────────┐
                         │     User     │
                         └──────┬───────┘
                                │
             ┌──────────────────┼──────────────────┐
             │                  │                  │
             ▼                  ▼                  ▼
        ┌─────────┐        ┌──────────┐      ┌──────────┐
        │  Blog   │        │ Comment  │      │ Bookmark │
        └────┬────┘        └──────────┘      └────┬─────┘
             │                                    │
       ┌─────┼─────┐                              │
       │     │     │                              │
       ▼     ▼     ▼                              ▼
    Comment Like  BlogView                       Blog
       │     │     │
       │     │     └─────────── Analytics
       │     │
       └─────┴──────────── User
````

---

# 🖥️ Project Screenshots

This section showcases the major interfaces and features implemented in the SmartBlogger — AI-Powered Blog Platform.

<table>
<tr>

<td width="50%" valign="top">

## 🔐 Account Recovery – Change Password

Allows users to securely change their account password after completing the required recovery process.

<img src="Project%20Screenshots/Account%20Recovery%20%E2%80%93%20Change%20Password.png" width="100%">

</td>

<td width="50%" valign="top">

## 🔑 Account Recovery – Forgot Password

Provides users with an account recovery option when they forget their password.

<img src="Project%20Screenshots/Account%20Recovery%20%E2%80%93%20Forgot%20Password.png" width="100%">

</td>

</tr>

<tr>

<td width="50%" valign="top">

## 👤 Account Recovery – Forgot Username

Allows users to recover their username through the account recovery system.

<img src="Project%20Screenshots/Account%20Recovery%20%E2%80%93%20Forgot%20Username.png" width="100%">

</td>

<td width="50%" valign="top">

## 🤖 AI Assistant – Content Suggestions

AI-powered assistance for generating or suggesting content ideas for bloggers.

<img src="Project%20Screenshots/AI%20Assistant%20Content%20Suggestions.png" width="100%">

</td>

</tr>



<tr>

<td width="50%" valign="top">

## 🔎 Blog Search and Filtering – Results

Displays search and filtering results based on the user's selected criteria.

<img src="Project%20Screenshots/Blog%20Search%20and%20Filtering1.png" width="100%">

</td>

<td width="50%" valign="top">

## 🔎 Blog Search and Filtering – Interface

Additional view of the blog discovery and filtering interface.

<img src="Project%20Screenshots/Blog%20Search%20and%20Filtering2.png" width="100%">

</td>

</tr>

<tr>

<td width="50%" valign="top">

## 🔎 Blog Search and Filtering – Content Discovery

Additional view demonstrating blog search and content filtering.

<img src="Project%20Screenshots/Blog%20Search%20and%20Filtering3.png" width="100%">

</td>

<td width="50%" valign="top">

## 👨‍💻 Blogger Profile Details

Displays detailed information about a blogger and their profile.

<img src="Project%20Screenshots/blogger%20profile%20details.png" width="100%">

</td>

</tr>

<tr>

<td width="50%" valign="top">

## 💬 Chitti AI Chatbot Integration

Integration of the Chitti AI chatbot into the blogging platform for conversational interaction.

<img src="Project%20Screenshots/Chitti%20AI%20Chatbot%20Integration.png" width="100%">

</td>

<td width="50%" valign="top">

## 💬 Chitti AI Chatbot – Interaction

Demonstrates the chatbot interaction interface and AI-generated responses.

<img src="Project%20Screenshots/Chitti%20AI%20Chatbot%20Integration1.png" width="100%">

</td>

</tr>

<tr>

<td width="50%" valign="top">

## 💬 Chitti AI Chatbot – Response Interface

Additional view of the Chitti AI chatbot functionality.

<img src="Project%20Screenshots/Chitti%20AI%20Chatbot%20Integration2.png" width="100%">

</td>

<td width="50%" valign="top">

## 💭 Comments Section

Allows readers to participate in discussions and interact with blog content through comments.

<img src="Project%20Screenshots/Comments%20Section.png" width="100%">

</td>

</tr>

<tr>

<td width="50%" valign="top">

## 📝 Create Account

Registration interface for creating a new user account on the platform.

<img src="Project%20Screenshots/create%20acc%20pg.png" width="100%">

</td>

<td width="50%" valign="top">

## 📝 Create Account – Additional View

Additional interface for the user registration and account creation process.

<img src="Project%20Screenshots/create%20acc%20pg2.png" width="100%">

</td>

</tr>

<tr>

<td width="50%" valign="top">

## ✍️ Create Blog Post – CKEditor

Provides bloggers with a rich text editor for creating and formatting blog posts using CKEditor.

<img src="Project%20Screenshots/Create%20Blog%20Post%20Interface%20with%20CKEditor.png" width="100%">

</td>

<td width="50%" valign="top">

## ✍️ Create Blog Post – CKEditor

Additional view of the blog creation and rich text editing interface.

<img src="Project%20Screenshots/Create%20Blog%20Post%20Interface%20with%20CKEditor1.png" width="100%">

</td>

</tr>

<tr>

<td width="50%" valign="top">

## ⚙️ Edit User Profile Settings

Allows users to update and manage their profile information and account settings.

<img src="Project%20Screenshots/Edit%20User%20Profile%20Settings.png" width="100%">

</td>

<td width="50%" valign="top">

## 🧠 First Blog Assistant Tool

Demonstrates the first AI-powered assistant tool designed to help bloggers with blog-related tasks.

<img src="Project%20Screenshots/First%20Blog%20Assistant%20Tool.png" width="100%">

</td>

</tr>

<tr>

<td width="50%" valign="top">

## 🧠 First Blog Assistant Tool – Additional View

Additional view of the first AI-powered blog assistant functionality.

<img src="Project%20Screenshots/First%20Blog%20Assistant%20Tool1.png" width="100%">

</td>

<td width="50%" valign="top">

## 👥 Followers and Following

Allows users to manage and view their followers and the users they follow.

<img src="Project%20Screenshots/followers%20and%20following.png" width="100%">

</td>

</tr>

<tr>

<td width="50%" valign="top">

## 📖 Individual Blog Post View

Displays an individual blog post with its content and reader interaction features.

<img src="Project%20Screenshots/Individual%20Blog%20Post%20View.png" width="100%">

</td>

<td width="50%" valign="top">

## 📖 Individual Blog Post View – Additional View

Additional view of an individual blog post and its associated content.

<img src="Project%20Screenshots/Individual%20Blog%20Post%20View1.png" width="100%">

</td>

</tr>

<tr>

<td width="50%" valign="top">

## 🔥 Latest Stories and Trending Section

Displays the latest stories and trending content to help users discover popular and recent blog posts.

<img src="Project%20Screenshots/Latest%20Stories%20and%20Trending%20Section.png" width="100%">

</td>

<td width="50%" valign="top">

## 👤 Public Author Profile

Public-facing author profile displaying information and content associated with a blogger.

<img src="Project%20Screenshots/Public%20Author%20Profile.png" width="100%">

</td>

</tr>

<tr>

<td width="50%" valign="top">

## 🔒 Security Settings and Email Verification

Provides security-related account settings and email verification functionality.

<img src="Project%20Screenshots/Security%20Settings%20and%20Email%20Verification.png" width="100%">

</td>

<td width="50%" valign="top">

## 🔒 Security Settings and Email Verification

Additional view of the account security and email verification features.

<img src="Project%20Screenshots/Security%20Settings%20and%20Email%20Verification1.png" width="100%">

</td>

</tr>

<tr>

<td width="50%" valign="top">

## 🏠 SmartBlogger Landing Page

Main landing page introducing the SmartBlogger platform and its core functionality.

<img src="Project%20Screenshots/SmartBlogger%20Landing%20Page.png" width="100%">

</td>

<td width="50%" valign="top">

## 🏠 SmartBlogger Landing Page – Features

Additional view highlighting the platform's features and user experience.

<img src="Project%20Screenshots/SmartBlogger%20Landing%20Page1.png" width="100%">

</td>

</tr>

<tr>

<td width="50%" valign="top">

## 🏠 SmartBlogger Landing Page – Additional View

Additional section of the SmartBlogger landing page.

<img src="Project%20Screenshots/SmartBlogger%20Landing%20Page2.png" width="100%">

</td>

<td width="50%" valign="top">

## 📊 User Analytics Dashboard

Centralized analytics dashboard providing insights into user engagement and platform activity.

<img src="Project%20Screenshots/User%20Analytics%20Dashboard.png" width="100%">

</td>

</tr>

<tr>

<td width="50%" valign="top">

## 📊 User Analytics Dashboard – Analytics View

Additional view of the analytics dashboard and user engagement information.

<img src="Project%20Screenshots/User%20Analytics%20Dashboard1.png" width="100%">

</td>

<td width="50%" valign="top">

## 🔖 User Bookmarks

Displays the user's saved or bookmarked blog content for quick access.

<img src="Project%20Screenshots/User%20Bookmarks%20Model.png" width="100%">

</td>

</tr>

<tr>

<td width="50%" valign="top">

## 📊 User Dashboard Overview

Provides users with a centralized dashboard for accessing account information, activity, and platform features.

<img src="Project%20Screenshots/User%20Dashboard%20Overview.png" width="100%">

</td>

<td width="50%" valign="top">

## 🔐 User Sign-In Page

Login interface allowing registered users to securely access their accounts.

<img src="Project%20Screenshots/User%20Sign-In%20Page.png" width="100%">

</td>

</tr>

<tr>

<td width="50%" valign="top">

## 📝 Your Blog

Displays the user's own blog content and provides access to their published posts.

<img src="Project%20Screenshots/your%20bolg.png" width="100%">

</td>

<td width="50%" valign="top">

</td>

</tr>

</table>

---

# 🛠 Technology Stack

| Category | Technology |
|----------|------------|
| Language | Python |
| Backend Framework | Django 6.0.1 |
| Frontend | HTML5, CSS3, JavaScript |
| Template Engine | Django Templates |
| Database | SQLite |
| ORM | Django ORM |
| Rich Text Editor | CKEditor |
| Image Processing | Pillow |
| Authentication | Django Authentication System |
| AI Processing | NLP-based Knowledge Retrieval |
| Web Search | External Web Search Integration |
| Analytics | Custom Engagement Tracking |
| Database Migrations | Django Migrations |
| Package Management | pip & `requirements.txt` |
| Development Server | Django Development Server |
| Version Control | Git & GitHub |

---

# ⚙️ Installation & Setup

Follow the steps below to run the SmartBlogger — AI-Powered Blog Platform locally.

## 1. Clone the Repository

Clone the project from GitHub:

```bash
git clone https://github.com/maazsiddiqui79/Smart_Blogging-Platform-FYP.git
````

Navigate to the project directory:

```bash
cd Smart_Blogging-Platform-FYP
```

## 2. Create a Virtual Environment

Create a Python virtual environment:

```bash
python -m venv venv
```

## 3. Activate the Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### macOS / Linux

```bash
source venv/bin/activate
```

## 4. Install Dependencies

Install all required Python packages from `requirements.txt`:

```bash
pip install -r requirements.txt
```

## 5. Apply Database Migrations

Run the following command to create and update the required database tables:

```bash
python manage.py migrate
```

## 6. Create a Superuser

To access the Django administration panel, create a superuser:

```bash
python manage.py createsuperuser
```

Enter the requested username, email address, and password.

## 7. Start the Development Server

Start the Django development server:

```bash
python manage.py runserver
```

## 8. Open the Application

Open your browser and visit:

```text
http://127.0.0.1:8000/
```

The SmartBlogger — AI-Powered Blog Platform should now be running locally.

## 9. 🛑 Stopping the Server

To stop the development server, press:
```text
CTRL + C
```

---

# 📂 Project Modules

- User Interface Module  
- Authentication Module  
- Blog Management Module  
- AI Chatbot Module  
- Knowledge Retrieval Module  
- External Search Module  
- Blog Engagement Tracking Module  
- Blog Analytics & Insights Module  

---

# 🚀 Future Enhancements

- Voice-based chatbot interaction  
- Multilingual chatbot support  
- AI-powered personalized blog recommendations  
- Predictive analytics for trending blog topics  
- AI-based blog summarization  
- Smart content suggestions for bloggers  

---

# 👥 Team Members

| Name | Role |
|------|------|
| **Maaz Siddiqui** | Project Lead / Frontend & Backend Developer |
| **Sufiyan Shaikh** | Backend Developer |
| **Awan Shaikh** | Report Coordinator |
| **Anas Shaikh** | Documentation Assistant |

### Project Lead

**Maaz Siddiqui**
- GitHub: [@maazsiddiqui79](https://github.com/maazsiddiqui79)
- Portfolio: [themaaz.online](https://www.themaaz.online/)
  
---

# 🎓 Project Information

**Project Type:** Final Year Diploma Project  
**Department:** Computer Engineering  
**Institution:** M.H. Saboo Siddik College  

---

# 📌 Project Status

**Status:** Completed

This project was developed as a academic Final Year Diploma Project in Computer Engineering.

---

## 📜 License

This project is licensed under the MIT License.

You are free to use, copy, modify, merge, publish, distribute, sublicense copies of the project, subject to the terms of the MIT License.

See the [LICENSE](LICENSE) file for the complete license.

---
