from datetime import datetime, timedelta
from pytz import timezone

import click
import re
import pytz

TIME_REGEX = re.compile('^((?P<day>[a-zA-Z]+)\s)?(?P<hour>[0-9]{1,2})\s(?P<ampm>(am|pm|AM|PM))$')
TODAY = datetime.now()
print(f'TODAY: {TODAY.strftime("%Y/%m/%d %H:%M")}\n')
MEXICO = timezone('America/Mexico_City')

TIMEZONES = {
    "Colombia": timezone('America/Bogota'),
    "Chile": timezone('America/Santiago'),
    "Ecuador": timezone('America/Guayaquil'),
    "Perú": timezone('America/Lima'),
    "Argentina": timezone('America/Argentina/Buenos_Aires'),
    "Guinea Ecuatorial": timezone('Africa/Malabo'),
    "Costa Rica": timezone('America/Costa_Rica')
}

SPANISH_DAYS = [
    'lunes',
    'martes',
    'miercoles',
    'jueves',
    'viernes',
    'sabado',
    'domingo'
]

ENGLISH_DAYS = [
    'monday',
    'tuesday',
    'wednesday',
    'thursday',
    'friday',
    'saturday',
    'sunday'
]

@click.command()
@click.option('-d', '--month-day', type=click.INT)
@click.argument('time-string', type=click.STRING)
def main(time_string: str, month_day: int):
    """
    CADENA_TIEMPO Este es tu tiempo en lenguaje natural
    """
    match = TIME_REGEX.match(time_string)
    if match:
        matches = match.groupdict()
        
        hour = int(matches['hour']) + (0 if matches['ampm'] == 'am' else 12)
        
        if month_day is not None:
            if month_day < TODAY.day:
                print('MONTH DATE MUST BE MINOR THAN TODAY')
                exit()
            final_date = datetime(TODAY.year, TODAY.month, month_day, hour, 0)
        else:
            week_day = SPANISH_DAYS.index(matches['day'].lower())
            days_for_sunday = 6 - TODAY.weekday()
            days_for_date = ((TODAY.weekday() + days_for_sunday + week_day) % 6) + 1
            user_date = TODAY + timedelta(days=days_for_date)
        
            final_date = datetime(user_date.year, user_date.month, user_date.day, hour, 0)
        
        for country, time_zone in TIMEZONES.items():
            date = final_date.astimezone(time_zone)
            spanish_day_index = ENGLISH_DAYS.index(date.strftime('%A').lower())
            print(f'{country}: {SPANISH_DAYS[spanish_day_index].capitalize()} {date.strftime("%d, %H:%M")}')
    else:
        print('INVALID STRING')

if __name__ == '__main__':
    main()