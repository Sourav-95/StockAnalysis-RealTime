import sys
from components.logger import logger

def error_message_detail(error,error_detail:sys):
    _,_,exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = "Error occured: [{0}] line number  [{1}] error message[{2}]".format(
        file_name, exc_tb.tb_lineno, str(error))
    
    return error_message

class CustomException(Exception):
    def __init__(self,error_message,error_detail:sys):
        super().__init__(error_message)
        self.error_message=error_message_detail(error_message,error_detail=error_detail)
    
    def __str__(self):
        return self.error_message
    

# Wrap to handle and log exceptions
def log_and_raise_exception(error, error_detail:sys, custom_message:str=""):
    
    custom_error = CustomException(error, error_detail)
    log_message = f"{custom_message} - {custom_error}" if custom_message else str(custom_error)
    logger.debug(log_message)
    raise custom_error
