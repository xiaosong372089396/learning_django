from django import template

register = template.Library()
@register.filter
def cut_url(img):
    try:
        url = '/static/userimg/' + str(img.name).split('/')[-1]
    except:
        url = '/static/userimg/IMG_0201.JPG'
    return url
