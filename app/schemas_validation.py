

def students_count_validation(cls, v):
    if not v.isnumeric():
        raise ValueError("Only integers are allowed.")
    else:
        return v

    # if v not in ('desc', 'asc'):
    #     raise ValueError(f"'{v}' order argument is invalid. Only 'desc' and 'asc' are allowed.")
    # elif v == "desc":
    #     return True
    # else:
    #     return False
