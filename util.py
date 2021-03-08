def check_grade(percent: float):
    if 90 <= percent <= 100:
        return 'A+'
    elif 80 <= percent < 90:
        return 'A'
    elif 70 <= percent < 80:
        return 'B+'
    elif 60 <= percent < 70:
        return 'B'
    elif 50 <= percent < 60:
        return 'C'
    elif 40 <= percent < 50:
        return 'D'
    elif 33 <= percent < 40:
        return 'E'
    else:
        return 'F'