import os, sys, traceback, faulthandler
faulthandler.enable()

_real_exit = os._exit
def _spy(code):
    print("os._exit called with", code, flush=True)
    traceback.print_stack()
    _real_exit(code)
os._exit = _spy

os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"
import django
django.setup()
print("setup done", flush=True)

from django.db import connection
try:
    print("connecting...", flush=True)
    connection.ensure_connection()
    print("connected", flush=True)

    from django.core.management import call_command
    call_command("migrate")
    print("AFTER MIGRATE", flush=True)
except BaseException:
    print("CAUGHT:", flush=True)
    traceback.print_exc()