"""
Custom model for making OAuth requests.

This model tracks important state so that we don't need to track this state
in memory. Doing so in memory makes the server stateful and makes it difficult
to run multiple server workers.
"""

from django.contrib.auth import get_user_model
from django.db import models


class OAuthSessionState(models.Model):
    """
    Keeps track of OAuth session state in case the redirect worker is
    different from the worker that generated the redirect URL. Also tracks
    the user that logged in via this session so we can keep their access_token
    alive for as long as possible.
    """

    user = models.OneToOneField(
        get_user_model(), blank=True, null=True, on_delete=models.CASCADE
    )
    access_token = models.CharField(max_length=255, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    session_type = models.CharField(max_length=32, blank=True)  # ucams or xcams
    state_param = models.CharField(max_length=128, blank=True)
