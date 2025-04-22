from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    purpose = models.CharField(max_length=50, choices=[('donate', 'Donate'), ('assistance', 'Assistance')], null=True, blank=True)
    contact_method = models.CharField(max_length=50, choices=[('email', 'Email'), ('phone', 'Phone')], null=True, blank=True)
    donation_type = models.CharField(max_length=100, null=True, blank=True)
    needs_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Join(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    why = models.TextField()
    message = models.TextField()
    availability = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"