from django.core.exceptions import ValidationError


class IsCapitalValidator:
    def validate(self, password, user=None):
        if not password[0].isupper():
            raise ValidationError(
                'первый стмвол пароля должен быть в верхнем регистре',
                code='firs_digit_capital',
            )
            
    def get_help_text(self):
        return 'первый стмвол пароля должен быть в верхнем регистре'