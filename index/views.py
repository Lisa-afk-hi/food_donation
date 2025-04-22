from django.shortcuts import render, redirect
from .models import Contact, Join
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.conf import settings
from twilio.rest import Client  # Added missing import for Twilio API

def index(request):
    return render(request, 'index.html')

def reciever(request):
    return render(request, 'receiver.html')

def donate(request):
    errors = {}
    form_data = {}

    if request.method == 'POST':
        # Get form data
        form_data = {
            'name': request.POST.get('name', '').strip(),
            'email': request.POST.get('email', '').strip(),
            'phone': request.POST.get('phone', '').strip(),
            'donation_type': request.POST.get('donation_type', ''),
            'contact_method': request.POST.get('contact_method', ''),
            'subject': request.POST.get('subject', '').strip(),
            'message': request.POST.get('message', '').strip(),
        }

        # Validation
        if not form_data['name']:
            errors['name'] = 'Name is required'
        elif any(char.isdigit() for char in form_data['name']):
            errors['name'] = 'Name cannot contain numbers'
            
        if not form_data['email']:
            errors['email'] = 'Email is required'
        else:
            try:
                validate_email(form_data['email'])
            except ValidationError:
                errors['email'] = 'Invalid email address'
                
        if not form_data['phone']:
            errors['phone'] = 'Phone number is required'
        elif not form_data['phone'].isdigit():
            errors['phone'] = 'Phone must contain only digits'
            
        if not form_data['donation_type']:
            errors['donation_type'] = 'Please select donation type'
            
        if not form_data['contact_method']:
            errors['contact_method'] = 'Please select contact method'
            
        if not form_data['subject']:
            errors['subject'] = 'Subject is required'
        elif len(form_data['subject']) < 5:
            errors['subject'] = 'Subject must be at least 5 characters'
            
        if not form_data['message']:
            errors['message'] = 'Message is required'
        elif len(form_data['message']) < 10:
            errors['message'] = 'Message must be at least 10 characters'

        if errors:
            for error in errors.values():
                messages.error(request, error)
            return render(request, 'donate.html', {
                'errors': errors,
                'form_data': form_data
            })

        # Save to database
        Contact.objects.create(
            name=form_data['name'],
            email=form_data['email'],
            phone=form_data['phone'],
            purpose='donate',  # Hardcoded purpose field
            contact_method=form_data['contact_method'],
            donation_type=form_data['donation_type'],
            subject=form_data['subject'],
            message=form_data['message']
        )

        messages.success(request, 'Thank you for your donation interest! We will contact you soon.')
        return redirect('donate_success')  # Create this URL in urls.py

    return render(request, 'donate.html')

def about(request):
    return render(request, 'aboutUs.html')

def testimonial(request):
    return render(request, 'testimonial.html')

def navbar(request):
    return render(request, 'navbar.html')

def footer(request):
    return render(request, 'footer.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        purpose = request.POST.get('purpose')
        contact_method = request.POST.get('contact_method')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        donation_type = request.POST.get('donation_type', '')
        needs_description = request.POST.get('needs_description', '')

        # Validate input fields
        errors = {}

        if any(char.isdigit() for char in name):
            errors['name_error'] = 'Name field cannot contain numbers.'

        try:
            validate_email(email)
        except ValidationError:
            errors['email_error'] = 'Invalid email address.'

        if not subject or len(subject) < 5:
            errors['subject_error'] = 'Subject must contain at least 5 characters.'

        if not phone.isdigit():
            errors['phone_error'] = 'Phone number must contain only digits.'

        if len(message) < 10:
            errors['message_error'] = 'Message field must contain at least 10 characters.'

        # Additional validation for conditional fields
        if purpose == 'donate' and not donation_type:
            errors['donation_type_error'] = 'Please specify donation type.'
            
        if purpose == 'assistance' and not needs_description:
            errors['needs_description_error'] = 'Please describe your needs.'

        if not contact_method:
            errors['contact_method_error'] = 'Please select preferred contact method.'

        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            return render(request, 'contact.html', {
                'errors': errors,
                'form_data': request.POST
            })

        # Save data to the Contact model
        Contact.objects.create(
            name=name,
            email=email,
            phone=phone,
            purpose=purpose,
            contact_method=contact_method,
            donation_type=donation_type,
            needs_description=needs_description,
            subject=subject,
            message=message
        )
        messages.success(request, 'Your message has been sent successfully!')
        return render(request, 'contact.html', {
            'success_message': 'Your message has been sent successfully!'
        })

    return render(request, 'contact.html')

def join(request):
    if request.method == 'POST':
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        why = request.POST.get('why')
        message = request.POST.get('message')
        availability = request.POST.get('availability')

        # Validate input fields
        errors = {}

        if any(char.isdigit() for char in first_name):
            errors['first_name_error'] = 'First name cannot contain numbers.'

        if any(char.isdigit() for char in last_name):
            errors['last_name_error'] = 'Last name cannot contain numbers.'

        try:
            validate_email(email)
        except ValidationError:
            errors['email_error'] = 'Invalid email address.'

        if not phone.isdigit():
            errors['phone_error'] = 'Phone number must contain only digits.'

        if len(phone) < 10:
            errors['phone_length_error'] = 'Phone number must be at least 10 digits long.'

        if len(why) < 10:
            errors['why_error'] = 'Why field must contain at least 10 characters.'

        if len(message) < 10:
            errors['message_error'] = 'Message field must contain at least 10 characters.'

        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            return render(request, 'join.html', {'errors': errors, 'form_data': request.POST})

        # Save data to the Join model
        Join.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            address=address,
            why=why,
            message=message,
            availability=availability
        )
        messages.success(request, 'Your application has been submitted successfully!')
        return render(request, 'join.html', {'success_message': 'Your application has been submitted successfully!'})

    return render(request, 'join.html')

@login_required
def admin_dashboard(request):
    contacts = Contact.objects.all().order_by('-id')
    joins = Join.objects.all().order_by('-id')
    
    return render(request, 'admin_dashboard.html', {
        'contacts': contacts,
        'joins': joins
    })

def custom_logout(request):
    logout(request)
    messages.success(request, "You've been logged out successfully.")
    return redirect('index')

def contact_view(request):
    if request.method == 'POST':
        # Process your form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        contact_method = request.POST.get('contact_method')
        message = request.POST.get('message')
        
        # Save to database if needed
        
        # Automated response based on contact method
        if contact_method == 'email':
            # Send email
            send_mail(
                'Thank you for contacting HopeBites',
                f'Dear {name},\n\nThank you for reaching out to us. We have received your message and will get back to you soon.\n\nYour message: {message}\n\nBest regards,\nThe HopeBites Team',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
        elif contact_method == 'whatsapp':
            try:
                # Send WhatsApp message (using Twilio API example)
                account_sid = settings.TWILIO_ACCOUNT_SID
                auth_token = settings.TWILIO_AUTH_TOKEN
                client = Client(account_sid, auth_token)
                
                client.messages.create(
                    body=f'Thank you for contacting HopeBites, {name}! We have received your message and will get back to you soon.',
                    from_='whatsapp:+14155238886',  # Your Twilio WhatsApp number
                    to=f'whatsapp:{phone}'
                )
            except Exception as e:
                messages.error(request, f"Failed to send WhatsApp message: {e}")
                return redirect('contact')
        
        # Redirect or return response
        return redirect('contact_success')
    
    return render(request, 'contact.html')