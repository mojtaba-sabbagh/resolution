from django import http
from rest_framework import views
from . import models

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus.tables import Table, TableStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Image
from reportlab.lib.enums import TA_RIGHT

from jalali_date import date2jalali
from bidi.algorithm import get_display
import arabic_reshaper
from textwrap import wrap

import io
from pathlib import Path
import os


class PDFMaker(views.APIView):

    def get_object(self, pk):
        try:
            return models.Proceeding.objects.get(pk=pk)
        except models.Proceeding.DoesNotExist:
            raise http.Http404

    def get(self, request, pk):
        proceeding = self.get_object(pk)
        create_proceeding = CreateProceeding(proceeding=proceeding)
        return create_proceeding.get_response()


class CreateProceeding:

    def __init__(self, proceeding):
        self.proceeding = proceeding
        self.participant_p_line = 5
        self.spaces = '&nbsp;' * 30
        self.register_fonts()
        self.space_width = 1
        self.space_height = 10
        self.tableStyle = TableStyle([
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('FONTNAME', (0, 0), (-1, -1), 'Yekan'),
            ('ALIGNMENT', (0, 0), (-1, -1), 'CENTER'),
        ])

        self.stylesheet = Stylesheet()
        self.stories = []

        self.create_story()

    def get_response(self):
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        doc.build(self.stories)
        response = http.HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="{mealTime:} by student.pdf"'.format(mealTime='')
        response.write(buffer.getvalue())
        return response

    def create_story(self):
        self.add_title()
        self.add_under_title()
        self.create_space()
        self.add_resolution()
        self.create_space()
        self.create_space()
        self.add_signatures()

    @property
    def base_dir(self):
        return Path(__file__).resolve().parent

    @property
    def default_sign(self):
        return os.path.join(self.base_dir, 'assets/signatures/default.png')

    def arabic_reshaper(self, data):
        reshaped_text = arabic_reshaper.reshape(data)
        bidi_text = get_display(reshaped_text)
        return bidi_text

    def create_space(self):
        self.stories.append(Spacer(self.space_width, self.space_height))

    def register_fonts(self):
        pdfmetrics.registerFont(TTFont('Yekan', '../fonts/Yekan/Yekan.ttf'))
        pdfmetrics.registerFont(TTFont('Titr', '../fonts/Titr/titr.ttf'))

    def add_title(self):
        meeting = models.Meeting.objects.get(pk=self.proceeding.meeting.id)
        title = f"<b>صورتجلسه شماره {self.proceeding.proceeding_no} {meeting.meeting_name} به تاریخ {date2jalali(self.proceeding.pdate).strftime('%Y/%m/%d')}</b>"
        title = self.arabic_reshaper(title)
        self.stories.append(Paragraph(title, self.stylesheet.proceeding_title_style()))
        self.create_space()

    def add_under_title(self):
        under_title = f"این جلسه با حضور شرکت کنندگان زیر در ساعت {self.proceeding.ptime.strftime('%H:%M')} برگزار شد و مفاد ذیل به تصویب رسید."
        under_title = self.arabic_reshaper(under_title)
        self.stories.append(Paragraph(under_title, self.stylesheet.titr_text_style()))
        self.create_space()

    def get_participants(self):
        participants = []
        for employee in self.proceeding.participants.all():
            fullname = self.arabic_reshaper(f'{employee.stockholder.first_name} {employee.stockholder.last_name}')
            position = self.arabic_reshaper(employee.position)
            participant = models.Participant.objects.get(member=employee, proceeding=self.proceeding)
            if participant.is_signed:
                signature = os.path.join(self.base_dir, 'assets', employee.stockholder.signature.name)
            else:
                signature = self.default_sign
            participants.append({
                'fullname': fullname,
                'position': position,
                'signature': signature,
            })
        return participants

    def add_signatures(self):
        rows = []
        fullname, position, signature = [], [], []
        for i, participant in enumerate(self.get_participants()):
            fullname.append(Paragraph(participant['fullname'], self.stylesheet.participants_text_style()))
            position.append(Paragraph(participant['position'], self.stylesheet.participants_text_style()))
            if os.path.isdir(participant['signature']):
                signature_path = self.default_sign
            else:
                signature_path = participant['signature']
            signature.append(Image(open(signature_path, 'rb'), width=100, height=100, kind='proportional'))
            if (i + 1) % self.participant_p_line == 0:
                rows.append(fullname)
                rows.append(position)
                rows.append(signature)
                fullname, position, signature = [], [], []
        rows.append(fullname)
        rows.append(position)
        rows.append(signature)
        try:
            table = Table(rows, colWidths=130, rowHeights=10)
            table.setStyle(self.tableStyle)
            self.stories.append(table)
        except:
            pass

    def add_resolution(self):
        resolution = models.Resolution.objects.filter(proceeding=self.proceeding)
        resolution = sorted(resolution, key=lambda r: int(r.item_no))
        for res in resolution:
            act_text = f"{res.item_no}. {res.act_text}"
            wrapped_text = wrap(act_text, width=100)
            for line in wrapped_text:
                reshaped_text = self.arabic_reshaper(line)
                p = Paragraph(reshaped_text, self.stylesheet.arabic_text_style())
                self.stories.append(p)
            self.create_space()
        self.create_space()


class Stylesheet:

    def __init__(self):
        self.style = getSampleStyleSheet()

    def get_styles(self):
        return self.style

    def arabic_text_style(self):
        return ParagraphStyle(
            name='border',
            parent=self.style['Normal'],
            rightIndent=30,
            alignment=TA_RIGHT,
            fontName="Yekan",
            fontSize=9,
            leading=12,
            wordWrap='RTL',
            language='AR',
        )

    def participants_text_style(self):
        return ParagraphStyle(
            name='border',
            parent=self.style['Normal'],
            rightIndent=30,
            alignment=1,
            wordWrap=None,
            fontName="Yekan",
            fontSize=8,
        )

    def titr_text_style(self):
        return ParagraphStyle(
            name='border',
            parent=self.style['Normal'],
            spaceAfter=5,
            rightIndent=30,
            alignment=2,
            fontName="Titr"
        )

    def proceeding_title_style(self):
        return ParagraphStyle(
            name='border',
            parent=self.style['Normal'],
            spaceBefore=5,
            spaceAfter=15,
            alignment=1,
            fontName="Titr"
        )
