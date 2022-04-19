from django.core.mail import send_mail


def send_activation_email(email, activation_code):
    activation_url = f'http://localhost:3000/api/v1/accounts/activate/{activation_code}/'
    message = f'''
              Thank you for signing up.
              Please, activate your account.
              Activation link: {activation_url}  
            '''
    send_mail(
        'Activate your account',
        message,
        'test@hahaton.kg',
        [email, ],
        fail_silently=False
    )

