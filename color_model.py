import math
import json
import http.client
from abc import ABCMeta, abstractmethod
from enum import Enum
from typing import List, Optional
from dataclasses import dataclass
from utils import find_color_name, ColorNotFoundException

@dataclass
class ConnectionInfo:
    """Mutable Connection Info"""
    host:str = "www.csscolorsapi.com"
    endpoint:str = "/api/colors/"

class MessageErrors(Enum):
    """Reserved messages for main errors"""
    FORMAT = "Wrong color format"
    LENGTH = "Wrong color length"
    HEX_DIGITS = "Wrong color hex digits"
    CONVERTATION = "Convertation error"
    JSON_DECODE  = "JSON Decode error"
    CONN_ERROR = "Host connection error"


class Color(metaclass=ABCMeta):
    """
    Abstrct class for Color, main idea to have different color format types in the future: 
        - RGB
        - HSL
        - LAB
        - HEX (implemented)

    Methods:
        __repr__ - magic method for representing color format type
        value - getter + setter for laziness and validation. We are assume that this value can be changed (color changed)
        brightness - storing brightness float value, also property due to laziness (because of the math operations)
        get_color_name - return color name from the host
    """
    @abstractmethod
    def __repr__(self) -> str:
        ...

    @property
    @abstractmethod
    def value(self) -> str:
        ...
    # Farbe kann Mutable sein + Lazy (langsam?)
    @value.setter
    @abstractmethod
    def value(self, color_str_format:str):
        ...

    # Lazy Feld
    @property
    @abstractmethod
    def brightness(self) -> float:
        ...
    @abstractmethod
    def get_color_name(self) -> str:
        ...

class HEXColor(Color):
    """Implementation of HEX color format"""
    def __init__(self, input_color: str) -> None:
        self.value = input_color
        self.color_name: Optional[str] = None
        self._brightness: Optional[float] = None

    @property
    def value(self) -> str:
        return self._value
    
    @value.setter
    def value(self, input_color: str) -> None:
        # Validations
        if len(input_color) != 7:
            raise ValueError(MessageErrors.LENGTH)
        if input_color[0] != "#":
            raise ValueError(MessageErrors.FORMAT)

        hex_part = input_color[1:]
        if not all(c in '0123456789ABCDEFabcdef' for c in hex_part):
            raise ValueError(MessageErrors.HEX_DIGITS)
        self._value = input_color
        # Color changed - brightness changed
        self._brightness = None

    @property
    def brightness(self) -> float:
        # check if exists
        if self._brightness:
            return self._brightness
        R,G,B = self.HEXtoRGBAdapter()
        self._brightness = round(math.sqrt(0.241*(R**2) + 0.691 *(G**2) + 0.068*(B**2)), 2)
        return self._brightness

    def get_color_name(self):
        if self.color_name:
            return color_name
        # Some web logic goes here, would be a good idea to move it away in utils in the future
        conn = http.client.HTTPSConnection(ConnectionInfo().host)
        try:
            conn.request("GET", ConnectionInfo().endpoint)
        # Socket io exceptions and https exceptions???
        except Exception as e:
            raise ConnectionError(MessageErrors.CONN_ERROR)

        response = conn.getresponse()


        data = response.read()
        data_str = data.decode("utf-8")

        try:
            json_data = json.loads(data_str)
            data = json_data["colors"]
        except json.JSONDecodeError as e:
            raise e        
        conn.close()

        try:
            color_value = self._value[1:].lower()
            # find_color_name - simple loop algorithm in utils.py 
            color_name = find_color_name(color_value, repr(self), data)
        except ColorNotFoundException:
            return ""

        self.color_name = color_name
        return color_name

    def __repr__(self) -> str:
        return "hex"
    
    def HEXtoRGBAdapter(self) -> tuple:
        """Custom adapter for converting HEX color format type into RGB. Should be implemented as a class"""
        try:
            R = int(self._value[1:3], 16)
            G = int(self._value[3:5], 16)
            B = int(self._value[5:7], 16)
        except ValueError as e:
            return ValueError([MessageErrors.CONVERTATION,e])
        return (R,G,B)

class ColorFactory(metaclass=ABCMeta):
    """Abstract factory for creating Color objects without specifying their concrete classes + different generating approaches: 
        - single instance of HEXColor - create_hex_color()
        - list of instances of HEXColor - create_list_hex_colors()"""
    @abstractmethod
    def create_hex_color(self) -> Color:
        return HEXColor
    
    @abstractmethod
    def create_list_hex_colors(self) -> List[Color]:
        ...
    
class HEXColorFactory(ColorFactory):
    """HEXColor factory implementation"""
    def create_hex_color(self, input_color: str) -> HEXColor:
        return HEXColor(input_color)

    def create_list_hex_colors(self, input_colors: List[str]) -> List[HEXColor]:
        return [self.create_hex_color(color) for color in input_colors]