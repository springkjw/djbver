from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone

from djbver.db.models import GenericModel, GenericActiveModel
from djbver.core.validators.regex import phone_regex
from djbver.settings import djbver_settings


class SmsStatus(models.Choices):
    SUCCESS = "success"
    RESERVED = "reserved"
    SCHEDULED = "scheduled"
    FAIL = "fail"


class SmsHistory(GenericModel):
    phone = models.CharField(
        '전화번호',
        max_length=15,
        validators=[
            RegexValidator(regex=phone_regex, message="올바른 번호가 아닙니다", code='invalid_phone')
        ]
    )
    message = models.TextField('내용', null=True, blank=True)
    status = models.CharField('상태', max_length=20, choices=SmsStatus.choices, null=True, blank=True)

    class Meta:
        db_table = 'sms_histories'
        verbose_name = 'SMS 이력'
        verbose_name_plural = 'SMS 이력들'
    
    def __str__(self):
        return "{phone}[{status}]".format(
            phone=self.phone,
            status=self.status
        )


def minutes_hence():
    return timezone.now() + timezone.timedelta(minutes=djbver_settings.SMS_VERIFY_CODE_EXPIRE)


class SmsVerifyCode(GenericActiveModel):
    phone = models.CharField(
        '전화번호',
        max_length=15,
        validators=[
            RegexValidator(regex=phone_regex, message="올바른 번호가 아닙니다", code='invalid_phone')
        ]
    )
    code = models.CharField('인증코드', max_length=10)
    expire = models.DateTimeField('만료일', default=minutes_hence)

    class Meta:
        db_table = 'sms_verify_codes'
        unique_together = ['phone', 'code']
        verbose_name = 'SMS 인증코드'
        verbose_name_plural = 'SMS 인증코드들'

    @property
    def is_expire(self):
        return timezone.now() > self.expire

