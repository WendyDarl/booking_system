from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.shortcuts import render, redirect

from .forms import RegisterForm, BookingForm
from .models import Booking, AuditLog

# =========================
# LOGIN BRUTE FORCE PROTECTION
# =========================
LOGIN_ATTEMPT_LIMIT = 5
LOGIN_BLOCK_SECONDS = 300  # 5 minutes

def _login_cache_key(ip: str, username: str) -> str:
    return f"login_fail:{ip}:{username}".lower()

# =========================
# AUTH VIEWS
# =========================
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        ip = request.META.get("REMOTE_ADDR", "unknown")

        key = _login_cache_key(ip, username)
        fails = cache.get(key, 0)

        if fails >= LOGIN_ATTEMPT_LIMIT:
            return render(request, "bookings/login.html", {
                "error": "Too many failed attempts. Please try again later."
            })

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)

            AuditLog.objects.create(
                user=user,
                action="LOGIN",
                details="User logged in"
            )

            cache.delete(key)
            return redirect("bookings:dashboard")

        # failed login
        cache.set(key, fails + 1, timeout=LOGIN_BLOCK_SECONDS)
        AuditLog.objects.create(
            user=None,
            action="LOGIN",
            details=f"Failed login attempt for username={username}"
        )

        return render(request, "bookings/login.html", {
            "error": "Invalid username or password"
        })

    return render(request, "bookings/login.html")


@login_required
def user_logout(request):
    AuditLog.objects.create(
        user=request.user,
        action="LOGOUT",
        details="User logged out"
    )
    logout(request)
    return redirect("bookings:login")


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("bookings:login")
    else:
        form = RegisterForm()

    return render(request, "bookings/register.html", {"form": form})


# =========================
# MAIN PAGES
# =========================
@login_required
def dashboard(request):
    return render(request, "bookings/dashboard.html")


@login_required
def booking_create(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()

            AuditLog.objects.create(
                user=request.user,
                action="CREATE_BOOKING",
                details=f"Booking {booking.booking_no} created"
            )

            return redirect("bookings:my_bookings")
    else:
        form = BookingForm()

    return render(request, "bookings/booking_form.html", {"form": form})


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "bookings/my_bookings.html", {"bookings": bookings})


# =========================
# CUSTOM ERROR PAGES (No.4)
# =========================
def bad_request(request, exception):
    return render(request, "400.html", status=400)

def permission_denied(request, exception):
    return render(request, "403.html", status=403)

def page_not_found(request, exception):
    return render(request, "404.html", status=404)

def server_error(request):
    return render(request, "500.html", status=500)
