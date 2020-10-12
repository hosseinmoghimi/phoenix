from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import Blog,SiteMap
class SiteMapFeeder(Feed):
    # def __init__(self):
    #     self.objects=SiteMap.objects
    title = "خواف آنلاین"
    link = "/sitemap/"
    description = "نقشه سایت"
    
    def items(self):
        return SiteMap.objects.filter(active=True)

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.parent

    # item_link is only needed if Blog has no get_absolute_url method.
    def item_link(self, item):
        return item.url



class LatestEntriesFeed(Feed):
    title = "خواف آنلاین"
    link = "/feed/"
    description = "لیست آخرین اخبار سایت "

    def items(self):
        return Blog.objects.order_by('-id')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    # item_link is only needed if Blog has no get_absolute_url method.
    def item_link(self, item):
        return item.get_absolute_url()