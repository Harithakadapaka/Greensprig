from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from plants.models import Post, Category, Comment, Favorite, UserProfile
from plants.forms import PostForm, CommentForm, UserProfileForm, UserSignupForm


class CategoryModelTest(TestCase):
    def test_str(self):
        category = Category.objects.create(name="Spring", description="Spring season")
        self.assertEqual(str(category), "Spring")


class UserAuthTests(TestCase):
    def setUp(self):
        # Create a user matching your TC-001 precondition
        self.user = User.objects.create_user(
            username='Example1',
            email='Example123@gmail.com',
            password='password123'
        )

    def test_valid_login_redirects_to_dashboard(self):
        # POST to the login URL with valid credentials
        response = self.client.post(reverse('login'), {
            'username': 'Example1',
            'password': 'password123'
        })

        # Check for redirect (status code 302)
        self.assertEqual(response.status_code, 302)

        # Follow the redirect and check for welcome message
        response = self.client.get(response.url)
        self.assertContains(response, "Welcome")  # Adjust if your dashboard shows a different welcome message


class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.category = Category.objects.create(name="Winter")
        self.post = Post.objects.create(
            title='Test Post',
            content='Some content',
            author=self.user,
            categories=self.category  # FK assigned correctly
        )

    def test_str(self):
        self.assertEqual(str(self.post), "Test Post")

    def test_total_likes(self):
        self.assertEqual(self.post.total_likes, 0)
        self.post.likes.add(self.user)
        self.assertEqual(self.post.total_likes, 1)

    def test_post_comment_count(self):
        Comment.objects.create(post=self.post, author=self.user, content='Nice post!')
        Comment.objects.create(post=self.post, author=self.user, content='Thanks for sharing.')
        self.assertEqual(self.post.comments.count(), 2)


class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='commenter', password='12345')
        self.post = Post.objects.create(
            title='Post with Comment',
            content='Some content',
            author=self.user,
            categories=Category.objects.create(name="General")
        )
        self.comment = Comment.objects.create(post=self.post, author=self.user, content="Nice post!")

    def test_str(self):
        self.assertEqual(str(self.comment), "Nice post!")


class FavoriteModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='favuser', password='12345')
        self.post = Post.objects.create(
            title='Fav Post',
            content='Content',
            author=self.user,
            categories=Category.objects.create(name="FavCategory")
        )
        self.favorite = Favorite.objects.create(user=self.user, post=self.post)

    def test_str(self):
        self.assertIn(self.post.title, str(self.favorite))


class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='profileuser', password='testpass')

    def test_str(self):
        profile, created = UserProfile.objects.get_or_create(user=self.user, defaults={'bio': 'Hello world'})
        self.assertEqual(str(profile), self.user.username)


class PostFormTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Eco')

    def test_valid_form(self):
        form_data = {
            'title': 'A title',
            'content': 'Some content',
            'categories': self.category.pk,
            'tags': 'green,eco',
        }
        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {
            'title': '',  # missing title makes form invalid
            'content': 'Content without title',
            'categories': self.category.pk,
        }
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())


class CommentFormTest(TestCase):
    def test_valid_form(self):
        form = CommentForm(data={'content': 'This is a comment'})
        self.assertTrue(form.is_valid())


class UserProfileFormTest(TestCase):
    def test_valid_form(self):
        form = UserProfileForm(data={'bio': 'Some bio'})
        self.assertTrue(form.is_valid())


