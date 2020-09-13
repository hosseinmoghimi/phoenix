from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from .persian import PersianCalendar
# from xhtml2pdf import pisa
import qrcode
import qrcode.image.svg


from datetime import datetime
from datetime import timedelta
from openpyxl import Workbook
from django.http import HttpResponse


def get_qrcode(data,method=None):
    if method is None:
        method='basic'
    if method == 'basic':
        # Simple factory, just a set of rects.
        factory = qrcode.image.svg.SvgImage
    elif method == 'fragment':
        # Fragment factory (also just a set of rects)
        factory = qrcode.image.svg.SvgFragmentImage
    else:
        # Combined path factory, fixes white space that may occur when zooming
        factory = qrcode.image.svg.SvgPathImage

    img = qrcode.make(data=data, image_factory=factory)
    return img

# def render_to_pdf(template_src, context_dict={}):
#     template = get_template(template_src)
#     html  = template.render(context_dict)
#     result = BytesIO()
     
#     pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
#     if not pdf.err:
#         return HttpResponse(result.getvalue(), content_type='application/pdf')
#     return None