from .utils import short_name
from dataclasses import dataclass


class HVAC:
    """Placeholder HVAC class.
       Currently will just return no hvac
    """

    def to_inp(self):
        inp_str = '"Sys1 (SUM)" = SYSTEM\n' \
            '   TYPE             = SUM\n' \
            '   HEAT-SOURCE      = NONE\n' \
            '   SYSTEM-REPORTS   = NO\n   ..\n'
        return inp_str

    def __repr__(self):
        return self.to_inp()


@dataclass
class _HVACBase:
    """Make base that takes HB HVAC objs:
        Checks if in eQuest system lib, makes obj
    """
    pass
