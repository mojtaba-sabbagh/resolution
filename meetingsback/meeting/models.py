from django.db import models
from django.contrib.auth.models import User
from jalali_date import date2jalali
# Create your models here.

class Stockholder(models.Model):
    GENDER_CHOICES = (
        ('M', 'مرد'),
        ('F', 'زن'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, default='M', choices=GENDER_CHOICES)
    birthday = models.DateField(blank=True, null=True)
    national_id = models.CharField(max_length=10, unique=True, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    mobile = models.CharField(max_length=11, blank=True, null=True)
    signature = models.FileField(upload_to='signatures/', max_length=254, blank=True, null=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    #class Meta:
        #abstract = True

class Student(models.Model):
    MAGHTA_CHOICES = (
        ('کارشناسی', 'کارشناسی'),
        ('کارشناسی ارشد', 'کارشناسی ارشد'),
        ('دکتری', 'دکتری')
    )
    stockholder = models.OneToOneField(Stockholder, on_delete=models.CASCADE)
    stdno = models.CharField(max_length=10, unique=True)
    major = models.CharField(max_length=255, blank=True, null=True)
    maghta = models.CharField(max_length=20, default='کارشناسی', choices=MAGHTA_CHOICES)
    
    def __str__(self):
        return f"{self.stdno} - {self.stockholder}"

class Employee(models.Model):
    TYPE_CHOICE = (
        ('کارمند', 'کارمند'),
        ('هیات علمی', 'هیات علمی'),
    )
    stockholder = models.OneToOneField(Stockholder, on_delete=models.CASCADE)
    employee_no = models.CharField(max_length=10, unique=True)
    position = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=20, default='کارمند', choices=TYPE_CHOICE)
    dep = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.employee_no} - {self.stockholder}"

class Meeting(models.Model):
    PERIOD_CHOICE = (
        ('روزانه', 'روزانه'),
        ('هفتگی', 'هفتگی'),
        ('دوهفتگی', 'هفتگی'),
        ('ماهیانه', 'ماهیانه'),
        ('غیرمشخص', 'غیرمشخص'),
    )
    meeting_name = models.CharField(max_length=255)
    period = models.CharField(max_length=255, blank=True, null=True, choices=PERIOD_CHOICE)
    members = models.ManyToManyField(Employee, through='Membership')
    creator = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

    def is_member(self, user):
        # check if 'user' is member of the meeting.
        for member in self.members.all():
            if member.stockholder.user.id == user:
                return True
        return False
    
    @staticmethod
    def meetings_user_belongs_to(user):
        meetings = []
        all_meetings = Meeting.objects.all()
        for meeting in all_meetings:
            if meeting.is_member(user):
                meetings.append(meeting.id)
        return Meeting.objects.filter(id__in=meetings)
    
    @staticmethod
    def meetings_user_created(user):
        return Meeting.objects.filter(creator=user)
    
    @staticmethod
    def meetings_user_belongs_to_or_created(user):
        q1 = Meeting.meetings_user_created(user)
        return q1.union(Meeting.meetings_user_belongs_to(user))

    def __str__(self):
        return self.meeting_name

class Membership(models.Model):
    ROLE_CHOICE = (
        ('عضو', 'عضو'),
        ('دبیر', 'دبیر'),
    )
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    role = models.CharField(max_length=64, choices=ROLE_CHOICE)

    def __str__(self):
        return f"{self.employee} - {self.role} {self.meeting}"

class Proceeding(models.Model):
    proceeding_no = models.CharField(max_length=255)
    pdate = models.DateField()
    ptime = models.TimeField(blank=True, null=True)
    loc = models.CharField(max_length=255, blank=True, null=True)
    participants =  models.ManyToManyField(Employee, through='Participant')
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    readonly = models.BooleanField(default=False)
    upload = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.meeting} - {self.proceeding_no} - {date2jalali(self.pdate).strftime('%Y/%m/%d')}"

class Participant(models.Model):
    proceeding = models.ForeignKey(Proceeding, on_delete=models.CASCADE)
    member = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date_signed = models.DateField(blank=True, null=True)
    is_signed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('proceeding', 'member')
        
    def __str__(self):
        return f"{self.proceeding}-{self.member}"
    
    @staticmethod
    def get_user_proceedings(user, sign=''):
        logged_user = User.objects.get(id=user)
        logged_stockholder = Stockholder.objects.get(user=logged_user)
        logged_employee = Employee.objects.get(stockholder=logged_stockholder)
        if sign == '':
            return Participant.objects.filter(member=logged_employee)
        elif sign == 'f':
            return Participant.objects.filter(member=logged_employee, is_signed=False)
        else: return Participant.objects.filter(member=logged_employee, is_signed=True)

    @staticmethod
    def get_proceedings_bysigned(user, sign):
        user_proceedings = [part.proceeding.id for part in Participant.get_user_proceedings(user, sign)]
        return Proceeding.objects.filter(id__in=user_proceedings)

class Resolution(models.Model):
    STOCKHOLDER_CHOICE = (
        ('0', 'انتخاب کنید'),
        ('دانشجو', 'دانشجو'),
        ('کارکنان', 'کارکنان'),
    )
    item_no = models.CharField(max_length=64)
    act_text = models.CharField(max_length=255)
    resolution_type = models.CharField(max_length=255, blank=True, null=True)
    result = models.BooleanField(default=True)
    proceeding = models.ForeignKey(Proceeding, on_delete=models.CASCADE)
    stockholder_type = models.CharField(max_length=64, choices=STOCKHOLDER_CHOICE, blank=True, null=True)
    stockholder = models.ForeignKey(Stockholder, on_delete=models.CASCADE,  blank=True, null=True)
    
    def __str__(self):
        return f"{self.item_no} - {self.proceeding}"

class ResolutionType(models.Model):
     resolution_type = models.CharField(max_length=255)
     def __str__(self):
        return self.resolution_type