from django.db import models

# Create your models here.


class Organization(models.Model):
    name = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Organization"

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=255)
    organization = models.ForeignKey(Organization, blank=True, null=True, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Contact"

    def __str__(self):
        return self.name


class ContactEmail(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="emails")
    email = models.EmailField(unique=True)

    class Meta:
        db_table = "ContactEmail"

    def __str__(self):
        return f"{self.contact.name} - {self.email}"


class Label(models.Model):
    google_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    contacts = models.ManyToManyField(Organization, related_name="labels")

    class Meta:
        db_table = "Label"

    def __str__(self):
        return self.name
