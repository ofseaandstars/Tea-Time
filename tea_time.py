#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" tea-time.py: A utility script to make sure you don't forget about the kettle you boiled."""

# Ownership, licensing and usage documentation
# can be found at the bottom of this script.

from argparse import ArgumentParser
import os
import sys
import time
from rich import print as rprint, pretty as auto_pretty
from rich.progress import Progress, SpinnerColumn
from rich.prompt import Confirm, Prompt
from rich.panel import Panel
from rich.pretty import Pretty
from playsound import playsound

auto_pretty.install()
# This allows us to insert pretty-printed data into other renderables.
pretty = Pretty(locals())

# ----------------------------------------- #


def register_arguments():
    ''' Registers the arguments for the script.'''

    arguments_parser = ArgumentParser(
        description='Utility script to make sure you don\'t forget about the kettle you boiled')

    arguments_parser.add_argument(
        "-k", "--kettle", help='How long to wait for the kettle.', dest="kettle")

    arguments_parser.add_argument(
        "-b", "--brew", help='How long to wait for the tea to brew.', dest="brew")

    return arguments_parser.parse_args()


def convert_time(time_string):
    ''' Converts a time string to seconds'''
    time_string = str(time_string)
    seconds_per_unit = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}
    return int(time_string[:-1]) * seconds_per_unit[time_string[-1]]


def set_timer(seconds, arg):
    ''' Sets the timer to start'''

    start_time = time.time()
    elapsed_time = 0

    if arg == "kettle":
        with Progress(SpinnerColumn(spinner_name='clock'), *Progress.get_default_columns(), transient=True) as kettle_progress:
            kettle_timer = kettle_progress.add_task(
                messages['kettle_task_description'], total=seconds)

            while elapsed_time < seconds:
                elapsed_time = time.time() - start_time
                kettle_progress.update(kettle_timer, advance=1)
                time.sleep(1)

        # Reset the timer for the next step.
        start_time = time.time()

    if arg == "brew":
        print('')
        with Progress(SpinnerColumn(spinner_name='clock'), *Progress.get_default_columns(), transient=True) as brew_progress:
            brew_timer = brew_progress.add_task(
                messages['tea_task_description'], total=seconds)

            while elapsed_time < seconds:
                elapsed_time = time.time() - start_time
                brew_progress.update(brew_timer, advance=1)
                time.sleep(1)


def ready_to_brew_prompt():
    '''Gets input from the user if they want to brew.'''

    confirmation = Confirm.ask(messages['tea_brew_confirmation'])
    return confirmation


def display_tea_time_header():
    ''' Prints a display header for the script. '''
    clear_terminal()
    string = (
        messages['tea_time_header_primary'] +
        messages['tea_time_header_secondary']
    )
    rprint(Panel.fit(string, title=messages['tea_time_header_title'],
                     subtitle=messages['tea_time_header_subtitle'], padding=(1, 1)))


def clear_terminal():
    ''' Clears the terminal display. '''
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)
    rprint('')
# ----------------------------------------- #


args = register_arguments()

# All of the output messages sent to the console.
messages = {
    "tea_time_header_title": "[bold]TEA TIME",
    "tea_time_header_subtitle": '[italic]Lovingly crafted by Marina[/italic] :hot_beverage-emoji:',
    "tea_time_header_primary": "[italic]It\'s time to brew some tea![/italic]\n",
    "tea_time_header_secondary": "[italic]Get your kettle boiling and press[/italic] [gold1]Enter[white] [italic]to continue the process![/italic]",
    "invalid_kettle_format": '[red]Invalid time specified! Use "-k 1m" format',
    "invalid_brew_format": '[red]Invalid time specified! Use "-b 1m" format',
    "kettle_boiled": '[green blink]Kettle has now boiled (hopefully)!\n',
    "kettle_task_description": "[blink]Kettle boiling...",
    "tea_brew_confirmation": '[bold]Are you ready to brew?',
    "tea_brewed": '\n[bold italic]Your tea has brewed![/bold italic] :hot_beverage-emoji:\nPress [gold1]Enter[/gold1] once more and then enjoy your beverage!',
    "tea_brewing_cancelled": 'Tea brewing cancelled. Press [gold1]Enter[/gold1] to close the program.',
    "tea_task_description": "[blink]Tea brewing...",
    "no_kettle_timer_prompt": '\nHow long would you like to set your kettle timer for? [bold cyan](3m)[/bold cyan]',
    "no_brew_timer_prompt": '\nHow long would you like to brew your tea for? [bold cyan](Leave blank if you don\'t want to brew)[/bold cyan]'
}


