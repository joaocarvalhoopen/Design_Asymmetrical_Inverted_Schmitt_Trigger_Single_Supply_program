# Automatic design of an Asymmetrical Inverted Schmitt-Trigger with Single Supply

![Schematic](./schematic.png?raw=true "Schematic")

# Description:
This is a simple program to make the automatic design of an Asymmetrical Inverted Schmitt-Trigger with Single Supply, with resistors from E24 scale. Typically used for 1%, but in this case used for 5% or 0.1% .<br>
The input is V_supply, V_low_threshold, V_high_threshold and Resistor_tolerance_perc.<br>
It works by making the full search of all combinations of values from E24 to identify the best ones. In this way it speeds up immensely the manual experimentation.<br>
It also makes resistor tolerance analysis.<br>
Please see the schematic diagram.<br>

![Program output](./program_output.png?raw=true "Program output")

## License
MIT open source license

## Have fun!
Best regards,<br>
Joao Nuno Carvalho<br>