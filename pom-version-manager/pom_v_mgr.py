import argparse
from enum import Enum
import sys
import xml.etree.ElementTree as ET
import re
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# -----------------------------------------------------------------------------------------------------------------------
# VersionType an enum for the version types
# description: Using an enum to minimize typing mistakes
# MAJOR = "major", MINOR = "minor", PATCH = "patch", PRERELEASE = "prerelease", BUILDMETADATA = "buildmetadata"
# more info https://semver.org/#backusnaur-form-grammar-for-valid-semver-versions
# -----------------------------------------------------------------------------------------------------------------------
class VersionType(Enum):
    MAJOR = "major"
    MINOR = "minor"
    PATCH = "patch"
    PRERELEASE = "prerelease"
    BUILDMETADATA = "buildmetadata"
# end-class
    

# --------------------------------------------------------------------------------------------
# validates if the version is a valid semantic version
# https://semver.org/ for more information
# input: version - string
# output: boolean
# --------------------------------------------------------------------------------------------
def valid_semantic_version(version):
    logger.debug(f'Validating version {version}')
    if version:
        pattern = r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
        return bool(re.match(pattern, version))
    else:
        return False
# end-def


# --------------------------------------------------------------------------------------------
# extract version parts from a semantic version
# input: version - string
# output: tuple of strings (major, minor, patch, prerelease, buildmetadata)
# --------------------------------------------------------------------------------------------
def extract_version_part(version, version_type : VersionType):
    if version:
        pattern = r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
        match = re.match(pattern, version)
        if match:
            return match.group(version_type.value)
        # end-if
    
    # nothing found for the requested part
    return ''
# end-def


# --------------------------------------------------------------------------------------------
# updates or if not present, inserts the release candidate version part (-RC.1, -RC.2, etc)
# input: version - string
# output: string, the new release candidate version
# --------------------------------------------------------------------------------------------
def upsert_release_candidate(version):
    prerelease = extract_version_part(version, VersionType.PRERELEASE)

    if prerelease:
        # if the prerelease is a SNAPSHOT, then replace it with RC.1
        if 'SNAPSHOT' in prerelease.upper():
            return 'RC.1'
            
        prerelease_number = re.search(r'\d+', prerelease)
        if prerelease_number:
            return re.sub(r'\d+', str(int(prerelease_number.group()) + 1), prerelease)
    else:
        return 'RC.1'
# end-def
     

# --------------------------------------------------------------------------------------------
# gets the current version from the POM file
# input: pom_file - string
# output: string, the version
# --------------------------------------------------------------------------------------------
def get_current_version(pom_file):
    
    logger.debug(f'Getting current version from {pom_file}')
    tree = ET.parse(pom_file)
    root = tree.getroot()
    for child in root:     
        if 'version' in child.tag:
            logger.debug(f'Version tag found: {child.text}')
            return child.text

    return None
# end-def


# --------------------------------------------------------------------------------------------
# saves the new version to the POM file
# input: version - string
#        pom_file - string
# output: none
# --------------------------------------------------------------------------------------------
def change_pom_version(version, pom_file):
    
    logger.debug(f'Saving current version {version} to {pom_file}')
    tree = ET.parse(pom_file)
    root = tree.getroot()
    for child in root:     
        if 'version' in child.tag:
            logger.debug(f'Version tag found: {child.text}')
            child.text = version
            break
        # end-if
    # end-for

    tree.write(pom_file)
# end-def

# --------------------------------------------------------------------------------------------
# generates a release candidate version
# input: version - string
# output: string, the new version
# --------------------------------------------------------------------------------------------
def generate_release_candidate(version):
    prerelease = extract_version_part(version, VersionType.PRERELEASE)
    if 'SNAPSHOT' in prerelease.upper():
        prerelease = prerelease.replace('SNAPSHOT', 'RC.1')
    
# end-def


# --------------------------------------------------------------------------------------------
# increases the version based on the version type
# input: version - string
#        version_type - VersionType enum (MAJOR, MINOR, PATCH, PRERELEASE, BUILDMETADATA)
# output: string, the new version
# --------------------------------------------------------------------------------------------
def increase_version(version, version_type : VersionType):
    
    major = extract_version_part(version, VersionType.MAJOR)
    minor = extract_version_part(version, VersionType.MINOR)
    patch = extract_version_part(version, VersionType.PATCH)
    prerelease = extract_version_part(version, VersionType.PRERELEASE)
    buildmetadata = extract_version_part(version, VersionType.BUILDMETADATA)
    
    logger.debug(f'Actual version parts: major={major}, minor={minor}, patch={patch}, prerelease={prerelease}, buildmetadata={buildmetadata}')
    
    if version_type == VersionType.MAJOR:
        major = str(int(major) + 1)
    elif version_type == VersionType.MINOR:
        minor = str(int(minor) + 1)
    elif version_type == VersionType.PATCH:
        patch = str(int(patch) + 1)
    elif version_type == VersionType.PRERELEASE:
        prerelease = upsert_release_candidate(version)
        
    logger.debug(f'Generated version parts: major={major}, minor={minor}, patch={patch}, prerelease={prerelease}, buildmetadata={buildmetadata}')
    
    return f'{major}.{minor}.{patch}{ "" if prerelease is None else "-"+prerelease }{"" if buildmetadata is None else "+"+buildmetadata }'
# end-def


# ---------------------------------------------------------------------------------------------------
# parse_arguments - parses arguments received from command line.
#
# This function will read and validate against specified rules the supplied arguments
# from command line
# ---------------------------------------------------------------------------------------------------
def parse_arguments(args=sys.argv[1:]):

    root_parser = argparse.ArgumentParser(description="POM version manager :: Manage versions with no further dependencies", prog="pom_v_mgr")
    
    command_parser = root_parser.add_subparsers(dest='command', title="Available commands")
    
    increase = command_parser.add_parser('increase', help='Increase Version of POM file')
    increase.add_argument('-t', "--type", help="Version type to be increase", choices=[VersionType.MAJOR.value, VersionType.MINOR.value, VersionType.PATCH.value, VersionType.PRERELEASE.value, VersionType.BUILDMETADATA.value], required=True)
    increase.add_argument('-p', "--pom", help="POM file path", required=True)

    dry_run = command_parser.add_parser('dry-run', help='Shows the new version without changing the POM file')
    dry_run.add_argument('-t', "--type", help="Version type to be increase", choices=[VersionType.MAJOR.value, VersionType.MINOR.value, VersionType.PATCH.value, VersionType.PRERELEASE.value, VersionType.BUILDMETADATA.value], required=True)
    dry_run.add_argument('-p', "--pom", help="POM file path", required=True)
    
    #if no args passed print help and exit 
    if not args:
        root_parser.print_help()
        sys.exit(2)
    #end-if

    return root_parser.parse_args(args)

# end-def


def main(args):
    
    # get parsed command line arguments
    options = parse_arguments(args)
    
    pom_file = options.pom
    # cast the version type to the enum
    version_type = VersionType(options.type)
    logger.info(f'Increasing "{version_type.value}" version in {pom_file}')
    current_version = get_current_version(pom_file)
    if (valid_semantic_version(current_version)):
        logger.info(f'Current version is: {current_version}')
        new_version = increase_version(current_version, version_type)
        logger.info(f'New version is: {new_version}')
        
        if options.command == 'increase':
            change_pom_version(new_version, pom_file)
            logger.info(f'Version updated in {pom_file}')
    else: 
        logger.warning(f'Version "{current_version}" is NOT valid.')
    # end-if
# end-def


if __name__ == "__main__":
    main(sys.argv[1:])
    

