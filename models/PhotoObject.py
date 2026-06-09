from datetime import datetime

class PhotoObject:
    def __init__(self, name: str, size: int, date: datetime) -> None:
        self.__name = name
        self.__size = size
        self.__date = date
        
    def get_name(self) -> str:
        return self.__name
    
    def get_size(self) -> str:
        return self.__size
    
    def get_date(self) -> datetime:
        return self.__date