import datetime as _dt

DATETIME_EPOCH = _dt.datetime(year=1984, month=1, day=1)
EPOC_EPOCH = 6011.0

EPOC_MIN = 5949
EPOC_MAX = 9999

_days_per_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

class datetime:
    def __init__(self, epoc, sinister, medius, dexter=0, fraction=0):
        if not isinstance(epoc, int):
            raise TypeError(f"'epoc must be an 'int', not a '{type(epoc).__name__}'")
        if epoc not in range(EPOC_MIN, EPOC_MAX+1):
            raise ValueError(f"'epoc must be between '{EPOC_MIN}' and '{EPOC_MAX}', not '{epoc}'")
        self.epoc = epoc
        
        if not isinstance(sinister, int):
            raise TypeError(f"'sinister' must be an 'int', not a '{type(sinister).__name__}'")
        if sinister not in range(0, 1000):
            raise ValueError(f"'sinister' must be between '0' and '999', not '{sinister}'")
        self.sinister = sinister
        
        if not isinstance(medius, int):
            raise TypeError(f"'medius' must be an 'int', not a '{type(medius).__name__}'")
        if medius not in range(0, 1000):
            raise ValueError(f"'medius' must be between '0' and '999', not '{medius}'")
        self.medius = medius
        
        if not isinstance(dexter, int):
            raise TypeError(f"'dexter' must be an 'int', not a '{type(dexter).__name__}'")
        if dexter not in range(0, 1000):
            raise ValueError(f"'dexter' must be between '0' and '999', not '{dexter}'")
        self.dexter = dexter
        
        if not isinstance(fraction, int):
            raise TypeError(f"'fraction' must be an 'int', not a '{type(fraction).__name__}'")
        if fraction not in range(0, 1000):
            raise ValueError(f"'fraction' must be between '0' and '999', not '{fraction}'")
        self.fraction = fraction
    
    def __repr__(self):
        return self.strftime("feltime.datetime(%e, %s, %m, %d, %f)")
    
    def __str__(self):
        return self.strftime("%e:%S.%M.%D")
    
    def __add__(self, other):
        if isinstance(other, _dt.timedelta):
            return self.from_real_time(self.to_real_time() + other)
        else:
            raise TypeError(f"unsupported operand type(s) for +: 'feltime.datetime' and '{type(other).__name__}'")
    
    def __sub__(self, other):
        if isinstance(other, datetime):
            return self.to_real_time() - other.to_real_time()
        elif isinstance(other, _dt.timedelta) or isinstance(other, _dt.datetime):
            return self.from_real_time(self.to_real_time() - other)
        else:
            raise TypeError(f"unsupported operand type(s) for -: 'feltime.datetime' and '{type(other).__name__}'")
    
    @classmethod
    def from_real_time(cls, dt):
        if not isinstance(dt, _dt.datetime):
            raise TypeError(f"'dt' must be a 'datetime.datetime object', not a '{type(dt).__name__}'")
        
        '''
        There are various bugs in the time calculation in Noctis. The epoc is
        supposed to be computed as:
            epoc = (number_of_seconds_since_1984 / 1e9) + 6011
        
        However, due to faulty leap year logic, every year which is not a leap
        year will actually be 1 day in the past. Then, at the start of the next
        leap year, it will gain a day to be accurate again, only to lose it
        after the year ends.
        
        To reproduce the behavior of the game as accurately as possible, I have
        ported the getsecs() function literally. If the time bugs were not
        present, I could simply do the following instead:
            epoc_raw = EPOC_EPOCH + ((dt - DATETIME_EPOCH).total_seconds() / 1e9)
        '''
        
        years = dt.year - DATETIME_EPOCH.year  # years since 1984
        days = (years * 365) + (years // 4)  # years * 365 + years / 4
        
        m = 1
        while m < dt.month:
            days += _days_per_month[m-1]  # days per month
            m += 1
        
        if (dt.month > 2) and (dt.year % 4 == 0):  # if it's a leap year
            days += 1
        
        days += dt.day - 1  # + current day of the month
        seconds = days * 86400  # seconds in a day
        
        seconds += 3600 * dt.hour  # current hour in seconds
        seconds += 60 * dt.minute  # current minute in seconds

        seconds += dt.second  # current seconds
        
        seconds += dt.microsecond / 1e6  # fraction of a second

        epoc_raw = 6011 + (seconds / 1e9)
        
        # Split the raw epoc into parts
        epoc, triad = f"{epoc_raw:.12f}".split(".")
        
        return cls(
            epoc = int(epoc),
            sinister = int(triad[0:3]),
            medius = int(triad[3:6]),
            dexter = int(triad[6:9]),
            fraction = int(triad[9:12])
        )
    
    @classmethod
    def from_timestamp(cls, ts):
        if not isinstance(ts, float) and not isinstance(ts, int):
            raise TypeError(f"'ts' must be a 'float' or 'int', not a '{type(ts).__name__}'")
        if ts not in range(EPOC_MIN, EPOC_MAX+1):
            raise ValueError(f"'ts must be between '{EPOC_MIN}' and '{EPOC_MAX}', not '{ts}'")
            
        return cls.from_real_time(cls.to_real_time(cls, ts))
    
    @classmethod
    def now(cls):
        return cls.from_real_time(_dt.datetime.now())
    
    @property
    def epoc_raw(self):
        return self.epoc + (self.sinister / 1e3) + (self.medius / 1e6) + (self.dexter / 1e9) + (self.fraction / 1e12)
    
    def timestamp(self):
        return self.epoc_raw * 1e9
    
    def to_real_time(self, epoc_raw=None):
        if epoc_raw == None:
            epoc_raw = self.epoc_raw
        if not isinstance(epoc_raw, float) and not isinstance(epoc_raw, int):
            raise TypeError(f"'epoc_raw' must be a 'float' or 'int', not a '{type(epoc_raw).__name__}'")
        
        '''
        There are various bugs in the time calculation in Noctis. The epoc is
        supposed to be computed as:
            epoc = (number_of_seconds_since_1984 / 1e9) + 6011
        
        However, due to faulty leap year logic, every year which is not a leap
        year will actually be 1 day in the past. Then, at the start of the next
        leap year, it will gain a day to be accurate again, only to lose it
        after the year ends.
        
        To reproduce the behavior of the game as accurately as possible, I have
        ported the getsecs() function literally. I then had to derive the
        inverse of that function below. If the time bugs were not present, I
        could simply do the following instead:
            dt = DATETIME_EPOCH + _dt.timedelta(seconds=(epoc_raw - EPOC_EPOCH) * 1e9)
        '''
        # Seconds since 1984
        seconds = (epoc_raw - EPOC_EPOCH) * 1e9
        
        # Split off the fraction of a second
        microsecond = int((seconds % 1) * 1e6)
        seconds = int(seconds)
        
        # Split off hour + minute + second and the remaining days component
        seconds_in_day = seconds % 86400
        days = seconds // 86400
        
        hour = seconds_in_day // 3600
        minute = (seconds_in_day % 3600) // 60
        second = seconds_in_day % 60
        
        # Split off the year
        year = DATETIME_EPOCH.year
        while True:
            years = (year + 1) - DATETIME_EPOCH.year
            next_year_days = (years * 365) + (years // 4)
            if next_year_days > days:
                break
            year += 1
        
        years = year - DATETIME_EPOCH.year
        days -= (years * 365) + (years // 4)
        
        # Split off the month
        month = 1
        while month < 12:
            next_month_days = _days_per_month[month - 1]
            
            if month == 2 and (year % 4 == 0):
                next_month_days += 1
                
            if days >= next_month_days:
                days -= next_month_days
                month += 1
            else:
                break
        
        # Split off the day
        day = days + 1
        
        return _dt.datetime(
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
            second=second,
            microsecond=microsecond,
        )
    
    def strftime(self, format):
        '''
        %e = epoc
        %s = sinister
        %m = medius
        %d = dexter
        %f = fraction
        %S = sinister, zero-padded
        %M = medius, zero-padded
        %D = dexter, zero-padded
        %D = fraction, zero-padded
        %t = triad (SSS.MMM.DDD)
        %c = complete timestamp (EEEE:SSS.MMM.DDD)
        %% = % (escaped)
        '''
        if not isinstance(format, str):
            raise TypeError(f"'format' must be a 'str', not a '{type(epoc_raw).__name__}'")
        
        out_string = ""
        i = 0
        while i < len(format):
            if format[i] == "%":
                if i+1 >= len(format):
                    raise Exception("% must be followed by another character (cannot be at the very end of the format string)")
                
                match format[i+1]:
                    case "e":
                        out_string += str(self.epoc)
                    case "s":
                        out_string += str(self.sinister)
                    case "m":
                        out_string += str(self.medius)
                    case "d":
                        out_string += str(self.dexter)
                    case "f":
                        out_string += str(self.fraction)
                    case "S":
                        out_string += f"{self.sinister:03d}"
                    case "M":
                        out_string += f"{self.medius:03d}"
                    case "D":
                        out_string += f"{self.dexter:03d}"
                    case "F":
                        out_string += f"{self.fraction:03d}"
                    case "t":
                        out_string += f"{self.sinister:03d}.{self.medius:03d}.{self.dexter:03d}"
                    case "c":
                        out_string += f"{self.epoc}:{self.sinister:03d}.{self.medius:03d}.{self.dexter:03d}"
                    case "%":
                        out_string += "%"
                    case _:
                        raise Exception(f"Formatting character not recognized: %{format[i+1]}")
                i += 1
            else:
                out_string += format[i]
            i += 1
        
        return out_string
