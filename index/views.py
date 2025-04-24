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

# def contact(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         phone = request.POST.get('phone')
#         purpose = request.POST.get('purpose')
#         contact_method = request.POST.get('contact_method')
#         subject = request.POST.get('subject')
#         message = request.POST.get('message')
#         donation_type = request.POST.get('donation_type', '')
#         needs_description = request.POST.get('needs_description', '')

#         # Validate input fields
#         errors = {}

#         if any(char.isdigit() for char in name):
#             errors['name_error'] = 'Name field cannot contain numbers.'

#         try:
#             validate_email(email)
#         except ValidationError:
#             errors['email_error'] = 'Invalid email address.'

#         if not subject or len(subject) < 5:
#             errors['subject_error'] = 'Subject must contain at least 5 characters.'

#         if not phone.isdigit():
#             errors['phone_error'] = 'Phone number must contain only digits.'

#         if len(message) < 10:
#             errors['message_error'] = 'Message field must contain at least 10 characters.'

#         # Additional validation for conditional fields
#         if purpose == 'donate' and not donation_type:
#             errors['donation_type_error'] = 'Please specify donation type.'
            
#         if purpose == 'assistance' and not needs_description:
#             errors['needs_description_error'] = 'Please describe your needs.'

#         if not contact_method:
#             errors['contact_method_error'] = 'Please select preferred contact method.'

#         if errors:
#             for key, value in errors.items():
#                 messages.error(request, value)
#             return render(request, 'contact.html', {
#                 'errors': errors,
#                 'form_data': request.POST
#             })

#         # Save data to the Contact model
#         Contact.objects.create(
#             name=name,
#             email=email,
#             phone=phone,
#             purpose=purpose,
#             contact_method=contact_method,
#             donation_type=donation_type,
#             needs_description=needs_description,
#             subject=subject,
#             message=message
#         )
#         messages.success(request, 'Your message has been sent successfully!')
#         return render(request, 'contact.html', {
#             'success_message': 'Your message has been sent successfully!'
#         })

#     return render(request, 'contact.html')

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

# def contact_view(request):
#     if request.method == 'POST':
#         # Process your form data
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         phone = request.POST.get('phone')
#         contact_method = request.POST.get('contact_method')
#         message = request.POST.get('message')
        
#         # Save to database if needed
        
#         # Automated response based on contact method
#         if contact_method == 'email':
#             # Send email
#             send_mail(
#                 'Thank you for contacting HopeBites',
#                 f'Dear {name},\n\nThank you for reaching out to us. We have received your message and will get back to you soon.\n\nYour message: {message}\n\nBest regards,\nThe HopeBites Team',
#                 settings.DEFAULT_FROM_EMAIL,
#                 [email],
#                 fail_silently=False,
#             )
#         elif contact_method == 'whatsapp':
#             try:
#                 # Send WhatsApp message (using Twilio API example)
#                 account_sid = settings.TWILIO_ACCOUNT_SID
#                 auth_token = settings.TWILIO_AUTH_TOKEN
#                 client = Client(account_sid, auth_token)
                
#                 client.messages.create(
#                     body=f'Thank you for contacting HopeBites, {name}! We have received your message and will get back to you soon.',
#                     from_='whatsapp:+14155238886',  # Your Twilio WhatsApp number
#                     to=f'whatsapp:{phone}'
#                 )
#             except Exception as e:
#                 messages.error(request, f"Failed to send WhatsApp message: {e}")
#                 return redirect('contact')
        
#         # Redirect or return response
#         return redirect('contact_success')
    
