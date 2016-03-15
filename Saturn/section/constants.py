PAGE_SIZE = 5

class Status:
    PUBLIC = 1
    PRIVATE = 2

STATUS_CHOICES = (
    (Status.PUBLIC, 'Public'),
    (Status.PRIVATE, 'Private'),
)

class SectionTypes:
    DEFAULT = 0
    POST = 1
