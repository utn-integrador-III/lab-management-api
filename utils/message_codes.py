# utils/message_codes.py

"""
This file defines the message codes for multilanguage in the frontend
Using i18n standard, please check multilanguage folder to add or modify messages
assets/i18n/<lang>
"""

# Common Messages
OK_MSG = "OK_MSG"
CREATED_MSG = "CREATED_MSG"
NOT_FOUND_MSG = "NOT_FOUND_MSG"
CONFLICT_MSG = "CONFLICT_MSG"
UNPROCESSABLE_ENTITY_MSG = "UNPROCESSABLE_ENTITY_MSG"
INTERNAL_SERVER_ERROR_MSG = "INTERNAL_SERVER_ERROR_MSG"
SERVER_TIMEOUT_MSG = "SERVER_TIMEOUT_MSG"
NO_DATA = "NO_DATA"
ERROR_MSG = "ERROR_MSG"  # Añadir ERROR_MSG aquí
SUCCESS_MSG = "SUCCESS_MSG"  # Añadir SUCCESS_MSG aquí

INCORRECT_REQUEST_PARAM = 'INCORRECT_REQUEST_PARAM'

# Common Validations Messages
INVALID_ID = "INVALID_ID"  # Invalid Id

# Health Validations Messages
HEALTH_NOT_FOUND = "HEALTH_NOT_FOUND"  # Health not found
HEALTH_SUCCESSFULLY = "HEALTH_SUCCESSFULLY"  # Health successfully responded

# LAB Validations Messages
LAB_NOT_FOUND = "LAB_NOT_FOUND"  # LAB not found
LAB_SUCCESSFULLY_UPDATED = "LAB_SUCCESSFULLY_UPDATED"  # LAB successfully updated
LAB_SUCCESSFULLY_DELETED = "LAB_SUCCESSFULLY_DELETED"  # LAB successfully deleted
LAB_SUCCESSFULLY_CREATED = "LAB_SUCCESSFULLY_CREATED"  # LAB created successfully
LAB_ALREADY_EXIST = "LAB_ALREADY_EXIST"  # LAB already exist from database
LAB_NAME_REQUIRED = "LAB_NAME_REQUIRED"  # Requerid LAB name
LAB_NUM_REQUIRED = "LAB_NUM_REQUIRED"  # Requerid LAB Num
LAB_COMPUTERS_REQUIRED = "LAB_COMPUTERS_REQUIRED"  # Requerid Computers in Lab

# Professor Validations Messages
PROFESSOR_EMAIL_REQUIRED = "PROFESSOR_EMAIL_REQUIRED" # Requerid Professor Email 
PROFESSOR_NOT_FOUND = "PROFESSOR_NOT_FOUND" # Professor not found
