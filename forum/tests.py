import datetime
from django.test import TestCase
from django.utils import timezone
from .models import ForumPost, ForumUser


class ForumPostModelTests(TestCase):
    time = timezone.now()
    test_user = ForumUser(username="testuser", password="testpass", email="test@example.com", rank="user", ban=time)

    def test_get_title_no_title_short_content(self):
        """
        get_title should be the same as content when content length is below 100
        """
        short_post = ForumPost(sender=self.test_user, timestamp=self.time, content="Short content, len()<100")
        self.assertEqual(short_post.get_title(), "Short content, len()<100")
    
    def test_get_title_no_title_long_content(self):
        """
        get_title should be the first 100 characters with three dots after when content length is above 100
        """
        long_post = ForumPost(sender=self.test_user, timestamp=self.time, content="Content content, len()>100 foobar foo foo foobar barbar foofoofoo barfoo foo bar something something this part should cut off")
        self.assertEqual(long_post.get_title(), "Content content, len()>100 foobar foo foo foobar barbar foofoofoo barfoo foo bar something something...")
    
    def test_get_title_no_title_100char_content(self):
        """
        get_title should be the same as content when content length is 100
        """
        hundred_long_post = ForumPost(sender=self.test_user, timestamp=self.time, content="Content content, len()>100 foobar foo foo foobar barbar foofoofoo barfoo foo bar something something")
        self.assertEqual(hundred_long_post.get_title(), "Content content, len()>100 foobar foo foo foobar barbar foofoofoo barfoo foo bar something something")
    
    def test_get_title_with_title(self):
        """
        get_title should be the same as the title when given
        """
        short_post = ForumPost(sender=self.test_user, timestamp=self.time, content="Some content", title="Post title")
        self.assertEqual(short_post.get_title(), "Post title")
