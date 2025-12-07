from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags


def send_email(subject, template_name, context, recipient_list):
    """
    Send email using HTML template
    """
    html_content = render_to_string(template_name, context)
    text_content = strip_tags(html_content)
    
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=recipient_list
    )
    
    email.attach_alternative(html_content, "text/html")
    
    try:
        email.send()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def send_reservation_email(reservation):
    """
    Send reservation confirmation email
    """
    subject = f'Bicycle Reservation Confirmed - {reservation.bicycle.name}'
    context = {
        'reservation': reservation,
        'site_url': settings.SITE_URL,
        'site_name': settings.SITE_NAME,
    }
    
    return send_email(
        subject=subject,
        template_name='emails/reservation_confirmation.html',
        context=context,
        recipient_list=[reservation.user.email]
    )


def send_rental_start_email(rental):
    """
    Send rental start notification email
    """
    subject = f'Rental Started - {rental.bicycle.name}'
    context = {
        'rental': rental,
        'site_url': settings.SITE_URL,
        'site_name': settings.SITE_NAME,
    }
    
    return send_email(
        subject=subject,
        template_name='emails/rental_start.html',
        context=context,
        recipient_list=[rental.user.email]
    )


def send_rental_end_email(rental):
    """
    Send rental end notification email
    """
    subject = f'Rental Completed - {rental.bicycle.name}'
    context = {
        'rental': rental,
        'site_url': settings.SITE_URL,
        'site_name': settings.SITE_NAME,
    }
    
    return send_email(
        subject=subject,
        template_name='emails/rental_end.html',
        context=context,
        recipient_list=[rental.user.email]
    )


def send_overdue_reminder_email(rental):
    """
    Send overdue rental reminder email
    """
    subject = f'Overdue Rental Reminder - {rental.bicycle.name}'
    context = {
        'rental': rental,
        'site_url': settings.SITE_URL,
        'site_name': settings.SITE_NAME,
    }
    
    return send_email(
        subject=subject,
        template_name='emails/overdue_reminder.html',
        context=context,
        recipient_list=[rental.user.email]
    )