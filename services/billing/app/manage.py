#!/usr/bin/env python
import os, sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE','billing_project.settings')
from django.core.management import execute_from_command_line
execute_from_command_line(sys.argv)
