import datetime

async def date2unix(date) -> int:
    unix = datetime.datetime.timestamp(date) * 1000
    return int(str(unix)[0:10])
