from date import Date
from status import Status
from source import Source
import pickle


class Application:
    
    def __init__(self, source: str, day: str, month: str, year: str, title: str, company: str, status: str):
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
    
    
    def get_data(self):
        source_value = str(self.get_source())
        date_value = str(self.get_date())
        title_value = self.get_title()
        company_value = self.get_company()
        status_value = str(self.get_status())
        return [date_value, title_value, company_value, status_value]
    
    
    def __str__(self):
        return f'{self.source}, {self.date}, {self.title}, {self.company}, {self.status}'


# PICKLE DATA ~UPLOADING AND ~DOWNLOADING EXAMPLE
# with open('data.pkl', 'ab') as outp:
#     a1 = Application('cv.ee', '24', 'Detsember', '2024', 'Title', 'Company', 'TBD')
#     pickle.dump(a1, outp, pickle.HIGHEST_PROTOCOL)
#     
#     a2 = Application('CVKeskus', '25', 'Detsember', '2024', 'Other Title', 'Other Company', 'TBD')
#     pickle.dump(a2, outp, pickle.HIGHEST_PROTOCOL)
# 
# 
# 
# del a1
# del a2
# 
# with open('data.pkl', 'rb') as inp:
#     a1 = pickle.load(inp)
#     print(a1)
#     
#     a2 = pickle.load(inp)
#     print(a2)

# a1 = Application('cv.ee', '24', 'Detsember', '2024', 'Title', 'Company', 'TBD')
# print(str(a1.get_status()))
# print(type(str(a1.get_status())))
