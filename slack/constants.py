from enum import Enum


class Constants(str, Enum):
    """
    Class containing set of constants used mainly in views
    Class inheritances from str for serialization purposes
    """
    DIALOG_CANCELLATION = 'dialog_cancellation'
    DIALOG_SUBMISSION = 'dialog_submission'
    EDIT_TICKET = 'edit_ticket'
    CREATE_TICKET = 'create_ticket'
    EDIT = 'E'
    DELETE = 'D'
    BLOCK = 'block_actions'

