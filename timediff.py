
"""
    en utilisant le @staticmethod, pas de besoin de créer une instance de la classe avant d'utiliser cette méthode.

"""

class TimeDiff:

    def __init__(self):
        """ """

    @classmethod
    def time_to_dec(cls,t):
        hh = int(t/100)
        mm = round((t%100)/60*100)
        dec = int(str(hh)+str('{:02}'.format(mm)))
        return int(str(hh)), int(str('{:02}'.format(mm))), dec

    @classmethod
    def dec_to_time(cls,t):
        hh = int(t/100)
        mm = round((t%100)*60/100)
        dec = int(str(hh)+str('{:02}'.format(mm)))
        return int(str(hh)), int(str('{:02}'.format(mm))), dec

    @classmethod
    def offset(cls,hh,mm):
        dec_time = cls.time_to_dec(hh)
        dec_offset = round(mm/60*100)
        _offset = dec_time[2] + dec_offset 

        offset_time = _offset if _offset >= 0 else 2400 + _offset
        new_time = cls.dec_to_time(offset_time)
        return new_time

# End