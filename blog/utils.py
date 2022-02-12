from django.utils.html import strip_tags
from haystack.utils import Highlighter as HaystackHighlighter
from rest_framework_extensions.key_constructor.bits import KeyBitBase
from django.core.cache import cache
from datetime import datetime


class UpdatedAtKeyBit(KeyBitBase):
    key = "updated_at"

    def get_data(self, params, view_instance, view_method, request, args, kwargs):
        value = cache.get(self.key, None)
        if not value:
            value = datetime.utcnow()
            cache.set(self.key, value=value)
        return str(value)


class Highlighter(HaystackHighlighter):
    """
    自定义关键词高亮器，不截断过短的文本（例如文章标题）
    """

    def highlight(self, text_block):
        self.text_block = strip_tags(text_block)
        highlight_locations = self.find_highlightable_words()
        start_offset, end_offset = self.find_window(highlight_locations)
        if len(text_block) < self.max_length:
            start_offset = 0
        return self.render_html(highlight_locations, start_offset, end_offset)
