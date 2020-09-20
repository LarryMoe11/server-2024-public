#!/usr/bin/env python3
# Copyright (c) 2019 FRC Team 1678: Citrus Circuits
"""Houses upload_qr_codes which appends unique QR codes to local competition document.

Checks for duplicates within set of QR codes to add, and the database.
Appends new QR codes to raw.qr.
"""

import yaml

import local_database_communicator
import utils


def upload_qr_codes(qr_codes):
    """Uploads QR codes into the current competition document.

    Prevents duplicate QR codes from being uploaded to the database.
    qr_codes is a list of QR code strings to upload.
    """
    # Gets the starting character for each QR code type, used to identify QR code type
    schema = utils.read_schema('schema/match_collection_qr_schema.yml')

    # Acquires current qr data using local_database_communicator.py
    qr_data = local_database_communicator.read_dataset('raw.qr')

    # Creates a set to store QR codes
    # This is a set in order to prevent addition of duplicate qr codes
    qr = set()

    for qr_code in qr_codes:
        if qr_code in qr_data:
            pass
        # Checks to make sure the qr is valid by checking its starting character. If the starting
        # character doesn't match either of the options, the QR is printed out.
        elif not (qr_code.startswith(schema['subjective_aim']['_start_character']) or
                  qr_code.startswith(schema['objective_tim']['_start_character'])):
            utils.log_warning(f'Invalid QR code not uploaded: "{qr_code}"')
        else:
            qr.add(qr_code)

    # Adds the QR codes to the local database if the set isn't empty
    if qr != set():
        local_database_communicator.append_to_dataset('raw.qr', list(qr))

    return qr
