import dragonfly_energy


class DoeHVAC(object):
    """Placeholder HVAC class.
       Currently will just return no hvac
    """

    def to_inp_string(self):
        inp_str = '"Sys1 (SUM)" = SYSTEM\n  ' \
            'TYPE             = SUM\n  ' \
            'HEAT-SOURCE      = NONE\n  ' \
            'SYSTEM-REPORTS   = NO\n  ..\n'
        return(inp_str)

    def __repr__(self):
        return(self.to_inp_string)
