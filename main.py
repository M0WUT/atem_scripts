from macro_lib import Macro, Source

# Camera definitions
MONITOR = Source.CAM1
ROAMING_CAM = Source.CAM2
VNA = Source.CAM3
OVERHEAD = Source.CAM4
SPECTRUM_ANALYSER = Source.CAM5
OSCILLOSCOPE = Source.CAM6
MICROSCOPE = Source.CAM7
OVERLAYS = Source.CAM8

macros: list[Macro] = []

macros.append(Macro(
    0, "Enable PIP", "Enable Picture in Picture"
))
macros[-1].add_picture_in_picture(source=OVERHEAD)

macros.append(Macro(1, "Disable PIP", "Remove Picture in Picture"))
macros[-1].remove_picture_in_picture()

macros.append(Macro(2, "Monitor", "Display PC Monitor"))
macros[-1].change_camera(MONITOR)

macros.append(Macro(3, "VNA", "Display VNA"))
macros[-1].start_stinger()
macros[-1].disable_non_stinger_keyers()
macros[-1].set_input_source(Source.BLACK)
macros[-1].add_upstream_key(keyNumber=1, source=VNA,
                            xPos=0, yPos=0, xSize=1.5, ySize=1.5)
macros[-1].close_stinger()


macros.append(Macro(4, "Spectrum Analyser", "Display Spectrum Analyser"))
macros[-1].change_camera(SPECTRUM_ANALYSER)

macros.append(Macro(5, "Microscope", "Display Microscope"))
macros[-1].change_camera(MICROSCOPE)

macros.append(Macro(6, "Overhead Camera", "Display Overhead Camera"))
macros[-1].change_camera(OVERHEAD)

macros.append(Macro(7, "Spare Camera", "Display Spare Camera"))
macros[-1].change_camera(ROAMING_CAM)

macros.append(Macro(8, "Enable Overlays", "Enable Green screen overlays"))
macros[-1].enable_green_screen_overlays(OVERLAYS)

macros.append(Macro(9, "Hide Overlays", "Hide green screen overlays"))
macros[-1].hide_green_screen_overlays()

macros.append(Macro(10, "Show Overlays",
                    "Enables the overlay USK but doesn't set it up"))
macros[-1].set_upstream_keyer_state(Macro.USK_INSTRUMENT, True)

macros.append(Macro(11, "Preview Camera 1", "Preview Camera 1"))
macros[-1].set_output_source(1, OVERHEAD)

macros.append(Macro(12, "Preview Multiview", "Preview Multiview"))
macros[-1].set_output_source(1, Source.MULTIVIEW)

macros.append(Macro(13, "Preview Program", "Preview Program"))
macros[-1].set_output_source(1, Source.PROGRAM)

macros.append(Macro(14, "Oscilloscope", "Display Oscilloscope"))
macros[-1].change_camera(OSCILLOSCOPE)

with open("output.xml", 'w') as output_file:
    # Header
    output_file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    output_file.write(
        '<Profile majorVersion="2" minorVersion="0" product="ATEM Mini Extreme ISO">\n')
    output_file.write('    <MacroPool>\n')

    # Macros
    for macro in macros:
        output_file.write(macro.finalise())

    # Footer
    output_file.write('    </MacroPool>\n')
    output_file.write('    <MacroControl loop="False"/>\n')
    output_file.write('</Profile>\n')
