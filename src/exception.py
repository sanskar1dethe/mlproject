import sys
from src.logger import logging

def error_message_detail(error,error_detail:sys):
    
    _,_,exec_tb =  error_detail.exc_info() #the first 2 values of return are not important the last value has all the information regaring the error 
    file_name = exec_tb.tb_frame.f_code.co_filename
    error_msg = "Error occured in python script name[{0}] line number[{1}] error message[{2}]".format(file_name,exec_tb.tb_lineno,str(error))

    return error_msg


class CustomException(Exception):
    def __init__(self,error_message,error_detail:sys):
        super().__init__(error_message)
        self.error_message=error_message_detail(error_message,error_detail=error_detail)
    
    def __str__(self):
        return self.error_message
