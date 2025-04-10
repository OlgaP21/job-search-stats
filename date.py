from calendar import isleap


class Date:
    
    _month_to_id = {
        'Jaanuar': '01', 'Veebruar': '02', 'Märts': '03',
        'Aprill': '04', 'Mai': '05', 'Juuni': '06',
        'Juuli': '07', 'August': '08', 'September': '09',
        'Oktoober': '10', 'November': '11', 'Detsember': '12',
    }
    
    _id_to_month = {
        '01': 'Jaanuar', '02': 'Veebruar', '03': 'Märts',
        '04': 'Aprill', '05': 'Mai', '06': 'Juuni',
        '07': 'Juuli', '08': 'August', '09': 'September',
        '10': 'Oktoober', '11': 'November', '12': 'Detsember'
    }
    
    _short_months = [2, 4, 6, 9, 11]
    
    
    def __init__(self, day: int, month: str, year: int) -> None:
        if self._date_valid(day, int(self._month_to_id[month]), year):
            self.day = day
            self.month = self._month_to_id[month]
            self.year = year
        else:
            self.day = 31
            self.month = '05'
            self.year = 2024
    
    
    def get_day(self) -> int:
        return self.day
    
    
    def get_month(self) -> str:
        return self._id_to_month[self.month]
    
    
    def get_year(self) -> int:
        return self.year
    
    
    def set_date(self, day: int, month: str, year: int) -> None:
        if self._date_valid(day, int(self._month_to_id[month]), year):
            self.day = day
            self.month = int(self._month_to_id[month])
            self.year = year
    
    
    def _date_valid(self, day: int, month: int, year: int) -> bool:
        if day > 30 and month in self._short_months:
            return False
        if month == 2 and day > 29:
            return False
        if month == 2 and not isleap(year) and day > 28:
            return False
        return True
    
    
    def is_changed(self, new_date: list) -> bool:
        changed = False
        if self.day != int(new_date[0]):
            changed = True
        if self.month != self._month_to_id[new_date[1]]:
            changed = True
        if self.year != int(new_date[2]):
            changed = True
        if changed and not self._date_valid(int(new_date[0]), self._month_to_id[new_date[1]], int(new_date[2])):
            changed = False
        return changed
    
    
    def __str__(self) -> str:
        return f'{self.day}.{self.month}.{self.year}'
