
from django.core.exceptions import ValidationError


def tank_level_validators(value):
    message = 'значение уровня танка должно быть от 1 до 10. Текущие значение: %(value)s'
    code = 'level_not_allowed'
    if not (1 <= value <= 10):
            raise ValidationError(message=message, code=code, params={'value': value})


class TankLevelValidator:
    message = 'значение уровня танка должно быть от 1 до 10. Текущие значение: %(value)s'
    code = 'level_not_allowed'

    def __init__(self, message=None, code=None):
        self.message = message or self.message
        self.code = code or self.code
        
    def __call__(self, value):
        if not (1 <= value <= 10):
            raise ValidationError(message=self.message, code=self.code, params={'value': value})
        
        
        
class ImageSizeValidator:
    message = 'не допустимый размер файла (%(width)sx%(height)s)'
    code = 'level_not_allowed'

    def __init__(self, width=1, height=1, message=None, code=None):
        self.message = message or self.message
        self.code = code or self.code
        self.width = width
        self.height = height
        
    def __call__(self, image):
        width = image.width
        height = image.height
        if self.width / self.height != width / height:
            raise ValidationError(message=self.message, code=self.code, params={'width': width, 'height': height})