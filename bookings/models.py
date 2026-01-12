from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Booking(models.Model):
    STATUS = [
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
        ("CANCELLED", "Cancelled"),
    ]

    booking_no = models.CharField(max_length=20, unique=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # keep as CharField; form will whitelist
    service = models.CharField(max_length=100)
    date = models.DateField()
    time_slot = models.CharField(max_length=30)

    status = models.CharField(max_length=10, choices=STATUS, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Auto-generate Booking Number: BK-YYYYMMDD-XXXX
        if not self.booking_no:
            today = timezone.localdate().strftime("%Y%m%d")
            count_today = Booking.objects.filter(created_at__date=timezone.localdate()).count() + 1
            self.booking_no = f"BK-{today}-{count_today:04d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.booking_no


class AuditLog(models.Model):
    ACTIONS = [
        ("LOGIN", "Login"),
        ("LOGOUT", "Logout"),
        ("CREATE_BOOKING", "Create Booking"),
        ("UPDATE_STATUS", "Update Booking Status"),
        ("CANCEL_BOOKING", "Cancel Booking"),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=30, choices=ACTIONS)
    details = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.created_at} - {self.action}"
