# Hosts

Command line tool that manipulates /etc/hosts without buggering it up.


# Usage

    # Add a entry to your hosts file
    sudo hosts -a '192.0.2.1 example.com'

    # Remove all enteries for example.com (as the canonical name)
    sudo hosts -r example.com


# Installation

Arch Linux user can install hosts as a package but running;

    ./scripts/package

