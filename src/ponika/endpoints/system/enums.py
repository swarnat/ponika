from enum import Enum


class ButtonHandler(str, Enum):
    REBOOT = 'reboot'
    USER_DEFAULTS = 'default'
    FACTORY_DEFAULTS = 'firstboot'


class DeviceParameterType(str, Enum):
    EVENT = 'event'
    DEVICE = 'device'
    NETWORK = 'network'
    MOBILE = 'mobile'
    IO = 'io'
    OTHER = 'other'
