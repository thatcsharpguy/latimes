from typing import Dict


class LatimesOutputFormatting:
    def __init__(
        self,
        time_format_string: str,
        different_time_joiner: str,
        aggregate_joiner: str,
        aggregate: bool,
    ):
        self.aggregate = aggregate
        self.aggregate_joiner = aggregate_joiner
        self.time_format_string = time_format_string
        self.different_time_joiner = different_time_joiner

    def __eq__(self, other) -> bool:
        if not isinstance(other, LatimesOutputFormatting):
            return False
        return (
            other.time_format_string == self.time_format_string
            and other.different_time_joiner == self.different_time_joiner
            and other.aggregate == self.aggregate
            and other.aggregate_joiner == self.aggregate_joiner
        )

    @classmethod
    def from_dict(cls, dictionary: Dict):
        return cls(**dictionary)
