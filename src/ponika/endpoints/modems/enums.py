from enum import IntEnum, StrEnum


class ModemMode(IntEnum):
    UNKNOWN = 0
    BUILTIN = 1
    USB = 2
    PCIE = 3


class ModemName(StrEnum):
    PRIMARY = 'Primary modem'
    SECONDARY = 'Secondary modem'
    EXTERNAL = 'External modem'
    INTERNAL = 'Internal modem'
    UNKNOWN = 'Unknown modem'


class SimState(StrEnum):
    INSERTED = 'Inserted'
    NOT_INSERTED = 'Not inserted'


class SimStateId(IntEnum):
    INSERTED = 0
    NOT_INSERTED = 1


class ConnectionState(StrEnum):
    CONNECTED = 'Connected'
    DISCONNECTED = 'Disconnected'
    UNKNOWN = 'Unknown'


class ConnectionStateId(IntEnum):
    CONNECTED = 0
    DISCONNECTED = 1
    UNKNOWN = 2


class PinState(StrEnum):
    INSERTED = 'Inserted'
    NOT_READY = 'Not ready'
    PIN_REQUIRED = 'Required PIN, X attempts left'
    PUK_REQUIRED = 'Required PUK, X attempts left'
    NOT_INSERTED = 'Not inserted'
    SIM_FAILURE = 'SIM failure'
    BUSY = 'Busy'
    PUK = 'PUK'


class PinStateId(IntEnum):
    INSERTED = 0
    NOT_READY = 1
    PIN_REQUIRED = 2
    PUK_REQUIRED = 4
    NOT_INSERTED = 5
    SIM_FAILURE = 10
    BUSY = 13
    PUK = 14
    UNKNOWN = 15


class RegistrationState(StrEnum):
    NOT_REGISTERED = 'Not registered'
    REGISTERED_HOME = 'Registered, home'
    SEARCHING = 'Searching'
    DENIED = 'Denied'
    UNKNOWN = 'Unknown'
    ROAMING = 'Roaming'


class RegistrationStateId(IntEnum):
    NOT_REGISTERED = 0
    REGISTERED_HOME = 1
    SEARCHING = 2
    DENIED = 3
    UNKNOWN = 4
    ROAMING = 5


class SecondaryCarrierBandState(StrEnum):
    INACTIVE = 'Inactive'
    ACTIVE = 'Active'


class MobileStage(IntEnum):
    STAGE_0 = 0
    STAGE_1 = 1
    STAGE_2 = 2
    STAGE_3 = 3
    STAGE_4 = 4
    STAGE_5 = 5
    STAGE_6 = 6
    STAGE_7 = 7
    STAGE_8 = 8
    STAGE_9 = 9
    STAGE_10 = 10
    STAGE_11 = 11
    STAGE_12 = 12
    STAGE_13 = 13
    STAGE_14 = 14
    STAGE_15 = 15
    STAGE_16 = 16
    STAGE_17 = 17
    STAGE_18 = 18
    STAGE_19 = 19
    STAGE_20 = 20
    STAGE_21 = 21
    STAGE_22 = 22
    STAGE_23 = 23


class ModemStateId(IntEnum):
    STATE_1 = 1
    STATE_2 = 2
    STATE_3 = 3
    STATE_4 = 4
    STATE_5 = 5


class NetworkType(IntEnum):
    TYPE_0 = 0
    TYPE_1 = 1
    TYPE_2 = 2
    TYPE_3 = 3
    TYPE_4 = 4
    TYPE_5 = 5
    TYPE_6 = 6
    TYPE_7 = 7
    TYPE_8 = 8
    TYPE_9 = 9
    TYPE_10 = 10
    TYPE_11 = 11
    TYPE_12 = 12
    TYPE_13 = 13
    TYPE_14 = 14
    TYPE_15 = 15
    TYPE_16 = 16
    TYPE_17 = 17
    TYPE_18 = 18
    TYPE_19 = 19
    TYPE_20 = 20
    TYPE_21 = 21
    TYPE_22 = 22
    TYPE_23 = 23
    TYPE_24 = 24
    TYPE_25 = 25
    TYPE_26 = 26
    TYPE_27 = 27
    TYPE_28 = 28
    TYPE_29 = 29
    TYPE_30 = 30
    TYPE_31 = 31
    TYPE_32 = 32
    TYPE_33 = 33
    TYPE_34 = 34
    TYPE_35 = 35
    TYPE_36 = 36
    TYPE_37 = 37
    TYPE_38 = 38
    TYPE_39 = 39


class ApnAuthentication(StrEnum):
    NONE = 'none'
    PAP = 'pap'
    CHAP = 'chap'


