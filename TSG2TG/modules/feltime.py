import datetime

DATETIME_EPOCH = datetime.datetime(year=1984, month=1, day=2, second=1)
TIMESTAMP_EPOCH = 6011.0

class feltime:
    def __init__(self, epoc, sinister, medius, dexter=0, fraction=0):
        self.epoc = epoc
        self.sinister = sinister
        self.medius = medius
        self.dexter = dexter
        self.fraction = fraction
    
    def __repr__(self):
        return self.strftime("feltime(%e, %s, %m, %d, %f)")
    
    def __str__(self):
        return self.strftime("%e:%S.%M.%D")
    
    def __add__(self, other):
        if isinstance(other, datetime.timedelta):
            return self.from_datetime(self.to_datetime() + other)
        else:
            raise TypeError(f"unsupported operand type(s) for +: 'feltime' and '{type(other).__name__}'")
    
    def __sub__(self, other):
        if isinstance(other, feltime):
            return self.to_datetime() - other.to_datetime()
        elif isinstance(other, datetime.timedelta) or isinstance(other, datetime.datetime):
            return self.from_datetime(self.to_datetime() - other)
        else:
            raise TypeError(f"unsupported operand type(s) for -: 'feltime' and '{type(other).__name__}'")
    
    @classmethod
    def from_datetime(cls, dt):
        epoc_raw = TIMESTAMP_EPOCH + ((dt - DATETIME_EPOCH).total_seconds() / 1e9)
    
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
        return cls.from_datetime(cls.to_datetime(cls, ts))
    
    @classmethod
    def now(cls):
        return cls.from_datetime(datetime.datetime.now())
    
    @property
    def epoc_raw(self):
        return self.epoc + (self.sinister / 1e3) + (self.medius / 1e6) + (self.dexter / 1e9) + (self.fraction / 1e12)
    
    def timestamp(self):
        return self.epoc_raw * 1e9
    
    def to_datetime(self, epoc_raw=None):
        if epoc_raw == None:
            epoc_raw = self.epoc_raw
        return DATETIME_EPOCH + datetime.timedelta(seconds=(epoc_raw - TIMESTAMP_EPOCH) * 1e9)
    
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
