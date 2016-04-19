class ErrorCode:
    NO_SUCH_FILE = 1
    NO_PERMISSION = 2
    TITLE_MISSING = 3
    DOMAIN_MISSING = 4

ErrorMsg = {
    ErrorCode.TITLE_MISSING : "Title Missing",
    ErrorCode.DOMAIN_MISSING : "Domain Missing",
} 