class PdpType(StrEnum):
    IPV4 = '0'
    IPV6 = '1'
    IPV4_IPV6 = '2'


class OperatorStatus(StrEnum):
    AVAILABLE = 'Available'
    CURRENT = 'Current'
    FORBIDDEN = 'Forbidden'
    UNKNOWN = 'Unknown'


class UssdState(IntEnum):
    COMPLETE = 0
    ACTION_REQUIRED = 1
    TERMINATED = 2
    OTHER_CLIENT_RESPONDED = 3
    NOT_SUPPORTED = 4
    NETWORK_TIMEOUT = 5


class VolteMode(StrEnum):
    AUTO = 'auto'
    ON = 'on'
    OFF = 'off'


class MobileService(StrEnum):
    GSM = '2g'
    UMTS_PREFERRED = '3g_pref'
    UMTS = '3g'
    LTE_PREFERRED = 'lte_pref'
    LTE = 'lte'
    NR5G_PREFERRED = 'nr5g_pref'


class LteCategory(StrEnum):
    CAT_M1 = 'm1'
    NARROWBAND = 'nb'
    CAT_M1_NARROWBAND = 'm1_nb'


class Nr5gMode(StrEnum):
    AUTO = 'auto'
    NSA = 'nsa'
    SA = 'sa'


class BandSelection(StrEnum):
    AUTO = 'auto'
    MANUAL = 'manual'


class OperatorListMode(StrEnum):
    WHITELIST = 'whitelist'
    BLACKLIST = 'blacklist'


class SmsLimitPeriod(StrEnum):
    DAY = 'day'
    WEEK = 'week'
    MONTH = 'month'


class OperatorSelection(StrEnum):
    AUTO = 'auto'
    MANUAL = 'manual'
    MANUAL_AUTO = 'manual-auto'


class GsmBand(StrEnum):
    ALL = 'all'
    GSM_850 = 'gsm_850'
    GSM_900 = 'gsm_900'
    GSM_1800 = 'gsm_1800'
    GSM_1900 = 'gsm_1900'


class UmtsBand(StrEnum):
    ALL = 'all'
    WCDMA_800 = 'wcdma_800'
    WCDMA_850 = 'wcdma_850'
    WCDMA_900 = 'wcdma_900'
    WCDMA_1700 = 'wcdma_1700'
    WCDMA_1800 = 'wcdma_1800'
    WCDMA_1900 = 'wcdma_1900'
    WCDMA_2100 = 'wcdma_2100'


class LteBand(StrEnum):
    ALL = 'all'
    B1 = 'lte_b1'
    B2 = 'lte_b2'
    B3 = 'lte_b3'
    B4 = 'lte_b4'
    B5 = 'lte_b5'
    B7 = 'lte_b7'
    B8 = 'lte_b8'
    B12 = 'lte_b12'
    B13 = 'lte_b13'
    B14 = 'lte_b14'
    B17 = 'lte_b17'
    B18 = 'lte_b18'
    B19 = 'lte_b19'
    B20 = 'lte_b20'
    B25 = 'lte_b25'
    B26 = 'lte_b26'
    B28 = 'lte_b28'
    B29 = 'lte_b29'
    B30 = 'lte_b30'
    B32 = 'lte_b32'
    B34 = 'lte_b34'
    B38 = 'lte_b38'
    B39 = 'lte_b39'
    B40 = 'lte_b40'
    B41 = 'lte_b41'
    B42 = 'lte_b42'
    B43 = 'lte_b43'
    B48 = 'lte_b48'
    B66 = 'lte_b66'
    B71 = 'lte_b71'


class LteNbBand(StrEnum):
    ALL = 'all'
    B1 = 'lte_nb1'
    B2 = 'lte_nb2'
    B3 = 'lte_nb3'
    B4 = 'lte_nb4'
    B5 = 'lte_nb5'
    B8 = 'lte_nb8'
    B12 = 'lte_nb12'
    B13 = 'lte_nb13'
    B18 = 'lte_nb18'
    B19 = 'lte_nb19'
    B20 = 'lte_nb20'
    B26 = 'lte_nb26'
    B28 = 'lte_nb28'


class Nr5gBand(StrEnum):
    ALL = 'all'
    N1 = '1'
    N2 = '2'
    N3 = '3'
    N4 = '4'
    N5 = '5'
    N7 = '7'
    N8 = '8'
    N12 = '12'
    N20 = '20'
    N25 = '25'
    N28 = '28'
    N38 = '38'
    N40 = '40'
    N41 = '41'
    N48 = '48'
    N66 = '66'
    N71 = '71'
    N77 = '77'
    N78 = '78'
    N79 = '79'
    N257 = '257'
    N258 = '258'
    N260 = '260'
    N261 = '261'
