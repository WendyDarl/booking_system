from django.contrib import admin
from .models import Booking, AuditLog


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "booking_no",
        "user",
        "service",
        "date",
        "time_slot",
        "status",
        "created_at",
    )
    list_filter = ("status", "date", "service")
    search_fields = ("booking_no", "user__username", "service")
    ordering = ("-created_at",)
    readonly_fields = ("booking_no", "created_at")

    def save_model(self, request, obj, form, change):
        old_status = None
        if change:
            old_status = Booking.objects.get(pk=obj.pk).status

        super().save_model(request, obj, form, change)

        if change and old_status != obj.status:
            AuditLog.objects.create(
                user=request.user,
                action="UPDATE_STATUS",  # ✅ MUST MATCH AuditLog.ACTIONS
                details=f"Booking {obj.booking_no} status changed from {old_status} to {obj.status}",
            )


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("created_at", "user", "action", "details")
    list_filter = ("action", "created_at")
    search_fields = ("user__username", "details")
    ordering = ("-created_at",)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
