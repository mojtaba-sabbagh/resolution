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
from reportlab.lib.enums import TA_JUSTIFY

from jalali_date import date2jalali
from bidi.algorithm import get_display
import arabic_reshaper
from textwrap import wrap

import io
from pathlib import Path
import os
import yaml


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
        with open(os.path.join(self.base_dir, 'config/pdf_config.yml'), 'r') as file:
            self.config = yaml.safe_load(file)

        self.proceeding = proceeding
        self.register_fonts()
        self.tableStyle = TableStyle([
            ('FONTSIZE', (0, 0), (-1, -1), self.config['table']['font_size']),
            ('FONTNAME', (0, 0), (-1, -1), self.config['table']['font_name']),
            ('ALIGNMENT', (0, 0), (-1, -1), self.config['table']['alignment']),
        ])

        self.stylesheet = Stylesheet()
        self.stories = []

        self.create_story()

    def get_response(self):
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=self.config['page_margin']['right_margin'],
            leftMargin=self.config['page_margin']['left_margin'],
            topMargin=self.config['page_margin']['top_margin'],
            bottomMargin=self.config['page_margin']['bottom_margin']
        )
        doc.build(self.stories)
        response = http.HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="{mealTime:} by student.pdf"'.format(mealTime='')
        response.write(buffer.getvalue())
        return response

    def create_story(self):
        self.add_proceed_number()
        self.add_date()
        self.add_attached()
        self.create_space()
        self.create_space()
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
        self.stories.append(Spacer(self.config['space']['width'], self.config['space']['height']))

    def register_fonts(self):
        pdfmetrics.registerFont(TTFont('Yekan', '../fonts/Yekan/Yekan.ttf'))
        pdfmetrics.registerFont(TTFont('Titr', '../fonts/Titr/titr.ttf'))

    def add_proceed_number(self):
        number = self.proceeding.proceeding_no
        number = self.arabic_reshaper(number)
        self.stories.append(Paragraph(number, self.stylesheet.attached_style()))

    def add_date(self):
        date = date2jalali(self.proceeding.pdate).strftime('%Y/%m/%d')
        date = self.arabic_reshaper(date)
        self.stories.append(Paragraph(date, self.stylesheet.attached_style()))

    def add_attached(self):
        attached = self.proceeding.upload
        if attached is None or len(attached) == 0:
            attached = self.arabic_reshaper('ندارد')
        else:
            attached = self.arabic_reshaper('دارد')
        self.stories.append(Paragraph(attached, self.stylesheet.attached_style()))

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
            signature.append(
                Image(
                    open(signature_path, 'rb'),
                    width=self.config['signature']['width'],
                    height=self.config['signature']['height'],
                    kind='proportional'
                )
            )
            if (i + 1) % self.config['participant_p_line'] == 0:
                rows.append(fullname)
                rows.append(position)
                rows.append(signature)
                fullname, position, signature = [], [], []
        rows.append(fullname)
        rows.append(position)
        rows.append(signature)
        try:
            table = Table(
                rows,
                colWidths=self.config['table']['col_width'],
                rowHeights=self.config['table']['row_height']
            )
            table.setStyle(self.tableStyle)
            self.stories.append(table)
        except:
            pass

    def add_resolution(self):
        resolution = models.Resolution.objects.filter(proceeding=self.proceeding)
        resolution = sorted(resolution, key=lambda r: int(r.item_no))
        for res in resolution:
            act_text = f"{res.item_no}. {res.act_text}"
            wrapped_text = wrap(act_text, width=self.config['wrap_width'])
            for line in wrapped_text:
                reshaped_text = self.arabic_reshaper(line)
                p = Paragraph(reshaped_text, self.stylesheet.arabic_text_style())
                self.stories.append(p)
            self.create_space()
        self.create_space()


class Stylesheet:

    def __init__(self):
        with open(os.path.join(Path(__file__).resolve().parent, 'config/pdf_style.yml'), 'r') as file:
            self.config = yaml.safe_load(file)

        self.style = getSampleStyleSheet()

    def arabic_text_style(self):
        style = self.config['arabic_text_style']
        return ParagraphStyle(
            name=style['name'],
            parent=self.style['Normal'],
            rightIndent=style['rightIndent'],
            alignment=TA_JUSTIFY,
            fontName=style['fontName'],
            fontSize=style['fontSize'],
            leading=style['leading'],
            wordWrap=style['wordWrap'],
            language=style['language'],
        )

    def participants_text_style(self):
        style = self.config['participants_text_style']
        return ParagraphStyle(
            name=style['name'],
            parent=self.style['Normal'],
            rightIndent=style['rightIndent'],
            alignment=style['alignment'],
            wordWrap=None,
            fontName=style['fontName'],
            fontSize=style['fontSize'],
        )

    def titr_text_style(self):
        style = self.config['titr_text_style']
        return ParagraphStyle(
            name=style['name'],
            parent=self.style['Normal'],
            spaceAfter=style['spaceAfter'],
            rightIndent=style['rightIndent'],
            alignment=style['alignment'],
            fontName=style['fontName']
        )

    def proceeding_title_style(self):
        style = self.config['proceeding_title_style']
        return ParagraphStyle(
            name=style['name'],
            parent=self.style['Normal'],
            spaceBefore=style['spaceBefore'],
            spaceAfter=style['spaceAfter'],
            alignment=style['alignment'],
            fontName=style['fontName']
        )

    def attached_style(self):
        style = self.config['attached_style']
        return ParagraphStyle(
            name=style['name'],
            parent=self.style['Normal'],
            spaceBefore=style['spaceBefore'],
            fontSize=style['fontSize'],
            alignment=style['alignment'],
            fontName=style['fontName']
        )
