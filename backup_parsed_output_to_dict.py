import sys
import json
import logging
from nomad.client import parse, normalize_all
from nomad.utils import configure_logging
from nomad.datamodel import EntryArchive
from electronicparsers.vasp import VASPParser

configure_logging(console_log_level=logging.DEBUG)

archive = EntryArchive()
VASPParser().parse(sys.argv[1], archive, logging)
# json.dump(archive.m_to_dict(), sys.stdout, indent=2)

archive_dict = archive.m_to_dict()


energies = archive_dict['run'][0]['calculation'][0]['energy']
print(energies)




# def print_dict(d, indent=0):
#     """Recursively print a dictionary with indentation."""
#     for key, value in d.items():
#         if isinstance(value, dict):
#             print(' ' * indent + str(key) + ':')
#             print_dict(value, indent + 2)
#         else:
#             print(' ' * indent + str(key) + ':', value)


# print_dict(archive_dict)