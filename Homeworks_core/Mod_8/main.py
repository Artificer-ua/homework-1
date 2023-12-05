from datetime import date, datetime, timedelta


def get_birthdays_per_week(users):
    # here only for autocheck
    days_name = {
        0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
        4: "Friday",
        5: "Saturday",
        6: "Sunday",
    }

    # dict for result
    this_week_birthday = dict()

    # if empty input
    if not users:
        return this_week_birthday

    # Current date
    current_date = date.today()

    # listing dict
    for item in users:
        # if current month and current year
        if item.get("birthday").month == current_date.month and item.get("birthday").year == current_date.year:
            # if b-day in range of 7 days from today
            if (item.get("birthday") - current_date).days in range(0, 7):
                # if sat or sun
                if item.get('birthday').weekday() == 5 or item.get('birthday').weekday() == 6:
                    this_week_birthday.setdefault(days_name.get(0), []).append(item.get('name'))
                # any other day of week
                else:
                    this_week_birthday.setdefault(days_name.get(item.get('birthday').weekday()), []).\
                        append(item.get('name'))
        # some trash
        # if current month = 12, birthday month = 1 and current year + 1.
        # elif (current_date.month == 12 and item.get("birthday").month == 1) and \
        #         item.get("birthday").year == current_date.year + 1:
        #     #if b-day in range of 7 days from today
        #     if item.get('birthday') < (current_date + timedelta(days=7)):
        #         if item.get('birthday').weekday() == 5 or item.get('birthday').weekday() == 6:
        #             this_week_birthday.setdefault(days_name.get(0), []).append(item.get('name'))
        #         else:
        #             this_week_birthday.setdefault(days_name.get(item.get('birthday').weekday()), []).append(item.get('name'))

        # if current month = 12, birthday month = 1 and not current year.
        elif current_date.month == 12 and item.get("birthday").month == 1:
            # calculating new day of week for current year
            year, month, day = str(item.get("birthday")).split("-")
            # print("Day: ", day, "Month: ", month, "Year: ", year, sep="\t")
            day_of_week = datetime(year=current_date.year + 1, month=int(month), day=int(day)).date()

            # if b-day in range of 7 days from today
            if item.get('birthday') < (current_date + timedelta(days=7)):
                # if sat or sun
                if day_of_week.weekday() == 5 or day_of_week.weekday() == 6:
                    this_week_birthday.setdefault(days_name.get(0), []).append(item.get('name'))
                # any other day of week
                else:
                    this_week_birthday.setdefault(days_name.get(day_of_week.weekday()), []).append(item.get('name'))
        else: pass

    return  this_week_birthday


if __name__ == "__main__":
    users = [
        {"name": "Jan Koum", "birthday": datetime(1976, 1, 1).date()},
        {"name": "Vlad", "birthday": datetime(2025, 1, 1).date()},
        {"name": "Simon", "birthday": datetime(2023, 9, 6).date()},
        {"name": "Maryna", "birthday": datetime(2023, 9, 10).date()},
        {"name": "Olga", "birthday": datetime(2023, 9, 12).date()},
        {"name": "Denys", "birthday": datetime(2024, 9, 3).date()}
    ]

    result = get_birthdays_per_week(users)
    print(result)
    # Виводимо результат
    for day_name, names in result.items():
        print(f"{day_name}: {', '.join(names)}")
