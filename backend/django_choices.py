from enum import Enum

from django.utils.decorators import classproperty


class DjangoChoices(Enum):
    """
    Enum base class for django model choices.

    Why to use this enum:
    1. We can reference choice by Enum attribute name
    2. Value saved in db can be small int
    3. We can give nice, descriptive choice name for users.

    Example:
    >>> from django.db import models
    >>> from django.utils.translation import ugettext_lazy as _
    >>>
    >>> class SomeAccount(models.Model):
    ...     class AccountType(DjangoChoices):
    ...         USER = (1, _('User'))
    ...         DEALER = (2, _('Dealer'))
    ...         CUSTOMER = (3, _('Customer'))
    ...
    ...     account_type = models.SmallIntegerField(
    ...         _('account type'),
    ...         null=False,
    ...         blank=False,
    ...         choices=AccountType.choices,
    ...         default=AccountType.CUSTOMER.key
    ...     )
    ...
    ...     def get_account_type(self):
    ...         return self.AccountType(self.account_type)
    """

    def __init__(self, *args):
        if not isinstance(self.value, tuple):
            raise ValueError(
                'DjangoChoices requires its attributes to be tuples. '
                f'{self.name} is not a tuple (its {type(self.value)}).'
            )
        if len(self.value) != 2:
            raise ValueError(
                'DjangoChoices requires its attributes to be two-element tuple. '
                f'\'{self.name}\' attribute has {len(self.value)} elements.'
            )

        cls = self.__class__

        # Force uniqueness on first elements of tuples
        if any(self.value[0] == e.key for e in cls):
            a = self.name
            e = cls(self.value).name
            raise ValueError(
                (
                    'aliases not allowed in {}:  {!r:} --> {!r:}. '
                    'Remember that the first value of the tuple cannot be repeated.'
                ).format(cls.__name__, a, e)
            )

        # Add value to inner lookup dict
        cls._get_enum()[self.value[0]] = self.value

    @classmethod
    def _get_enum(cls):
        """
        Dict as lookup table, where key is first value of choice,
        value is tuple(<value of choice>, <verbose_name>).
        """
        if not hasattr(cls, '_enum'):
            cls._enum = {}
        return cls._enum

    @classmethod
    def _missing_(cls, value):
        """
        This method is called on __new__ if no value is found.
        Returns enum value that matches first element of value tuple.
        E.g.
        >>> class E(DjangoChoices):
        ...     NEW = (1, 'New - package is ready to dispatch')
        ...     PENDING = (2, 'Pending - package has been dispatched and is in transit')
        ...
        >>> assert(E(1) is E.NEW)
        >>> assert(E(2) is E.PENDING)
        """
        # In case there is a collision where only first value of the tuple
        # collided we can receive tuple there.
        # This value replacement will ensure that correct error will
        # be displayed
        if isinstance(value, tuple):
            value = value[0]

        _value = cls._get_enum().get(value, None)
        if _value is None:
            return super(DjangoChoices, cls)._missing_(value)

        for e in cls:
            if value == e.key:
                return e

    @classproperty
    def choices(cls):
        """
        Returns tuple of model choices
        ((A, B), (A, B)...)
        """
        return tuple(e.value for e in cls)

    @property
    def key(self):
        """
        Returns model value of the enum
        E.g.
        >>> class E(DjangoChoices):
        ...     NEW = (1, 'New - package is ready to dispatch')
        ...     PENDING = (2, 'Pending - package has been dispatched and is in transit')
        ...
        >>> assert(E.NEW.key == 1)
        """
        return super(DjangoChoices, self).value[0]

    @classproperty
    def keys(cls):
        """
        Returns list of keys of model choices
        [A, B, C ...]
        """
        return [e.key for e in cls]

    @classproperty
    def names(cls):
        """
        Returns list of names of model choices
        [A, B, C ...]
        """
        return [e.name for e in cls]

    @property
    def label(self):
        """
        Returns verbose value of the enum
        E.g.
        >>> class E(DjangoChoices):
        ...     NEW = (1, 'New - package is ready to dispatch')
        ...     PENDING = (2, 'Pending - package has been dispatched and is in transit')
        ...
        >>> assert(E.PENDING.label == 'Pending - package has been dispatched and is in transit')
        """
        return super(DjangoChoices, self).value[1]

    @classproperty
    def variable_choices(self):
        """
        Returns a list of tuples of the database value and the API input value
        [(0, 'received'),
         (1, 'commissioned'),
         ...
        ]
        """
        return [(s.key, s.name) for s in self]

    @classproperty
    def max_length(self):
        try:
            return max(len(s.key) for s in self)
        except TypeError:
            pass

    @classmethod
    def get_by_repr(cls, repr_value):
        choices = {v: k for k, v in cls.choices}
        choice = cls(choices[repr_value])
        return choice
