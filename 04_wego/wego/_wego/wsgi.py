
import os
# import sys
from django.core.wsgi import get_wsgi_application

#sys.path.append("/home/cevan/cebuschool_pro/cebuschool/")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '_wego.settings')
application = get_wsgi_application()
