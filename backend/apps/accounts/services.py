import re
import uuid
from django.contrib.auth import get_user_model

User = get_user_model()


def get_or_create_dummy_business_owner(phone='', email=None, first_name='', last_name=''):
    """Find an existing user by email (owner reassignment), or create a placeholder
    business_owner account — at the given email if one was provided (so that person
    can log in/reset their password later), or derived from phone when no email is given.
    Returns (user, created).
    """
    if email:
        try:
            return User.objects.get(email__iexact=email), False
        except User.DoesNotExist:
            candidate_email = email
            digits = re.sub(r'\D', '', phone or '') or uuid.uuid4().hex[:10]
            base_username = f"biz_{re.sub(r'[^a-zA-Z0-9]', '', email.split('@')[0]) or digits}"
            candidate_username, i = base_username, 1
            while User.objects.filter(username=candidate_username).exists():
                i += 1
                candidate_username = f"{base_username}-{i}"
            user = User(
                email=candidate_email,
                username=candidate_username,
                first_name=first_name or 'Business',
                last_name=last_name or 'Owner',
                role=User.Role.BUSINESS_OWNER,
                phone=phone or '',
            )
            user.set_unusable_password()
            user.save()
            return user, True

    digits = re.sub(r'\D', '', phone or '') or uuid.uuid4().hex[:10]
    base_email = f"{digits}@business.vbazaar.local"
    candidate_email, i = base_email, 1
    while User.objects.filter(email__iexact=candidate_email).exists():
        i += 1
        candidate_email = f"{digits}-{i}@business.vbazaar.local"

    base_username = f"biz_{digits}"
    candidate_username, i = base_username, 1
    while User.objects.filter(username=candidate_username).exists():
        i += 1
        candidate_username = f"{base_username}-{i}"

    user = User(
        email=candidate_email,
        username=candidate_username,
        first_name=first_name or 'Business',
        last_name=last_name or 'Owner',
        role=User.Role.BUSINESS_OWNER,
        phone=phone or '',
    )
    user.set_unusable_password()
    user.save()
    return user, True