#     return render(request, 'contact.html')

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def get_response_with_answer(user_response):
    question_flow = {
        "start": {
            "answer": "Welcome to HopeBites! How can I help you today?",
            "follow_up": [
                "What does HopeBites do?",
                "How can I donate food?",
                "How can I get involved as a volunteer?"
            ]
        },
        "what does hopebites do?": {
            "answer": "HopeBites rescues surplus food and redistributes it to communities in need, reducing waste and fighting hunger. We partner with donors, volunteers, and NGOs to make food accessible to all.",
            "follow_up": [
                "How does HopeBites collect food?",
                "Who benefits from the food donations?",
                "Is HopeBites a nonprofit organization?"
            ]
        },
        "how can i donate food?": {
            "answer": "You can donate packaged or bulk surplus food by scheduling a pickup or dropping it at our collection centers. We accept perishable and non-perishable items.",
            "follow_up": [
                "What kind of food can I donate?",
                "Do I need to package the food myself?",
                "Can I schedule a pickup?"
            ]
        },
        "how can i get involved as a volunteer?": {
            "answer": "Volunteers help with food collection, distribution, and awareness campaigns. No prior experience is needed—just sign up on our website!",
            "follow_up": [
                "What kind of volunteering roles are available?",
                "Do I need any prior experience to volunteer?",
                "How do I sign up to volunteer?"
            ]
        },
        "what kind of food can i donate?": {
            "answer": "We accept non-perishables, fresh produce, and packaged meals. Leftovers from events are welcome if properly stored.",
            "follow_up": [
                "Can I donate leftover food from events?",
                "Is there a minimum quantity for donations?",
                "Can restaurants or cafes donate?"
            ]
        },
        "can i schedule a pickup?": {
            "answer": "Yes! Request a pickup via our website. We serve select areas and may require 24-48 hours' notice.",
            "follow_up": [
                "What areas does HopeBites operate in?",
                "How far in advance should I request a pickup?",
                "Is there a fee for pickup?"
            ]
        },
        "how does hopebites collect food?": {
            "answer": "We collect food through donor pickups, business partnerships, and community drop-offs. Our team ensures safe and hygienic handling.",
            "follow_up": [
                "Does HopeBites have its own transport?",
                "Can I drop off food myself?",
                "Do they partner with local businesses?"
            ]
        },
        "who benefits from the food donations?": {
            "answer": "Food goes to underserved communities, shelters, and NGOs. We prioritize marginalized groups and disaster-affected areas.",
            "follow_up": [
                "Are donations given directly to individuals?",
                "Does HopeBites work with shelters or NGOs?",
                "Can I suggest a community in need?"
            ]
        },
        "is hopebites a nonprofit organization?": {
            "answer": "Yes, we're a registered nonprofit. Donations are tax-deductible, and we rely on grants and public support.",
            "follow_up": [
                "Is my donation tax-deductible?",
                "Where can I find your registration details?",
                "How is HopeBites funded?"
            ]
        },
        "contact hopebites": {
        "answer": "You can reach us directly on WhatsApp:",
        "action": "https://api.whatsapp.com/send?phone=919137871700"  # ← Replace with your number
}
    }

    default_response = {
        "answer": "Sorry, I didn't understand that.",
        "follow_up": [
            "Please choose from the available options",
            "Or type 'Contact HopeBites' to chat directly"
        ]
    }

    normalized_input = user_response.strip().lower()
    greetings = ["hi", "hello", "hey", ""]

    if normalized_input in greetings:
        return question_flow["start"]
    
    return question_flow.get(normalized_input, default_response)

@csrf_exempt
def whatsapp_webhook(request):
    if request.method == "POST":
        try:
            incoming_data = json.loads(request.body.decode("utf-8"))
            user_message = incoming_data.get("Body", "").strip()
        except (json.JSONDecodeError, AttributeError):
            return JsonResponse({"error": "Invalid request format"}, status=400)

        response_data = get_response_with_answer(user_message)
        return JsonResponse(response_data)

    return JsonResponse({"error": "Invalid request method"}, status=400)


from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Contact
import json
import logging
import pywhatkit

logger = logging.getLogger(__name__)

class NotificationError(Exception):
    pass

def send_email_notification(contact_data, contact_id):
    """Send simple text email without templates"""
    try:
        subject = "Thank you for contacting HopeBites"
        message = (
            f"Hi {contact_data['name']},\n\n"
            f"We've received your message (Reference ID: {contact_id}).\n"
            f"Your message: {contact_data['message']}\n\n"
            "Our team will respond shortly.\n\n"
            "Best regards,\n"
            "HopeBites Team"
        )
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[contact_data['email']],
            fail_silently=False,
        )
        logger.info(f"Email sent to {contact_data['email']}")
        return True
    except Exception as e:
        logger.error(f"Email failed for {contact_data['email']}: {str(e)}")
        return False
    
