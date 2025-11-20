import datetime
import logging

from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from .models import ForumPost, ForumReply
from .util import validators
# pylint: disable=W0105

"""
# Fix for OWASP Top 10 - A09:2021–Security Logging and Monitoring Failures; high value transactions were not logged making suspicious activity virtually invisible for system admins
# Remove the comment symbols preceeding lines where LOGGER is mentioned to implement
# Use the replace feature of your IDE to replace "#LOGGER" with "LOGGER"
"""
LOGGER = logging.getLogger(__name__)

def index(request):
    post_list = ForumPost.objects.all()
    return render(
        request,
        "forum/index.html",
        {
            "post_list": post_list,
            "user": request.user
        }
    )


def login(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            #LOGGER.info("An already logged in user %s attempted to log in from %s", str(request.user), request.META.get("REMOTE_ADDR", "Unknown IP"))
            return redirect(request.GET.get("next", "/"))
        return render(
            request,
            "forum/login.html",
            {
                "redirect": request.GET.get("next", "/"),
                "referer": request.META.get("HTTP_REFERER", "/"),
                "errormessage": ""
            }
        )
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            #LOGGER.info("User %s logged in from %s", str(user), request.META.get("REMOTE_ADDR", "Unknown IP"))
            return redirect(request.GET.get("next", "/"))
        #LOGGER.warning("Failed login attempt from %s", request.META.get("REMOTE_ADDR", "Unknown IP"))
        return render(
            request,
            "forum/login.html",
            {
                "redirect": request.GET.get("next", "/"),
                "referer": request.META.get("HTTP_REFERER", "/"),
                "errormessage": "Invalid username or password!"
            }
        )
    #LOGGER.warning("An unsupported HTTP method was used from %s", request.META.get("REMOTE_ADDR", "Unknown IP"))
    return HttpResponse(content='<h1>405 Only POST and GET methods are supported!</h1><a href="/">Main page</a>', status=405)


def register(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            #LOGGER.info("An already logged in user %s attempted to register from %s", str(request.user), request.META.get("REMOTE_ADDR", "Unknown IP"))
            return redirect(request.GET.get("next", "/"))
        return render(
            request,
            "forum/register.html",
            {
                "redirect": request.GET.get("next", "/"),
                "referer": request.META.get("HTTP_REFERER", "/"),
                "previous_username": "",
                "previous_email": "",
                "errormessage": ""
            }
        )
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password_confirmation = request.POST.get("confirmpassword")

        if password != password_confirmation:
            return render(
                request,
                "forum/register.html",
                {
                    "redirect": request.GET.get("next", "/"),
                    "referer": request.META.get("HTTP_REFERER", "/"),
                    "previous_username": username,
                    "previous_email": email,
                    "errormessage": "Password and password confirmation don't match!"
                }
            )

        user = User(username=username, email=email, password=password)
        """
        # Fix for OWASP Top 10 - A07:2021-Identification and Authentication Failures; users could have used short, common, and purely numeric passwords
        # Remove triple quotes around this block to implement
        try:
            password_validation.validate_password(password, user)
        except ValidationError as err:
            return render(
                request,
                "forum/register.html",
                {
                    "redirect": request.GET.get("next", "/"),
                    "referer": request.META.get("HTTP_REFERER", "/"),
                    "previous_username": username,
                    "previous_email": email,
                    "errormessage": "",
                    "errorlist": err
                }
            )
        """
        try:
            user.save()
            #LOGGER.info("New user %s registered from %s", str(user), request.META.get("REMOTE_ADDR", "Unknown IP"))
        except IntegrityError:
            return render(
                request,
                "forum/register.html",
                {
                    "redirect": request.GET.get("next", "/"),
                    "referer": request.META.get("HTTP_REFERER", "/"),
                    "previous_username": username,
                    "previous_email": email,
                    "errormessage": "Username was already taken or username or email fields contain invalid characters. Please only use characters from A-Z, a-z, 0-9, _, @, +, ., and -"
                }
            )
        auth.login(request, user)
        #LOGGER.info("New user %s logged in from %s", str(user), request.META.get("REMOTE_ADDR", "Unknown IP"))
        return redirect(request.GET.get("next", "/"))
    #LOGGER.warning("An unsupported HTTP method was used from %s", request.META.get("REMOTE_ADDR", "Unknown IP"))
    return HttpResponse(content='<h1>405 Only POST and GET methods are supported!</h1><a href="/">Main page</a>', status=405)


def logout(request):
    if request.user.is_authenticated:
        #LOGGER.info("User %s is logging out from %s", str(request.user), request.META.get("REMOTE_ADDR", "Unknown IP"))
        auth.logout(request)
        #LOGGER.info("Logged out")
        return render(
            request,
            "forum/logout.html",
            {}
        )
    return redirect("/")


def write_post(request, post_id=0, edit_mode=False):
    if request.user.is_authenticated:
        previous_content = ""
        previous_title = ""
        forum_post = None
        if edit_mode:
            forum_post = get_object_or_404(ForumPost, pk=post_id)
            """
            # Fix for OWASP Top 10 - 2021 A01:2021-Broken Access Control; users were able to edit posts with any logged in account
            # Remove triple quotes around this block to implement
            if request.user != forum_post.sender:
                LOGGER.warning("Unauthorized post edit attempt on post %s by %s from %s", forum_post.pk, str(request.user), request.META.get("REMOTE_ADDR", "Unknown IP"))
                return HttpResponse(content='<h1>403 Forbidden</h1><a href="/">Main page</a>', status=403)
            """
            previous_content = forum_post.content
            previous_title = forum_post.title

        if request.method == "GET":
            return render(
                request,
                "forum/compose.html",
                {
                    "user": request.user,
                    "previous_title": previous_title,
                    "previous_content": previous_content,
                    "edit_mode": edit_mode
                }
            )
        if request.method == "POST":
            title = request.POST.get("title")
            content = request.POST.get("text")

            title_length = validators.len_utf16(title)
            content_length = validators.len_utf16(content)
            if content_length < 20 or content_length > 5000 or title_length > 100:
                return render(
                    request,
                    "forum/compose.html",
                    {
                        "errormessage": "Invalid post content! Post must be between 20 and 5000 characters!",
                        "user": request.user,
                        "previous_title": title,
                        "previous_content": content,
                        "edit_mode": edit_mode
                    }
                )
            if not edit_mode:
                forum_post = ForumPost(
                    sender=request.user,
                    timestamp=datetime.datetime.now(),
                    content=content,
                    title=title
                )
                #LOGGER.info("New post %s primed by %s from %s", forum_post.pk, str(request.user), request.META.get("REMOTE_ADDR", "Unknown IP"))
            else:
                forum_post.edit_post(content, title)
                #LOGGER.info("Post %s edit primed by %s from %s", forum_post.pk, str(request.user), request.META.get("REMOTE_ADDR", "Unknown IP"))
            forum_post.save()
            #LOGGER.info("Post %s saved", forum_post.pk)
            return redirect(f"/post/{forum_post.pk}/")
        #LOGGER.warning("An unsupported HTTP method was used from %s", request.META.get("REMOTE_ADDR", "Unknown IP"))
        return HttpResponse(content='<h1>405 Only POST and GET methods are supported!</h1><a href="/">Main page</a>', status=405)
    if edit_mode:
        return redirect(f"/login/?next=/post/{post_id}/edit/")
    return redirect("/login/?next=/post/")


def view_post(request, post_id):
    post = get_object_or_404(ForumPost, pk=post_id)
    reply_list = ForumReply.objects.filter(parent=post)

    if request.method == "GET":
        return render(
            request,
            "forum/post.html",
            {
                "post": post,
                "user": request.user,
                "reply_list": reply_list
            }
        )
    if request.method == "POST":
        if not request.user.is_authenticated:
            #LOGGER.warning("An anonymous user attempted to add a reply to post %s from %s", post.pk, request.META.get("REMOTE_ADDR", "Unknown IP"))
            return HttpResponse(content='<h1>403 Forbidden</h1><a href="/">Main page</a>', status=403)
        reply_content = request.POST.get("reply_text")
        
        reply_length = validators.len_utf16(reply_content)
        if reply_length > 2 and reply_length <= 1000:
            reply = ForumReply(
                sender=request.user,
                parent=post,
                timestamp=datetime.datetime.now(),
                content=reply_content
            )
            reply.save()
            #LOGGER.info("Reply %s to post %s added by %s from %s", reply.pk, post.pk, str(request.user), request.META.get("REMOTE_ADDR", "Unknown IP"))
        return render(
                request,
                "forum/post.html",
                {
                    "post": post,
                    "user": request.user,
                    "reply_list": reply_list
                }
            )
    #LOGGER.warning("An unsupported HTTP method was used from %s", request.META.get("REMOTE_ADDR", "Unknown IP"))
    return HttpResponse(content='<h1>405 Only POST and GET methods are supported!</h1><a href="/">Main page</a>', status=405)


def search(request):
    number_of_posts = -1
    number_of_replies = -1
    if request.method == "GET":
        return render(
            request,
            "forum/search.html",
            {
                "post_amount": number_of_posts,
                "reply_amount": number_of_replies,
                "post_results": None,
                "reply_results": None
            }
        )
    if request.method == "POST":
        search_string = request.POST.get("search")
        
        search_string_length = validators.len_utf16(search_string)
        if search_string_length < 2 or search_string_length > 512:
            return render(
                request,
                "forum/search.html",
                {
                    "post_amount": number_of_posts,
                    "reply_amount": number_of_replies,
                    "post_results": None,
                    "reply_results": None
                }
            )
        """
        # Fix for OWASP Top 10 - 2021 A03:2021-Injection; users were able to inject SQL queries within search strings to obtain some private user information
        # Remove triple quotes around this block and comment out the following try-except statement to implement
        post_results = ForumPost.objects.filter(content__icontains=search_string)
        reply_results = ForumReply.objects.filter(content__icontains=search_string)
        number_of_posts = len(post_results)
        number_of_replies = len(reply_results)
        return render(
            request,
            "forum/search.html",
            {
                "post_amount": number_of_posts,
                "reply_amount": number_of_replies,
                "post_results": post_results,
                "reply_results": reply_results
            }
        )
        """
        #"""
        try:
            post_results = ForumPost.objects.raw("SELECT * FROM forum_forumpost WHERE content LIKE \'%%" + search_string + "%%\'")
            reply_results = ForumReply.objects.raw("SELECT * FROM forum_forumreply WHERE content LIKE \'%%" + search_string + "%%\'")
            number_of_posts = len(post_results)
            number_of_replies = len(reply_results)
            return render(
                request,
                "forum/search.html",
                {
                    "post_amount": number_of_posts,
                    "reply_amount": number_of_replies,
                    "post_results": post_results,
                    "reply_results": reply_results
                }
            )
        except Exception as err:
            return render(
                request,
                "forum/search.html",
                {
                    "post_amount": 0,
                    "reply_amount": 0,
                    "post_results": None,
                    "reply_results": None
                }
            )
        #"""
    #LOGGER.warning("An unsupported HTTP method was used from %s", request.META.get("REMOTE_ADDR", "Unknown IP"))
    return HttpResponse(content='<h1>405 Only POST and GET methods are supported!</h1><a href="/">Main page</a>', status=405)
