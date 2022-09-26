"""
WSGI config for RecommendationModule project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os
import asyncio

from django.core.wsgi import get_wsgi_application
# from async_kafka.views import main
from async_kafka.views import send_one, consume

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recommendation_module.settings')

application = get_wsgi_application()
print('Hello World')
asyncio.run(send_one())
asyncio.run(consume())