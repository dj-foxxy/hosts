# Hosts

Command line tool to manipulate /etc/hosts without buggering it up.

Cleanly adds and removes host file entries, ensuring no duplicates.

# Usage

    # Add a line to the hosts file
    sudo hosts -a "176.58.126.127 foxdogstudios.com"'

    # Remove a line
    sudo hosts -r foxdogstudios.com


# Installation

If you're on arch linux you can install the package

    ./scripts/package

