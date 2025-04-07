import os
import pickle
from application import Application
from stats import Stats


class Data:
    
    _directory = os.getcwd() + '\\data'
    
    _cvkeskus_file = os.getcwd() + '\\data\\cvkeskus_data.pkl'
    _cvee_file = os.getcwd() + '\\data\\cvee_data.pkl'
    _tootukassa_file = os.getcwd() + '\\data\\tootukassa_data.pkl'
    _letter_file = os.getcwd() + '\\data\\letter_data.pkl'
    _other_file = os.getcwd() + '\\data\\other_data.pkl'
    
    _status_to_index = {
        'Eitav vastus': 1,
        'Vastust pole': 2,
        'TBD': 3
    }
    
    _source = ''
    _current_file = ''
    
    
    @staticmethod
    def setup():
        if not os.path.exists(Data._directory):
            os.makedirs(Data._directory)
    
    
    # Method for loading specified Source data from the file
    @staticmethod
    def load_data(source: str) -> list[str] | bool:
        Data._get_filename(source)
        return Data._load_from_file(Data._current_file)
    
    
    # Method to get appropriate filename from Source name
    @staticmethod
    def _get_filename(source: str) -> None:
        Data._source = source
        if source == 'CVKeskus':
            Data._current_file = Data._cvkeskus_file
        elif source == 'cv.ee':
            Data._current_file = Data._cvee_file
        elif source == 'Töötukassa':
            Data._current_file = Data._tootukassa_file
        elif source == 'E-kiri':
            Data._current_file = Data._letter_file
        elif source == 'Muu':
            Data._current_file = Data._other_file
    
    
    @staticmethod
    def _load_from_file(filename: str) -> list[str] | bool:
        if not Data._file_exists(filename):
            return False
        applications = []
        with open(filename, 'rb') as input_file:
            while True:
                try:
                    application = pickle.load(input_file)
                    applications.append(application.get_data())
                    status = Data._status_to_index[str(application.get_status())]
                    Stats.update(Data._source, status)
                except EOFError:
                    break
        return applications
    
    
    @staticmethod
    def _load_objects_data(source: str) -> list[str] | bool:
        Data._get_filename(source)
        return Data._load_objects_from_file(Data._current_file)
    
    
    @staticmethod
    def _load_objects_from_file(filename: str) -> list[Application] | bool:
        if not Data._file_exists(filename):
            return False
        applications = []
        with open(filename, 'rb') as input_file:
            while True:
                try:
                    application = pickle.load(input_file)
                    applications.append(application)
                except EOFError:
                    break
        return applications
    
    
    @staticmethod
    def _file_exists(filename: str) -> bool:
        return os.path.isfile(filename)
    
    
    @staticmethod
    def add_entry(application_data: list[str]) -> list[str]:
        source, day, month, year, title, company, status = application_data
        new_application = Application(source, day, month, year, title, company, status)
        Data._get_filename(source)
        Data._add_to_file(new_application)
        return new_application.get_data()
    
    
    @staticmethod
    def _add_to_file(application_to_add: Application) -> None:
        with open(Data._current_file, 'ab') as output_file:
            pickle.dump(application_to_add, output_file, pickle.HIGHEST_PROTOCOL)
        status = Data._status_to_index[str(application_to_add.get_status())]
        Stats.update(Data._source, status)
    
    
    @staticmethod
    def update_entry(source: str, index: int, application: list) -> None:
        applications = Data._load_objects_data(source)
        if applications:
            applications[index].set_date(application[1], application[2], application[3])
            applications[index].set_title(application[5])
            applications[index].set_company(application[6])
            old_status = Data._status_to_index[str(applications[index].get_status())]
            new_status = Data._status_to_index[application[4]]
            applications[index].set_status(application[4])
            Data._update_file(applications)
            Stats.update(Data._source, new_status, old_status)
    
    
    @staticmethod
    def delete_entry(source: str, index: int) -> None:
        applications = Data._load_objects_data(source)
        application_status = Data._status_to_index[str(applications[index].get_status())]
        applications.pop(index)
        Data._update_file(applications)
        Stats.update(Data._source, application_status, delete=True)
    
    
    @staticmethod
    def _update_file(updated_applications: list[Application]) -> None:
        with open(Data._current_file, 'wb') as output_file:
            for application_to_add in updated_applications:
                pickle.dump(application_to_add, output_file, pickle.HIGHEST_PROTOCOL)
