import jdatetime

def jalali_to_gregorian(jalali_date_str):
    """
    تبدیل تاریخ هجری شمسی به تاریخ میلادی.

    :param jalali_date_str: تاریخ هجری شمسی به فرمت 'YYYY/MM/DD'
    :return: تاریخ میلادی به فرمت 'YYYY-MM-DD'
    """
    year, month, day = map(int, jalali_date_str.split('/'))
    jalali_date = jdatetime.date(year, month, day)
    gregorian_date = jalali_date.togregorian()
    return gregorian_date.strftime('%Y-%m-%d')

# نمونه استفاده
jalali_date = '۱۴۰۳/۰۵/۱۳'
gregorian_date = jalali_to_gregorian(jalali_date)
print(gregorian_date)  # خروجی: 2023-08-04
