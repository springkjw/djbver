from django.utils.translation import gettext_lazy as _


class BaseSMS:
    HOST = None

    def clean_number(self, phone) -> str:
        phone = phone.replace('-', '')
        if not phone.startswith('0'):
            phone = '0{}'.format(phone)
        return phone