class UserSignupFormTest(TestCase):
    def test_password_mismatch(self):
        form = UserSignupForm(data={
            'username': 'newuser', 'email': 'a@a.com', 'password': 'pass1', 'confirm_password': 'pass2'
        })
        self.assertFalse(form.is_valid())

    def test_email_uniqueness(self):
        User.objects.create_user(username='existing', email='taken@a.com', password='123')
        form = UserSignupForm(data={
            'username': 'newuser', 'email': 'taken@a.com', 'password': '123', 'confirm_password': '123'
        })
        self.assertFalse(form.is_valid())


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='user', password='pass')
        self.category = Category.objects.create(name='TestCat')
        self.post = Post.objects.create(
            title='Title',
            content='Content',
            author=self.user,
            categories=self.category
        )
        self.comment = Comment.objects.create(post=self.post, author=self.user, content="Test Comment")

    def test_home_view(self):
        self.client.login(username='user', password='pass')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_post_detail_view(self):
        self.client.login(username='user', password='pass')
        response = self.client.get(reverse('post_detail', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)

    def test_create_post_view(self):
        self.client.login(username='user', password='pass')
        response = self.client.post(reverse('create_post'), {
            'title': 'New Post',
            'content': 'Some text',
            'categories': self.category.id,
            'tags': 'test',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success

    def test_edit_post_view(self):
        self.client.login(username='user', password='pass')
        response = self.client.post(reverse('edit_post', args=[self.post.pk]), {
            'title': 'Updated',
            'content': 'Updated content',
            'categories': self.category.id,
            'tags': 'test',
        })
        self.assertEqual(response.status_code, 302)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated')

    def test_delete_post_view(self):
        self.client.login(username='user', password='pass')
        response = self.client.post(reverse('delete_post', args=[self.post.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())

    def test_like_post_view(self):
        self.client.login(username='user', password='pass')
        response = self.client.get(reverse('like_post', args=[self.post.pk]))
        self.assertEqual(response.status_code, 302)

    def test_toggle_favorite(self):
        self.client.login(username='user', password='pass')
        response = self.client.get(reverse('toggle_favorite', args=[self.post.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Favorite.objects.filter(user=self.user, post=self.post).exists())

    def test_add_comment_view(self):
        self.client.login(username='user', password='pass')
        response = self.client.post(reverse('add_comment', args=[self.post.pk]), {
            'content': 'Nice post!'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Comment.objects.filter(content='Nice post!').exists())

    def test_signup_view(self):
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'email': 'new@a.com',
            'password': 'pass1234',
            'confirm_password': 'pass1234'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_educational_resources_view(self):
        response = self.client.get(reverse('educational_resources'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'educational_resources.html')

    def test_create_post_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('create_post'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('create_post')}")


class ExtendedFeatureTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='extendeduser', password='pass')
        self.category = Category.objects.create(name='ExtendedCat')
        self.post = Post.objects.create(
            title='Tagged Post',
            content='Content',
            author=self.user,
            categories=self.category
        )
        self.post.tags.add('eco', 'green')

    def test_profile_edit_view(self):
        self.client.login(username='extendeduser', password='pass')
        response = self.client.post(reverse('profile'), {
            'bio': 'Updated bio'
        })
        self.assertEqual(response.status_code, 302)
        profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(profile.bio, 'Updated bio')

    def test_tagged_posts_view(self):
        response = self.client.get(reverse('tagged_posts', args=['eco']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Tagged Post')

    def test_search_results(self):
        self.client.force_login(self.user)  # Ensure user is logged in

        Post.objects.create(
            title='Unique Search Title',
            content='This is searchable content.',
            author=self.user
        )

        response = self.client.get(reverse('home'), {'q': 'Unique'})
        self.assertContains(response, 'Unique Search Title')

    def test_home_pagination(self):
        for i in range(15):
            Post.objects.create(
                title=f'Post {i}',
                content='Content',
                author=self.user,
                categories=self.category
            )
        response = self.client.get(reverse('home'), {'page': 2})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Post')

    def test_valid_image_upload_on_post(self):
        self.client.login(username='extendeduser', password='pass')

        with open('plants/tests/test_image.jpg', 'rb') as img:
            image = SimpleUploadedFile('test_image.jpg', img.read(), content_type='image/jpeg')

        response = self.client.post(reverse('create_post'), {
            'title': 'Image Post',
            'content': 'Post with image',
            'categories': [self.category.pk],  # Important: as a list
            'image': image,
            'tags': 'green',
        })

        # Debug print
        if response.status_code != 302:
         print("Form errors:", response.context['form'].errors)

        self.assertEqual(response.status_code, 302)

    def test_invalid_image_upload_on_post(self):
        self.client.login(username='extendeduser', password='pass')
        invalid_file = SimpleUploadedFile(
            name='notimage.txt',
            content=b'This is not an image',
            content_type='text/plain'
        )
        response = self.client.post(reverse('create_post'), {
            'title': 'Bad Image',
            'content': 'This should fail',
            'categories': self.category.id,
            'image': invalid_file
        })
        self.assertEqual(response.status_code, 200)  # form error re-renders page
        self.assertFormError(response, 'form', 'image', 'Upload a valid image. The file you uploaded was either not an image or a corrupted image.')


