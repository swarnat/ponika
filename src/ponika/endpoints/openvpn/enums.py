from enum import Enum


class OpenvpnType(str, Enum):
    CLIENT = 'client'
    SERVER = 'server'


class OpenvpnConfiguration(str, Enum):
    MANUAL = 'manual'
    CUSTOM = 'custom'
    EXTERNAL = 'external'


class OpenvpnAuthMode(str, Enum):
    STATIC_KEY = 'skey'
    TLS = 'tls'
    TLS_PASSWORD = 'tls/pass'
    PASSWORD = 'pass'


class OpenvpnDevice(str, Enum):
    TUN = 'tun'
    TAP = 'tap'


class OpenvpnTopology(str, Enum):
    NET30 = 'net30'
    P2P = 'p2p'
    SUBNET = 'subnet'


class OpenvpnProtocol(str, Enum):
    UDP = 'udp'
    UDP6 = 'udp6'
    TCP_CLIENT = 'tcp-client'
    TCP_SERVER = 'tcp-server'
    TCP6_CLIENT = 'tcp6-client'
    TCP6_SERVER = 'tcp6-server'


class OpenvpnCompression(str, Enum):
    YES = 'yes'
    NO = 'no'
    DISABLED = ''
    ADAPTIVE = 'adaptive'


class OpenvpnCipher(str, Enum):
    DES_CBC = 'DES-CBC'
    RC2_CBC = 'RC2-CBC'
    DES_EDE_CBC = 'DES-EDE-CBC'
    DES_EDE3_CBC = 'DES-EDE3-CBC'
    DESX_CBC = 'DESX-CBC'
    BF_CBC = 'BF-CBC'
    RC2_40_CBC = 'RC2-40-CBC'
    CAST5_CBC = 'CAST5-CBC'
    RC2_64_CBC = 'RC2-64-CBC'
    AES_128_CBC = 'AES-128-CBC'
    AES_128_CFB = 'AES-128-CFB'
    AES_128_CFB1 = 'AES-128-CFB1'
    AES_128_CFB8 = 'AES-128-CFB8'
    AES_128_OFB = 'AES-128-OFB'
    AES_128_GCM = 'AES-128-GCM'
    AES_192_CFB = 'AES-192-CFB'
    AES_192_CFB1 = 'AES-192-CFB1'
    AES_192_CFB8 = 'AES-192-CFB8'
    AES_192_OFB = 'AES-192-OFB'
    AES_192_CBC = 'AES-192-CBC'
    AES_192_GCM = 'AES-192-GCM'
    AES_256_GCM = 'AES-256-GCM'
    AES_256_CFB = 'AES-256-CFB'
    AES_256_CFB1 = 'AES-256-CFB1'
    AES_256_CFB8 = 'AES-256-CFB8'
    AES_256_OFB = 'AES-256-OFB'
    AES_256_CBC = 'AES-256-CBC'
    NONE = 'none'


class OpenvpnAuth(str, Enum):
    NONE = 'none'
    MD5 = 'md5'
    SHA1 = 'sha1'
    SHA256 = 'sha256'
    SHA384 = 'sha384'
    SHA512 = 'sha512'


class OpenvpnTlsSecurity(str, Enum):
    NONE = 'none'
    TLS_AUTH = 'tls-auth'
    TLS_CRYPT = 'tls-crypt'


class OpenvpnDh(str, Enum):
    NONE = 'none'
    DH_FILE_PATH = 'dh_file_path'


class OpenvpnConfigParsed(str, Enum):
    NOT_PARSED = '0'
    PARSED = '1'
    PARSE_FAILED = '2'


class OpenvpnExternalService(str, Enum):
    EXPRESS = 'express'
    NORD = 'nord'


class OpenvpnServerList(str, Enum):
    UK = 'uk'
    USA = 'usa'
    AUS = 'aus'
    SA = 'sa'
    CUSTOM = 'custom'


class OpenvpnTlsCipherList(str, Enum):
    ALL = 'all'
    DHE_RSA = 'dhe_rsa'
    CUSTOM = 'custom'


class OpenvpnTlsCipher(str, Enum):
    TLS_DHE_RSA_WITH_AES_256_GCM_SHA384 = 'TLS-DHE-RSA-WITH-AES-256-GCM-SHA384'
    TLS_DHE_RSA_WITH_AES_256_CBC_SHA = 'TLS-DHE-RSA-WITH-AES-256-CBC-SHA'
    TLS_DHE_RSA_WITH_AES_256_CBC_SHA256 = 'TLS-DHE-RSA-WITH-AES-256-CBC-SHA256'
    TLS_DHE_RSA_WITH_CAMELLIA_256_CBC_SHA = (
        'TLS-DHE-RSA-WITH-CAMELLIA-256-CBC-SHA'
    )
    TLS_DHE_RSA_WITH_3DES_EDE_CBC_SHA = 'TLS-DHE-RSA-WITH-3DES-EDE-CBC-SHA'
    TLS_DHE_RSA_WITH_AES_128_GCM_SHA256 = 'TLS-DHE-RSA-WITH-AES-128-GCM-SHA256'
    TLS_DHE_RSA_WITH_AES_128_CBC_SHA = 'TLS-DHE-RSA-WITH-AES-128-CBC-SHA'
    TLS_DHE_RSA_WITH_AES_128_CBC_SHA256 = 'TLS-DHE-RSA-WITH-AES-128-CBC-SHA256'
    TLS_DHE_RSA_WITH_SEED_CBC_SHA = 'TLS-DHE-RSA-WITH-SEED-CBC-SHA'
    TLS_DHE_RSA_WITH_CAMELLIA_128_CBC_SHA = (
        'TLS-DHE-RSA-WITH-CAMELLIA-128-CBC-SHA'
    )
    TLS_DHE_RSA_WITH_DES_CBC_SHA = 'TLS-DHE-RSA-WITH-DES-CBC-SHA'
