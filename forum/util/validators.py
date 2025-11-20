def len_utf16 (string):
    """
    JavaScript and HTML deal in utf-16. This is needed to match the local HTML string length validation with sever side string length validation
    
    Parameters:
        string (str): String to determine the UTF-16 charpoint length of.

    Returns:
        UTF-16 charpoint length of string.
    """
    l = 0
    for c in string:
        if ord(c) < 65536:
            l += 1
        else:
            l += 2
    return l
