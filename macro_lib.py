# Generates my Atem Mini Extreme macros as re-recording SUCKS!

from enum import Enum, auto


class Source(Enum):
    CAM1 = auto()
    CAM2 = auto()
    CAM3 = auto()
    CAM4 = auto()
    CAM5 = auto()
    CAM6 = auto()
    CAM7 = auto()
    CAM8 = auto()
    BLACK = auto()
    MEDIA_PLAYER_1 = auto()
    MEDIA_PLAYER_2 = auto()

    def __str__(self):
        names = {
            self.CAM1: "Camera1",
            self.CAM2: "Camera2",
            self.CAM3: "Camera3",
            self.CAM4: "Camera4",
            self.CAM5: "Camera5",
            self.CAM6: "Camera6",
            self.CAM7: "Camera7",
            self.CAM8: "Camera8",
            self.BLACK: "Black",
            self.MEDIA_PLAYER_1: "MediaPlayer1",
            self.MEDIA_PLAYER_2: "MediaPlayer2",
        }
        return names[self]


class Macro:
    def __init__(self, index: int, name: str = "", description: str = ""):
        self.macroString = f'        <Macro index="{index}" name="{name}" description="{description}">\n'

    def set_fastest_ftb_speed(self):
        self._macro_print(
            {"id": "FadeToBlackRate", "mixEffectBlockIndex": 0, "rate": 1}
        )

    def toggle_ftb(self):
        self._macro_print({"id": "FadeToBlackAuto", "mixEffectBlockIndex": 0})

    def set_upstream_keyer_state(self, keyer: int, enabled: bool):
        """Sets state of USK 1-4 to <enabled>"""
        self._macro_print(
            {
                "id": "KeyOnAir",
                "mixEffectBlockIndex": 0,
                "keyIndex": (keyer - 1),
                "onAir": bool(enabled),
            }
        )

    def set_downstream_keyer_state(self, keyer: int, enabled: bool):
        """Sets state of DSK 1-2 to <enabled>"""
        self._macro_print(
            {
                "id": "DownstreamKeyOnAir",
                "keyIndex": (keyer - 1),
                "onAir": bool(enabled),
            }
        )

    def disable_all_keyers(self):
        """Disables the 4 upstream and 2 downstream keyers"""
        for upstreamKeyer in range(1, 5):
            self.set_upstream_keyer_state(upstreamKeyer, False)

        for downstreamKeyer in range(1, 3):
            self.set_downstream_keyer_state(downstreamKeyer, False)

    def disable_non_stinger_keyers(self):
        """Disables the 4 upstream and DSK1 (2 is used for transition)"""
        for upstreamKeyer in range(1, 5):
            self.set_upstream_keyer_state(upstreamKeyer, False)

        for downstreamKeyer in [1]:
            self.set_downstream_keyer_state(downstreamKeyer, False)

    def set_input_source(self, source: Source):
        self._macro_print(
            {"id": "ProgramInput", "mixEffectBlockIndex": 0, "input": source}
        )

    def add_upstream_key(
        self,
        keyNumber: int,
        source: Source,
        xPos: float,
        yPos: float,
        xSize: float,
        ySize: float,
    ):

        # Set Key to DVE type
        self._macro_print(
            {
                "id": "KeyType",
                "mixEffectBlockIndex": 0,
                "keyIndex": (keyNumber - 1),
                "type": "DVE",
            }
        )

        # Set Key Source
        self._macro_print(
            {
                "id": "KeyFillInput",
                "mixEffectBlockIndex": 0,
                "keyIndex": (keyNumber - 1),
                "input": source,
            }
        )

        # Disable Masking
        self._macro_print(
            {
                "id": "KeyMaskEnable",
                "mixEffectBlockIndex": 0,
                "keyIndex": (keyNumber - 1),
                "enable": False,
            }
        )

        # Enable Flying image
        self._macro_print(
            {
                "id": "KeyFlyEnable",
                "mixEffectBlockIndex": 0,
                "keyIndex": (keyNumber - 1),
                "enable": True,
            }
        )

        # Set X Position
        self._macro_print(
            {
                "id": "DVEAndFlyKeyXPosition",
                "mixEffectBlockIndex": 0,
                "keyIndex": (keyNumber - 1),
                "xPosition": xPos,
            }
        )

        # Set Y Position
        self._macro_print(
            {
                "id": "DVEAndFlyKeyYPosition",
                "mixEffectBlockIndex": 0,
                "keyIndex": (keyNumber - 1),
                "yPosition": yPos,
            }
        )

        # Set X Size
        self._macro_print(
            {
                "id": "DVEAndFlyKeyXSize",
                "mixEffectBlockIndex": 0,
                "keyIndex": (keyNumber - 1),
                "xSize": xSize,
            }
        )

        # Set Y Size
        self._macro_print(
            {
                "id": "DVEAndFlyKeyYSize",
                "mixEffectBlockIndex": 0,
                "keyIndex": (keyNumber - 1),
                "ySize": ySize,
            }
        )

        self.set_upstream_keyer_state(keyNumber, True)

    def start_stinger(self):
        """Starts stinger to point where the screen is completely covered with RGB #e1970C"""
        self.macroString += (
            '            <Op id="ColorGeneratorHue" colorGeneratorIndex="0" hue="39.13043478260869"/>\n'
            '            <Op id="ColorGeneratorSaturation" colorGeneratorIndex="0" saturation="0.9002375296912113"/>\n'
            '            <Op id="ColorGeneratorLuminescence" colorGeneratorIndex="0" luminescence="0.464836625"/>\n'
            '            <Op id="DownstreamKeyFillInput" keyIndex="1" input="Color1"/>\n'
            '            <Op id="DownstreamKeyCutInput" keyIndex="1" input="MediaPlayer1Key"/>\n'
            '            <Op id="DownstreamKeyMaskEnable" keyIndex="1" enable="False"/>\n'
            '            <Op id="DownstreamKeyPreMultiply" keyIndex="1" preMultiply="False"/>\n'
            '            <Op id="DownstreamKeyClip" keyIndex="1" clip="0.429993"/>\n'
            '            <Op id="DownstreamKeyGain" keyIndex="1" gain="0.229996"/>\n'
            '            <Op id="DownstreamKeyOnAir" keyIndex="1" onAir="True"/>\n'
        )
        for x in range(10):
            self._macro_print(
                {
                    "id": "MediaPlayerSourceStillIndex",
                    "mediaPlayer": 0,
                    "index": x,
                }
            )
            self._macro_print(
                {"id": "MediaPlayerSourceStill", "mediaPlayer": 0}
            )
            self._macro_print({"id": "MacroSleep", "frames": 1})

    def close_stinger(self):
        self._macro_print({"id": "MacroSleep", "frames": 5})
        for x in range(10):
            self._macro_print(
                {
                    "id": "MediaPlayerSourceStillIndex",
                    "mediaPlayer": 0,
                    "index": 9 - x,
                }
            )
            self._macro_print(
                {"id": "MediaPlayerSourceStill", "mediaPlayer": 0}
            )
            self._macro_print({"id": "MacroSleep", "frames": 1})
        self.set_downstream_keyer_state(2, False)

    def _macro_print(self, x: dict):
        # Formats a dictionary into a single line to be printed
        line = "            <Op "
        line += " ".join([f'{a}="{b}"' for a, b in x.items()])
        line += "/>\n"
        self.macroString += line

    def print(self):
        self.macroString += "        </Macro>"
        print(self.macroString)  # @DEBUG


def main():
    x = Macro(index=0, name="test", description="This is a test macro")
    x.print()


if __name__ == "__main__":
    main()
