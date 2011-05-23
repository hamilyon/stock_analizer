

#----------------------------------------------------------------------
def guess(s):
    """Convert string to the more suitable type like int, float, date, time, etc."""
    # Guess type
    value = s
    if value[-1] == '%':
        value = value[:-1]
    # Try to convert to other types
    if type(value) is str:
        try: # Try to convert to int
            value = int(value)
        except ValueError:
            try: # Try to convert to float
                value = float(value)
            except ValueError: pass      
    return value

#----------------------------------------------------------------------
def decapitalize(s):
    """Change the first char in the input string to lowercase
    if second letter isn't capital."""
    if len(s) > 1 and not s[1].isupper():
        return s[0].lower() + s[1:]
    return s
