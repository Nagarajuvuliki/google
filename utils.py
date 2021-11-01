from datetime import datetime


def zeroStrings(digits, no_zeros):
    digits = str(digits)
    newDigit = f"{'0'*no_zeros if no_zeros > 0 else 1}{digits}"[
        ::-1][:no_zeros][::-1]
    return newDigit


def getDayFromYear():
    return datetime.now().isocalendar().week * 7 + (7 - datetime.now().weekday())
