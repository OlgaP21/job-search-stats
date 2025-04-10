from date import Date
from status import Status
from source import Source


class Application:
    
    def __init__(self, source: str, day: str, month: str, year: str, title: str, company: str, status: str) -> None:
        self.source = Source.from_string(source)
        self.date = Date(int(day), month, int(year))
        self.title = title
        self.company = company
        self.status = Status.from_string(status)
    
    
    def get_source(self) -> Source:
        return self.source
    
    
    def set_source(self, source: str) -> None:
        self.source = Source.from_string(source)
    
    
    def check_source(self, source: str) -> bool:
        return self.source.value == source
    
    
    def get_date(self) -> Date:
        return self.date
    
    
    def set_date(self, day: str, month: str, year: str) -> None:
        self.date.set_date(int(day), month, int(year))
    
    
    def get_title(self) -> str:
        return self.title
    
    
    def set_title(self, title: str) -> None:
        self.title = title
    
    
    def get_company(self) -> str:
        return self.company
    
    
    def set_company(self, company: str) -> None:
        self.company = company
    
    
    def get_status(self) -> Status:
        return self.status
    
    
    def set_status(self, status: str) -> None:
        self.status = Status.from_string(status)
    
    
    def get_data(self) -> list:
        source_value = str(self.get_source())
        date_value = str(self.get_date())
        title_value = self.get_title()
        company_value = self.get_company()
        status_value = str(self.get_status())
        return [date_value, title_value, company_value, status_value]
    
    
    def update(self, data: list) -> bool:
        changed = False
        if self.date.is_changed(data[1:4]):
            self.date.set_date(int(data[1]), data[2], int(data[3]))
            changed = True
        if self.title != data[5]:
            self.set_title(data[5])
            changed = True
        if self.company != data[6]:
            self.set_company(data[6])
            changed = True
        if self.status != Status.from_string(data[4]):
            self.set_status(data[4])
            changed = True
        return changed
    
    
    def __str__(self) -> str:
        return f'{self.source}, {self.date}, {self.title}, {self.company}, {self.status}'