def send_whatsapp_notification(contact_data, contact_id):
    """Send WhatsApp message using pywhatkit"""
    try:
        pywhatkit.sendwhatmsg_instantly(
            phone_no=f"+91{contact_data['phone']}",
            message=(
                f"Hi {contact_data['name']},\n\n"
                f"We've received your request (Ref: #{contact_id}).\n"
                "Our team will contact you shortly.\n\n"
                "Best regards,\nHopeBites Team"
            ),
            wait_time=20,
            tab_close=True,
            close_time=3
        )
        logger.info(f"WhatsApp message sent to {contact_data['phone']}")
    except Exception as e:
        logger.error(f"WhatsApp failed for {contact_data['phone']}: {str(e)}")
        raise NotificationError("WhatsApp notification failed")

def contact(request):
    if request.method == 'POST':
        try:
            # Extract and validate form data
            data = {
                'name': request.POST.get('name', '').strip(),
                'email': request.POST.get('email', '').strip(),
                'phone': request.POST.get('phone', '').strip(),
                'purpose': request.POST.get('purpose'),
                'contact_method': request.POST.get('contact_method'),
                'message': request.POST.get('message', '').strip()
            }

            # Validation
            errors = {}
            if not data['name']:
                errors['name'] = 'Name is required'
            elif any(char.isdigit() for char in data['name']):
                errors['name'] = 'Name cannot contain numbers'
                
            if not data['email']:
                errors['email'] = 'Email is required'
            else:
                try:
                    validate_email(data['email'])
                except ValidationError:
                    errors['email'] = 'Invalid email address'
                    
            if not data['phone']:
                errors['phone'] = 'Phone number is required'
            elif not data['phone'].isdigit():
                errors['phone'] = 'Phone must contain only digits'
                
            if not data['purpose']:
                errors['purpose'] = 'Purpose is required'
                
            if not data['contact_method']:
                errors['contact_method'] = 'Contact method is required'
                
            if not data['message']:
                errors['message'] = 'Message is required'
            elif len(data['message']) < 10:
                errors['message'] = 'Message must be at least 10 characters'

            if errors:
                for error in errors.values():
                    messages.error(request, error)
                return render(request, 'contact.html', {
                    'errors': errors,
                    'form_data': request.POST
                })

            # Save to database
            contact_obj = Contact.objects.create(**data)
            
            # Send notifications
            email_sent = send_email_notification(data, contact_obj.id)
            
            whatsapp_sent = False
            if data['contact_method'] == 'phone':
                whatsapp_sent = send_whatsapp_notification(data, contact_obj.id)
            
            if email_sent and (data['contact_method'] != 'phone' or whatsapp_sent):
                messages.success(request, 'Thank you! Your message has been received. We will contact you soon.')
            elif not email_sent and data['contact_method'] != 'phone':
                messages.warning(request, 'Form submitted successfully, but email notification failed. We will contact you shortly.')
            elif data['contact_method'] == 'phone' and not whatsapp_sent:
                messages.warning(request, 'Form submitted successfully, but WhatsApp notification failed. We will contact you shortly.')
            else:
                messages.warning(request, 'Form submitted successfully, but notifications failed. We will contact you shortly.')
            
            return redirect('contact')

        except Exception as e:
            logger.error(f"Contact form error: {str(e)}")
            messages.error(request, 'An error occurred. Please try again.')
            return render(request, 'contact.html', {'form_data': request.POST})

    return render(request, 'contact.html')

@csrf_exempt
def whatsapp_webhook(request):
    """Handle incoming WhatsApp messages for basic chatbot functionality"""
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode('utf-8'))
            user_message = data.get("Body", "").strip().lower()
            
            responses = {
                "hi": {
                    "answer": "Hello! How can we help you today?",
                    "options": ["Donate food", "Request assistance", "Volunteer"]
                },
                "donate": {
                    "answer": "We accept food donations at our centers.",
                    "action": "/donate"
                },
                "contact": {
                    "answer": "You can reach us at:",
                    "details": "Phone: +91 9137871700\nEmail: contact@hopebites.org"
                }
            }
            
            response = responses.get(user_message, {
                "answer": "Sorry, I didn't understand. Try asking about:",
                "options": ["Donations", "Assistance", "Volunteering"]
            })
            
            return JsonResponse(response)
            
        except Exception as e:
            logger.error(f"WhatsApp webhook error: {str(e)}")
            return JsonResponse({"error": "Invalid request"}, status=400)
    
    return JsonResponse({"error": "Method not allowed"}, status=405)

def contact_success(request):
    return render(request, 'contact.html', {
        'title': 'Thank You',
        'message': 'We have received your message and will respond soon.'
    })