def main():
    '''The main function of the script.'''

    ring_sound_path = os.getcwd() + '/lib/ring.mp3'
    ding_sound_path = os.getcwd() + '/lib/ding.mp3'

    display_tea_time_header()

    if args.kettle is None and args.brew is None:
        rprint(
            '\n[italic]No timers were provided...\n\nPress [gold1]Enter[/gold1] to set timers:')
        input()
        # We don't want to show the default here so we can use our own formatting for the messages.
        display_tea_time_header()
        args.kettle = Prompt.ask(
            messages['no_kettle_timer_prompt'], default="3m", show_default=False)
        display_tea_time_header()
        args.brew = Prompt.ask(
            messages['no_brew_timer_prompt'], default=None, show_default=False)
        display_tea_time_header()
        generated_timers = True
    else:
        generated_timers = False

    if args.kettle is not None:
        if generated_timers is False:
            input()
        else:
            rprint('')
        try:
            seconds = convert_time(args.kettle)
        except ValueError:
            rprint(messages['invalid_kettle_format'])
            sys.exit()

        rprint(f'[bold]Kettle Timer:[/bold] {args.kettle}')
        rprint(f'[bold]Brew Timer:[/bold] {args.brew}\n')
        set_timer(seconds, 'kettle')
        rprint(messages['kettle_boiled'])
        playsound(ding_sound_path)
        if args.brew is not None:
            response = ready_to_brew_prompt()
            if response is True:
                display_tea_time_header()
                rprint('')
                rprint(f'[bold]Kettle Timer:[/bold] {args.kettle}')
                rprint(f'[bold]Brew Timer:[/bold] {args.brew}\n')
                try:
                    seconds = convert_time(args.brew)
                except ValueError:
                    rprint(messages['invalid_brew_format'])
                    sys.exit()
                set_timer(seconds, 'brew')
                rprint('\r')
                rprint(messages['tea_brewed'])
                playsound(ring_sound_path)
                input()
                clear_terminal()
            else:
                rprint(messages['tea_brewing_cancelled'])
                input()
                clear_terminal()

    elif args.brew is not None:
        display_tea_time_header()
        rprint('')
        rprint(f'[bold]Kettle Timer:[/bold] {args.kettle}')
        rprint(f'[bold]Brew Timer:[/bold] {args.brew}\n')
        try:
            seconds = convert_time(args.brew)
        except ValueError:
            rprint(messages['invalid_brew_format'])
            sys.exit()
        set_timer(seconds, 'brew')
        rprint('\r')
        rprint(messages['tea_brewed'])
        playsound(ring_sound_path)
        input()
        clear_terminal()


if __name__ == "__main__":
    main()

"""
@Author = "Marina (OfSeaAndStars)"
@Licence = "MIT"
@Version = "2.0.0"
@Email = "oftheseaandstars@proton.me"
@Status = "Production"
"""

"""
Examples:

    Set a 'kettle-only' timer for 3 minutes:

        $ python tea_time.py -k 3m

    Set a timer with a 3-minute 'kettle' time and 4-minute 'brew' time:

        $ python tea_time.py -k 3m -b 4m

"""

"""
Attribution:

    'ding.mp3'
    'ring.mp3'

        Attribution 4.0 International (CC BY 4.0). You are allowed to use sound effects \
            free of charge and royalty free in your multimedia projects \
            for commercial or non-commercial purposes.
        http://www.freesoundslibrary.com
"""
