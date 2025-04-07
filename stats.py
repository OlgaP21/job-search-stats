class Stats:
    
    # total, responded, not responded, TBD
    _total_applications = [0, 0, 0, 0]
    _cvkeskus_applications = [0, 0, 0, 0]
    _cvee_applications = [0, 0, 0, 0]
    _tootukassa_applications = [0, 0, 0, 0]
    _letters_applications = [0, 0, 0, 0]
    _other_applications = [0, 0, 0, 0]
    
    
    # Method for updating Source statistics
    @staticmethod
    def update(source: str, new_status: int, old_status: int=None, delete=False) -> None:
        if source == 'CVKeskus':
            Stats._update_cvkeskus(new_status, old_status, delete)
        elif source == 'cv.ee':
            Stats._update_cvee(new_status, old_status, delete)
        elif source == 'Töötukassa':
            Stats._update_tootukassa(new_status, old_status, delete)
        elif source == 'E-kiri':
            Stats._update_letters(new_status, old_status, delete)
        elif source == 'Muu':
            Stats._update_other(new_status, old_status, delete)


    # Method for updating Kokku statistics
    @staticmethod
    def _update_total(new_status: int, old_status: int=None, delete=False) -> None:
        if delete:
            Stats._total_applications[new_status] -= 1
            Stats._total_applications[0] -= 1
        else:
            Stats._total_applications[new_status] += 1
            if old_status:
                Stats._total_applications[old_status] -= 1
            else:
                Stats._total_applications[0] += 1
    
    
    # Method for updating CVKeskus statistics
    @staticmethod
    def _update_cvkeskus(new_status: int, old_status: int=None, delete=False) -> None:
        if delete:
            Stats._cvkeskus_applications[new_status] -= 1
            Stats._cvkeskus_applications[0] -= 1
            Stats._update_total(new_status, delete=True)
        else:
            Stats._cvkeskus_applications[new_status] += 1
            if old_status:
                Stats._cvkeskus_applications[old_status] -= 1
                Stats._update_total(new_status, old_status)
            else:
                Stats._cvkeskus_applications[0] += 1
                Stats._update_total(new_status)
    
    
    # Method for updating cv.ee statistics
    @staticmethod
    def _update_cvee(new_status: int, old_status: int=None, delete=False) -> None:
        if delete:
            Stats._cvee_applications[new_status] -= 1
            Stats._cvee_applications[0] -= 1
            Stats._update_total(new_status, delete=True)
        else:
            Stats._cvee_applications[new_status] += 1
            if old_status:
                Stats._cvee_applications[old_status] -= 1
                Stats._update_total(new_status, old_status)
            else:
                Stats._cvee_applications[0] += 1
                Stats._update_total(new_status)
    
    
    # Method for updating Töötukassa statistics
    @staticmethod
    def _update_tootukassa(new_status: int, old_status: int=None, delete=False) -> None:
        if delete:
            Stats._tootukassa_applications[new_status] -= 1
            Stats._tootukassa_applications[0] -= 1
            Stats._update_total(new_status, delete=True)
        else:
            Stats._tootukassa_applications[new_status] += 1
            if old_status:
                Stats._tootukassa_applications[old_status] -= 1
                Stats._update_total(new_status, old_status)
            else:
                Stats._tootukassa_applications[0] += 1
                Stats._update_total(new_status)
    
    
    # Method for updating E-kiri statistics
    @staticmethod
    def _update_letters(new_status: int, old_status: int=None, delete=False) -> None:
        if delete:
            Stats._letters_applications[new_status] -= 1
            Stats._letters_applications[0] -= 1
            Stats._update_total(new_status, delete=True)
        else:
            Stats._letters_applications[new_status] += 1
            if old_status:
                Stats._letters_applications[old_status] += 1
                Stats._update_total(new_status, old_status)
            else:
                Stats._letters_applications[0] += 1
                Stats._update_total(new_status)
    
    
    # Method for updating Muu statistics
    @staticmethod
    def _update_other(new_status: int, old_status: int=None, delete=False) -> None:
        if delete:
            Stats._other_applications[new_status] -= 1
            Stats._other_applications[0] -= 1
            Stats._update_total(new_status, delete=True)
        else:
            Stats._other_applications[new_status] += 1
            if old_status:
                Stats._other_applications[old_status] -= 1
                Stats._update_total(new_status, old_status)
            else:
                Stats._other_applications[0] += 1
                Stats._update_total(new_status)
    
    
    # Methood for calculating Source:
    ## percent of total
    ## responded percent of Source total
    ## not responded percent of source total
    ## tbd percent of Source total
    # For Kokku it is overall statistics
    # For Source it is internal statistics for this particular Source
    @staticmethod
    def get_percent(source: str) -> list[float]:
        if source == 'CVKeskus':
            total, responded, not_responded, tbd = Stats._cvkeskus_applications
        elif source == 'cv.ee':
            total, responded, not_responded, tbd = Stats._cvee_applications
        elif source == 'Töötukassa':
            total, responded, not_responded, tbd = Stats._tootukassa_applications
        elif source == 'E-kiri':
            total, responded, not_responded, tbd = Stats._letters_applications
        elif source == 'Muu':
            total, responded, not_responded, tbd = Stats._other_applications
        elif source == 'Kokku':
            total, responded, not_responded, tbd = Stats._total_applications
        
        if Stats._total_applications[0] == 0:
            total_percent = 0
        else:
            total_percent = round(total / Stats._total_applications[0] * 100, 2)
        
        if total == 0:
            responded_percent, not_responded_percent, tbd_percent = 0, 0, 0
        else:
            responded_percent = round(responded / total * 100, 2)
            not_responded_percent = round(not_responded / total * 100, 2)
            tbd_percent = round(tbd / total * 100, 2)
        return [total_percent, responded_percent, not_responded_percent, tbd_percent]
    
    
    # Method for getting Source numbers for Source:
    ## total
    ## responded
    ## not responded
    ## tbd
    @staticmethod
    def get_numbers(source: str) -> list[int]:
        if source == 'CVKeskus':
            return Stats._cvkeskus_applications
        if source == 'cv.ee':
            return Stats._cvee_applications
        if source == 'Töötukassa':
            return Stats._tootukassa_applications
        if source == 'E-kiri':
            return Stats._letters_applications
        if source ==  'Muu':
            return Stats._other_applications
        if source == 'Kokku':
            return Stats._total_applications
