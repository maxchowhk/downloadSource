import subprocess
import sys

def get_zone_identifier(file_path):
    command = f'more < "{file_path}:Zone.Identifier"'
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        if 'The system cannot find the file specified' in e.output:
            return 'No Zone.Identifier found.'
        else:
            return f'Error: {e.output}'
    return output

def interpret_zone_id(zone_id):
    zone_names = {
        '0': 'Local machine',
        '1': 'Local intranet',
        '2': 'Trusted sites',
        '3': 'Internet',
        '4': 'Restricted sites'
    }
    return zone_names.get(str(zone_id), 'Unknown ZoneId')

def find_url_in_identifier(zone_identifier):
    lines = zone_identifier.split('\n')
    for line in lines:
        if line.startswith('ReferrerUrl') or line.startswith('HostUrl'):
            return line.split('=')[-1].strip()
    return 'No ReferrerUrl or HostUrl found.'

def find_ultimate_source(zone_id, url):
    if zone_id == '0':
        return 'The file was likely created or downloaded directly on this machine.'
    elif zone_id == '1':
        return 'The file likely came from an intranet source.'
    elif zone_id == '2':
        return 'The file likely came from a trusted site.'
    elif zone_id == '3':
        return f'The file was downloaded from the internet. The source URL may be: {url}'
    elif zone_id == '4':
        return 'The file likely came from a restricted site.'
    else:
        return 'The ultimate source of the file could not be determined from the ZoneId.'

def main():
    if len(sys.argv) < 2:
        print('Usage: python script.py [file_path]')
        return

    file_path = sys.argv[1]
    zone_identifier = get_zone_identifier(file_path)

    if 'ZoneId' in zone_identifier:
        zone_id = zone_identifier.split('ZoneId=')[-1].strip().split('\n')[0]
        print(f'ZoneId: {zone_id} ({interpret_zone_id(zone_id)})')

        url = find_url_in_identifier(zone_identifier)
        if zone_id == '3' and url != 'No ReferrerUrl or HostUrl found.':
            print(f'URL: {url}')
        source = find_ultimate_source(zone_id, url)
        print(f'Source Analysis: {source}')
    else:
        print(zone_identifier)

if __name__ == '__main__':
    main()
