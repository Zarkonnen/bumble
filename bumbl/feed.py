from django.utils.feedgenerator import Atom1Feed

class BumbleFeed(Atom1Feed):
    def add_item_elements(self, handler, item):
        super().add_item_elements(handler, item)
        if item['content'] is not None:
            handler.addQuickElement("content", item['content'], {"type": "html"})