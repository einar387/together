import datetime
import uuid
import shortuuid
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager


class Profile(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = (
        ("male", "Male"),
        ("female", "Female"),
        ("non-binary", "Non-binary"),
        ("chair", "Chair"),
    )

    SHOW_ME_CHOICES = (
        ("men", "Men"),
        ("women", "Women"),
        ("both", "Both"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.CharField(max_length=200, unique=True)
    firstname = models.CharField(max_length=200, null=True)
    lastname = models.CharField(max_length=200, null=True)
    password = models.CharField(max_length=200)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    has_account = models.BooleanField(default=False)

    birthdate = models.DateField(null=True, blank=True)
    age = models.PositiveIntegerField(null=True)
    nationality = models.TextField(max_length=20, null=True)
    city = models.TextField(max_length=15, null=True)
    university = models.TextField(max_length=40, null=True)
    description = models.TextField(max_length=500, null=True)

    gender = models.CharField(
        default="male", max_length=10, choices=GENDER_CHOICES, null=False
    )
    show_me = models.CharField(
        default="women", max_length=10, choices=SHOW_ME_CHOICES, null=False
    )

    blocked_profiles = models.ManyToManyField(
        "self", symmetrical=False, related_name="blockedProfiles", blank=True
    )

    USERNAME_FIELD = "email"
    # requred for creating user
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def get_full_name(self):
        return self.firstname + self.lastname


class Photo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(Profile, default=None, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)


class Group(models.Model):
    GENDER_CHOICES = (
        ("male", "Male"),
        ("female", "Female"),
        ("non-binary", "Non-binary"),
        ("chair", "Chair"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        Profile, default=None, on_delete=models.CASCADE, related_name="owner_profile"
    )
    gender = models.CharField(
        default="male", max_length=10, choices=GENDER_CHOICES, null=False
    )
    total_members = models.PositiveIntegerField(null=True)
    share_link = models.CharField(max_length=100, unique=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    members = models.ManyToManyField(
        Profile, blank=True, related_name="member_profiles"
    )

    def save(self, *args, **kwargs):
        if not self.share_link:
            self.share_link = f"https://start.the.night/{shortuuid.uuid()}"
        super().save(*args, **kwargs)



class Like(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{} : {}".format(self.profile_id_1, self.profile_id_2)
