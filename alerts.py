from abc import ABC, abstractclassmethod


class Alert(ABC): # pragma: no cover
    @abstractclassmethod
    def send_alert(self, breach_type): 
        raise NotImplementedError


class EmailAlert(Alert):
    def __init__(self, recepient) -> None:
        self.recepient = recepient

    def send_to_email(self, breach_type, alert=print):
        if breach_type != "NORMAL":
            alert(f"To: {self.recepient}")
            alert(f"Hi, the temperature is {breach_type}")
            return True
        return False
        

    def send_alert(self, breach_type):
        return self.send_to_email(breach_type)

class ControllerAlert(Alert):
    def __init__(self, header) -> None:
        self.header = header

    def send_to_controller(self, breach_type, alert=print):
        if breach_type != "NORMAL":
            alert(f"{self.header}, {breach_type}")
            return True
        return False

    def send_alert(self, breach_type):
        return self.send_to_controller(breach_type)
        