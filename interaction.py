import sys
import os

def prompt_decision_menu(summary: str, options: list[str]) -> str:
    """
    Presents a decision menu to the user and returns their selection.
    Automatically appends an 'Other' option.
    """
    # ANSI escape codes for colors
    RED = '\033[91m'
    YELLOW = '\033[93m'
    RESET_COLOR = '\033[0m'

    # Display summary (using RED for errors)
    print(f"{RED}{summary}{RESET_COLOR}\n")

    num_options = len(options)
    for i, option in enumerate(options):
        print(f"[{i+1}] {option}")

    # Add the "Other" option
    other_option_index = num_options + 1
    print(f"[{other_option_index}] Other (Please specify)")

    while True:
        try:
            choice = input("Selection: ").strip()
            if choice.isdigit():
                choice_num = int(choice)
                if 1 <= choice_num <= num_options:
                    return options[choice_num - 1]
                elif choice_num == other_option_index:
                    custom_input = input("Specify: ").strip()
                    return f"Other: {custom_input}"
                else:
                    print("Invalid option number. Please try again.")
            else:
                print("Invalid input. Please enter a number corresponding to your choice.")
        except EOFError:
            print("Input stream closed. Exiting.")
            sys.exit(1)
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            sys.exit(0)
