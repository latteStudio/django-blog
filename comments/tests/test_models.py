from .test_base import CommentDataTestCase
from comments.models import Comments


class CommentModelTestCase(CommentDataTestCase):
    def setUp(self):
        super().setUp()
        self.comment = Comments.objects.create(
            name='user1',
            email='user1@a.com',
            text='content',
            post=self.post,
        )

    def test_str_repr(self):
        self.assertEqual(self.comment.__str__(), 'user1:content')

