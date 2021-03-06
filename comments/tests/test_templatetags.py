from django.test import TestCase
from django.template import Template, Context
from comments.templatetags.comments_extra import show_comments_form
from comments.forms import CommentsForm
from .test_base import CommentDataTestCase


class CommentExtraTestCase(CommentDataTestCase):
    def setUp(self):
        super().setUp()
        self.ctx = Context()

    def test_show_comment_form_with_invalid_form_data(self):
        template = Template(
            '{% load comments_extra %}'
            '{% show_comments_form post form %}'
        )

        invalid_data = {
            'email': 'invalid_email',

        }

        form = CommentsForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        context = Context(show_comments_form(self.ctx, self.post, form=form))
        expected_html = template.render(context)
