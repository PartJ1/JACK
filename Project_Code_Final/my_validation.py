import calendar
import re

class validation():
    def create_acount
    def date(self, data):
        # check if data in form [dd, mm, yyyy]
        if type(data) != "list":
            return False

        day_range = calendar.monthrange(data[2], data[1])

        if 0 < data[0] <= day_range:
            if 0 < data[1] < 13:
                if 0 < data[2]:
                    return True
            
        return False
    
    def email(self, data):
        # using regex to validate email format of "sssssss@sssss.sss"
        if re.fullmatch(r"[a-zA-Z0-9._]*+@[a-zA-Z0-9]*+.+[a-zA-Z0-9]*", data):
            return True
        return False


if __name__ == "__main__":
    # valid = validation()
    if re.fullmatch(r"[a-zA-Z0-9._]*+@[a-zA-Z0-9]*+.+[a-zA-Z0-9]*", "ayiug@pus"):
        print("true")
