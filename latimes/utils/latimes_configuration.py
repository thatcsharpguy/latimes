import collections.abc
# from datetime import timezone
from typing import Union, Dict, List

from latimes.utils import DEFAULT_VALUES
from latimes.utils.latimes_output_formatting import LatimesOutputFormatting
from pytz import timezone


class LatimesConfiguration:


    def __init__(
        self,
        starting_timezone: Union[str, timezone],
        convert_to: Union[Dict[str, timezone], List[str]],
        output_formatting: LatimesOutputFormatting,
    ):
        self.output_formatting = output_formatting
        if isinstance(convert_to, collections.abc.Sequence):
            self.convert_to = dict()
            for content in convert_to:
                label, _, tz = content.partition(":")
                self.convert_to[label] = timezone(tz)
        else:
            self.convert_to = convert_to

        if isinstance(starting_timezone, str):
            self.starting_timezone = timezone(starting_timezone)
        else:
            self.starting_timezone = starting_timezone

    def __eq__(self, other) -> bool:
        if not isinstance(other, LatimesConfiguration):
            return False

        return (
            other.convert_to == self.convert_to
            and other.output_formatting == self.output_formatting
            and other.starting_timezone == self.starting_timezone
        )

    @classmethod
    def from_dict(cls, dictionary: Dict):
        output_format = LatimesOutputFormatting.from_dict(
            dictionary["output_formatting"]
        )

        convert_to = dict()
        for content in dictionary["convert_to"]:
            label, _, tz = content.partition(":")
            convert_to[label] = timezone(tz)
        starting_timezone = timezone(dictionary["starting_timezone"])

        return cls(
            starting_timezone=starting_timezone,
            convert_to=convert_to,
            output_formatting=output_format,
        )


DEFAULT_CONFIG = LatimesConfiguration.from_dict(DEFAULT_VALUES)
