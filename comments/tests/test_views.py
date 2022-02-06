from django.urls import reverse
from .test_base import CommentDataTestCase
from ..models import Comments


class CommentViewTestCase(CommentDataTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('comments:comments', kwargs={'post_pk': self.post.pk})

    def test_invalid_comment(self):
        invalid_data = {
            'email': 'invalid_mail',
        }

        res = self.client.post(self.url, invalid_data)
        self.assertTemplateUsed(res, 'comments/preview.html')
        self.assertIn('post', res.context)
        self.assertIn('form', res.context)
        form = res.context['form']
        for field_name, errors in form.errors.items():
            for err in errors:
                self.assertContains(res, err)
        self.assertContains(res, '评论发表失败')

    def test_valid_comment(self):
        valid_data = {
            'name': 'user1',
            'email': 'user1@a.com',
            'text': 'content',
            'post': self.post,
        }
        res = self.client.post(self.url, valid_data, follow=True)
        self.assertRedirects(res, self.post.get_absolute_url())
        self.assertContains(res, '评论发表成功')
        self.assertEqual(Comments.objects.count(), 1)
        comment = Comments.objects.first()
        self.assertEqual(comment.name, valid_data['name'])
        self.assertEqual(comment.text, valid_data['text'])


