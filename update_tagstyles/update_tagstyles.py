#!/bin/python3

import logging
import time
import argparse
import sys
import requests
import yaml
import glob
import os

"""Global Variables"""
SUCCESSFUL_STATUS_CODES = [200, 403]
MAX_BACKUPS = 20

def get_logger():
    """setup logging"""
    logging.basicConfig(stream = sys.stdout, level=logging.INFO)
    logger = logging.getLogger("Default")
    return logger

def get_status_code(url, timeout=10):
    try:
        r = requests.get(url, timeout=timeout)
        return r.status_code
    except requests.exceptions.ConnectionError:
        return 0
    
def load_config(config_file):
    """Load config file"""
    with open(config_file, 'r') as file:
        data = yaml.safe_load(file)

    return data

def get_services(data):
    """Get all services"""
    services = []
    for group in data['services']:
        for service in group['items']:
            services.append({
                "Application": service['name'],
                "tagstyle": service['tagstyle'],
                "url": service['url']
            })

    return services

def update_tagstyle(config_file, service_name, new_tagstyle):
    """Load config file"""
    with open(config_file, 'r') as file:
        data = yaml.safe_load(file)


    for group in data['services']:
        for service in group['items']:
            if service['name'] == service_name:
                service['tagstyle'] = new_tagstyle
                break

    with open(config_file, 'w') as file:
        yaml.safe_dump(data, file)

def backup_config(config_file):
    """Get date"""
    date = time.strftime("%Y%m%d-%H%M%S")

    """File Name"""
    file_name = os.path.basename(config_file)

    """Create backup directory if it doesn't exist"""
    backups_dir = os.path.join(os.path.dirname(config_file), 'backups')
    if not os.path.exists(backups_dir):
        logger.info("Backups directory doesnt exist. Creating directory now")
        os.makedirs(backups_dir)

    """Backup config file"""
    backup_file = f"{backups_dir}/{file_name}.backup_{date}"
    logger.info("Backing up config file")

    """Load config file"""
    with open(config_file, 'r') as file:
        data = yaml.safe_load(file)

    with open(f"{backup_file}", 'w') as file:
        yaml.safe_dump(data, file)

    """If more than max backups, delete oldest"""
    backups = sorted(glob.glob(f"{backups_dir}/{file_name}.backup_*"), key=os.path.getctime)
    if len(backups) > MAX_BACKUPS:
        logger.info("Max backups reached. Deleting oldest")
        os.remove(backups[0])


def get_parameters():
    """Get parameters"""
    parser = argparse.ArgumentParser(description="Check status of all services and update tagstyle")
    parser.add_argument("-c", "--config", help="Path to config file", required=True)
    args = parser.parse_args()

    """If ran without arguments, print help menu"""
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    return args

def main():

    """Get parameters"""
    args = get_parameters()

    config_file = args.config

    """Backup config file"""
    backup_config(config_file)

    """Get all services"""
    logger.info("Getting all services")
    services = get_services(load_config(config_file))

    """Check status for each service"""
    for service in services:
        logger.info(f"Checking status for {service['Application']}")
        try:
            status = get_status_code(service['url'])
        except Exception as e:
            logger.error(f"Error getting status for {service['Application']}. Changing tagstyle to is-danger\nError: {e}")
            update_tagstyle(config_file, service['Application'], "is-danger")
            continue

        """Check status and update tagstyle"""
        if status in SUCCESSFUL_STATUS_CODES:
            logger.info(f"{service['Application']} is up")
            update_tagstyle(config_file, service['Application'], "is-success")
        else:
            logger.info(f"{service['Application']} has status of of {status}. Updating tagstyle to is-danger")
            update_tagstyle(config_file, service['Application'], "is-danger")

if __name__ == '__main__':
    
    start_time = time.time()    
    """setup logging"""
    logger = get_logger()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))