'''
Returns total price paid for individual rentals
'''
import argparse
import json
import datetime
import math
import logging
import sys


def parse_cmd_arguments():
    """parse command line input JSON file and output JSON file"""
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', '--input', required=True, help='input JSON file')
    parser.add_argument('-o', '--output', required=True,
                        help='ouput JSON file')
    parser.add_argument('-d', '--debug', required=False,
                        help='log level. Can be 0-3. Defaults to 0')

    return parser.parse_args()


def setup_logging(log_level):
    lformat = '%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s'
    log_formatter = logging.Formatter(lformat)

    root_logger = logging.getLogger()

    log_file = datetime.datetime.now().strftime("%Y-%m-%d")+'.log'
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.WARNING)
    root_logger.addHandler(file_handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(logging.DEBUG)
    root_logger.addHandler(console_handler)

    parsed_log_level = 0
    try:
        parsed_log_level = int(log_level)
    except:
        # Log level not an integer. Default to logging disabled
        pass

    if parsed_log_level == 1:
        root_logger.setLevel(logging.ERROR)
    elif parsed_log_level == 2:
        root_logger.setLevel(logging.WARNING)
    elif parsed_log_level == 3:
        root_logger.setLevel(logging.DEBUG)
    else:
        root_logger.disabled = True


def load_rentals_file(filename):
    """load input json file"""
    logging.debug('Loading rental file %s', filename)
    try:
        with open(filename) as file:
            try:
                data = json.load(file)
            except ValueError:
                logging.error('File %s cannot be read as JSON', filename)
                exit(0)
    except IOError:
        logging.error('File %s cannot be read (does not exist?)', filename)
        exit(0)
    logging.debug('Successfully loaded rental file %s', filename)
    return data


def validate_entry(value, index):
    try:
        rental_start = datetime.datetime.strptime(value['rental_start'],
                                                  '%m/%d/%y')
    except ValueError:
        logging.warning('Unable to process entry %d because rental start ' +
                        'is not in %%m/%%d/%%y format. Skipping...', index)
        return False

    try:
        rental_end = datetime.datetime.strptime(value['rental_end'],
                                                '%m/%d/%y')
    except ValueError:
        logging.warning('Unable to process entry %d because rental end ' +
                        'is not in %%m/%%d/%%y format. Skipping...', index)
        return False

    if rental_end < rental_start:
        logging.warning('Unable to process entry %d because ' +
                        'rental start > end. Skipping...', index)
        return False

    if value['price_per_day'] < 0:
        logging.warning('Unable to process entry %d because ' +
                        'price per day is negative. Skipping...', index)
        return False

    if value['units_rented'] <= 0:
        logging.warning('Unable to process entry %d because ' +
                        'units rented is non-positive. Skipping...', index)
        return False

    return True


def calculate_additional_fields(data):
    logging.debug('Calculating additional fields for %d entries',
                  len(data.values()))
    for index, value in enumerate(data.values()):
        logging.debug('Processing entry %d with value: %s', index, value)
        try:
            if not validate_entry(value, index):
                continue
            rental_start = datetime.datetime.strptime(value['rental_start'],
                                                      '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'],
                                                    '%m/%d/%y')
            value['total_days'] = (rental_end - rental_start).days + 1
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except:
            logging.warning('Unexpected failure processing entry %d. Skipping',
                            index)
            continue

    return data


def save_to_json(filename, data):
    """save output file JSON"""
    logging.debug('Saving results to %s', filename)
    try:
        with open(filename, 'w') as file:
            json.dump(data, file)
    except IOError:
        logging.error('File %s cannot be opened for write', filename)
        exit(0)
    logging.debug('Successfully saved results to %s', filename)
    return data


if __name__ == "__main__":
    args = parse_cmd_arguments()
    setup_logging(args.debug)
    data = load_rentals_file(args.input)
    data = calculate_additional_fields(data)
    save_to_json(args.output, data)
