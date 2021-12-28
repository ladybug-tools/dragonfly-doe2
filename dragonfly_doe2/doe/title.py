from dataclasses import dataclass


@dataclass
class Title:

    title: str

    def to_inp(self) -> str:
        """Return run period as an inp string."""
        # standard holidays should be exposed.
        return 'TITLE\n' \
            f'    LINE-1           = *{self.title}*\n' \
            '    ..'

    def __repr__(self) -> str:
        return self.to_inp()
