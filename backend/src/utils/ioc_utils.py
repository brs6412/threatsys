from enum import Enum
import hashlib
import re
import ipaddress
from email_validator import validate_email, EmailNotValidError
import validators
import ipaddress

class IOCTypeEnum(str, Enum):
    """Enumeration of supported IOC types"""
    IPV4_ADDR = "ipv4_addr"
    IPV6_ADDR = "ipv6_addr"
    DOMAIN = "domain"
    EMAIL = "email"
    FILE_HASH_MD5 = "file_hash_md5"
    FILE_HASH_SHA1 = "file_hash_sha1"
    FILE_HASH_SHA256 = "file_hash_sha256"
    FILE_HASH_SHA512 = "file_hash_sha512"
    URL = "url"
    MUTEX = "mutex"
    REGISTRY_KEY = "registry_key"
    YARA_RULE = "yara_rule"

class IOCUtils:
    """Utils for handling different IOC types and hashing requirements"""
    
    def is_domain(value: str) -> bool:
        return validators.domain(value) is True

    def is_ipv4(value: str) -> bool:
        try:
            return isinstance(ipaddress.ip_address(value), ipaddress.IPv4Address)
        except ValueError:
            return False

    def is_ipv6(value: str) -> bool:
        try:
            return isinstance(ipaddress.ip_address(value), ipaddress.IPv6Address)
        except ValueError:
            return False

    def is_email(value: str) -> bool:
        try:
            validate_email(value, check_deliverability=False)
            return True
        except EmailNotValidError:
            return False
        
    HASH_TYPES = {
        IOCTypeEnum.FILE_HASH_MD5,
        IOCTypeEnum.FILE_HASH_SHA1,
        IOCTypeEnum.FILE_HASH_SHA256,
        IOCTypeEnum.FILE_HASH_SHA512
    }

    HASH_PATTERNS = {
        IOCTypeEnum.FILE_HASH_MD5: re.compile(r'^[a-fA-F0-9]{32}$'),
        IOCTypeEnum.FILE_HASH_SHA1: re.compile(r'^[a-fA-F0-9]{40}$'),
        IOCTypeEnum.FILE_HASH_SHA256: re.compile(r'^[a-fA-F0-9]{64}$'),
        IOCTypeEnum.FILE_HASH_SHA512: re.compile(r'^[a-fA-F0-9]{128}$'),
    }
        
    NON_HASH_PATTERNS = {
        IOCTypeEnum.DOMAIN: is_domain,
        IOCTypeEnum.IPV4_ADDR: is_ipv4,
        IOCTypeEnum.IPV6_ADDR: is_ipv6,
        IOCTypeEnum.EMAIL: is_email
    }

    @classmethod
    def validate_value(self, ioc_type_name: str, value: str) -> bool:
        """Validate IOC value against its specific pattern"""
        try:
            ioc_type = IOCTypeEnum(ioc_type_name.lower())
        except:
            return True
        
        if ioc_type in self.HASH_PATTERNS:
            return bool(self.HASH_PATTERNS[ioc_type].match(value))
        elif ioc_type in self.NON_HASH_PATTERNS:
            return bool(self.NON_HASH_PATTERNS[ioc_type](value))
        
        return True
    
    @classmethod
    def compute_hash(self, ioc_type_name: str, value: str) -> str:
        """Check ioc_type and compute SHA-256 hash if a non-hash type"""
        try:
            ioc_type = IOCTypeEnum(ioc_type_name.lower())
        except ValueError:
            return hashlib.sha256(value.encode("utf-8")).hexdigest()
        
        if ioc_type in self.HASH_TYPES:
            return value.lower()
        else:
            return hashlib.sha256(value.encode("utf-8")).hexdigest()
        
    @classmethod
    def get_normalized_value(self, ioc_type_name: str, value: str) -> str:
        """Get normalized representation for the value"""
        try:
            ioc_type = IOCTypeEnum(ioc_type_name.lower())
        except:
            return value
        
        if ioc_type in self.HASH_TYPES:
            return value.lower()
        elif ioc_type in [IOCTypeEnum.DOMAIN, IOCTypeEnum.EMAIL]:
            return value.lower()
        elif ioc_type == IOCTypeEnum.IPV6_ADDR:
            try:
                return str(ipaddress.IPv6Address(value))
            except ipaddress.AddressValueError:
                return value.lower()
            
        return value
