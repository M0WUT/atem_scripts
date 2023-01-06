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
    MULTIVIEW = auto()
    PROGRAM = auto()

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
            self.MULTIVIEW: "MultiView1",
            self.PROGRAM: "ME1Program"

        }
        return names[self]


class Macro:

    NUM_UPSTREAM_KEYERS = 4
    NUM_DOWNSTREAM_KEYERS = 2

    # Upstream Keyer uses (note that 1 is put on the bottom and 4 on the top)
    USK_INSTRUMENT = 3  # Overlay of Instrument Readings
    USK_PIP = 4  # Picture in Picture

    # Downstream Keyer uses (note that 1 is on the bottom and 2 is on the top)
    DSK_STINGER = 2

    def __init__(self, index: int, name: str = "", description: str = ""):
        self.macroString = f'        <Macro index="{index}" name="{name}" description="{description}">\n'

    def set_fastest_ftb_speed(self):
        self._macro_print(
            {"id": "FadeToBlackRate", "mixEffectBlockIndex": 0, "rate": 1}
        )

    def toggle_ftb(self):
        self._macro_print({"id": "FadeToBlackAuto", "mixEffectBlockIndex": 0})

    def set_upstream_keyer_state(self, keyer: int, enabled: bool):
        """Sets state of Upstream Keyer number <keyer> to <enabled>"""
        self._macro_print(
            {
                "id": "KeyOnAir",
                "mixEffectBlockIndex": 0,
                "keyIndex": (keyer - 1),
                "onAir": bool(enabled),
            }
        )

    def set_downstream_keyer_state(self, keyer: int, enabled: bool):
        """Sets state of Downstream Keyer number <keyer> to <enabled>"""
        self._macro_print(
            {
                "id": "DownstreamKeyOnAir",
                "keyIndex": (keyer - 1),
                "onAir": bool(enabled),
            }
        )

    def disable_all_keyers(self):
        """Disables the 4 upstream and 2 downstream keyers"""
        for upstream_keyer in range(1, self.NUM_UPSTREAM_KEYERS + 1):
            self.set_upstream_keyer_state(upstream_keyer, False)

        for downstream_keyer in range(1, self.NUM_DOWNSTREAM_KEYERS):
            self.set_downstream_keyer_state(downstream_keyer, False)

    def disable_non_stinger_keyers(self):
        """Disables the 4 upstream and DSK1 (2 is used for transition)"""
        for upstream_keyer in range(1, self.NUM_UPSTREAM_KEYERS + 1):
            self.set_upstream_keyer_state(upstream_keyer, False)

        for downstream_keyer in range(1, self.NUM_DOWNSTREAM_KEYERS + 1):
            if downstream_keyer != self.DSK_STINGER:
                self.set_downstream_keyer_state(downstream_keyer, False)

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
        self.set_downstream_keyer_state(self.DSK_STINGER, False)

    def set_output_source(self, output: int, source: Source):
        """
        Sets source for HDMI outputs
        """
        self._macro_print(
            {"id": "AuxiliaryInput", "auxilaryIndex": (output - 1), "input": source})

    def add_picture_in_picture(self, source: Source):
        self.add_upstream_key(
            keyNumber=self.USK_PIP,
            source=source,
            xPos=13,
            yPos=-7,
            xSize=0.2,
            ySize=0.2,
        )

    def remove_picture_in_picture(self):
        self.set_upstream_keyer_state(self.USK_PIP, False)

    def change_camera(self, source: Source):
        self.start_stinger()
        self.disable_non_stinger_keyers()
        self.set_input_source(source)
        self.close_stinger()

    def enable_green_screen_overlays(self, source: Source):
        self._macro_print({"id": "KeyType", "mixEffectBlockIndex": 0,
                          "keyIndex": self.USK_INSTRUMENT - 1, "type": "Chroma"})
        self._macro_print({"id": "KeyFillInput", "mixEffectBlockIndex": 0,
                          "keyIndex": self.USK_INSTRUMENT - 1, "input": source})
        self._macro_print({"id": "AdvancedChromaKeySamplingModeEnabled",
                          "mixEffectBlockIndex": 0, "keyIndex": self.USK_INSTRUMENT - 1, "enabled": True})
        self._macro_print({"id": "AdvancedChromaKeyCursorSize", "mixEffectBlockIndex": 0,
                          "keyIndex": self.USK_INSTRUMENT - 1, "size": 0.0630035})
        self._macro_print({"id": "AdvancedChromaKeyCursorXPosition", "mixEffectBlockIndex": 0,
                          "keyIndex": self.USK_INSTRUMENT - 1, "xPosition": -17.024})
        self._macro_print({"id": "AdvancedChromaKeyCursorYPosition", "mixEffectBlockIndex": 0,
                          "keyIndex": self.USK_INSTRUMENT - 1, "yPosition": 10.286})
        self.set_upstream_keyer_state(self.USK_INSTRUMENT, True)

    def hide_green_screen_overlays(self):
        self.set_upstream_keyer_state(self.USK_INSTRUMENT, False)

    def _macro_print(self, x: dict):
        # Formats a dictionary into a single line to be printed
        line = "            <Op "
        line += " ".join([f'{a}="{b}"' for a, b in x.items()])
        line += "/>\n"
        self.macroString += line

    def finalise(self) -> str:
        self.macroString += "        </Macro>\n"
        return self.macroString


def main():
    x = Macro(index=0, name="test", description="This is a test macro")
    x.print()


if __name__ == "__main__":
    main()
