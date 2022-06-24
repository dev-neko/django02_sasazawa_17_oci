from django.core.management.utils import get_random_secret_key

secret_key = f"SECRET_KEY='{get_random_secret_key()}'"
print(secret_key)