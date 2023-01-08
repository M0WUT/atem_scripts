from macro_lib import Macro, Source

# Camera definitions
MONITOR = Source.CAM1
CAMERA1 = Source.CAM2
VNA = Source.CAM3
CAMERA2 = Source.CAM4
SPECTRUM_ANALYSER = Source.CAM5
OSCILLOSCOPE = Source.CAM6
MICROSCOPE = Source.CAM7
OVERLAYS = Source.CAM8


macro1 = Macro(
    0, "Enable PIP", "Enable Picture in Picture"
)
macro1.add_picture_in_picture(source=CAMERA1)

macro2 = Macro(1, "Disable PIP", "Remove Picture in Picture")
macro2.remove_picture_in_picture()

macro3 = Macro(2, "Monitor", "Display PC Monitor")
macro3.change_camera(MONITOR)

macro4 = Macro(3, "VNA", "Display VNA")
macro4.change_camera(VNA)

macro5 = Macro(4, "Spectrum Analyser", "Display Spectrum Analyser")
macro5.change_camera(SPECTRUM_ANALYSER)

macro6 = Macro(5, "Microscope", "Display Microscope")
macro6.change_camera(MICROSCOPE)

macro7 = Macro(6, "Camera 1", "Display Camera 1")
macro7.change_camera(CAMERA1)

macro8 = Macro(7, "Camera 2", "Display Camera 2")
macro8.change_camera(CAMERA2)

macro9 = Macro(8, "Enable Overlays", "Enable Green screen overlays")
macro9.enable_green_screen_overlays(OVERLAYS)

macro10 = Macro(9, "Hide Overlays", "Hide green screen overlays")
macro10.hide_green_screen_overlays()

macro11 = Macro(10, "Show Overlays",
                "Enables the overlay USK but doesn't set it up")
macro11.set_upstream_keyer_state(Macro.USK_INSTRUMENT, True)

macro12 = Macro(11, "Preview Camera 1", "Preview Camera 1")
macro12.set_output_source(1, CAMERA1)

macro13 = Macro(12, "Preview Multiview", "Preview Multiview")
macro13.set_output_source(1, Source.MULTIVIEW)

macro14 = Macro(13, "Preview Program", "Preview Program")
macro14.set_output_source(1, Source.PROGRAM)

with open("output.xml", 'w') as output_file:
    # Header
    output_file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    output_file.write(
        '<Profile majorVersion="2" minorVersion="0" product="ATEM Mini Extreme ISO">\n')
    output_file.write('    <MacroPool>\n')

    # Macros
    for macro in [macro1, macro2, macro3, macro4, macro5, macro6, macro7, macro8, macro9, macro10, macro11, macro12, macro13, macro14]:
        output_file.write(macro.finalise())

    # Footer
    output_file.write('    </MacroPool>\n')
    output_file.write('    <MacroControl loop="False"/>\n')
    output_file.write('</Profile>\n')
