import xml.etree.ElementTree as ET
import re
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------------------------
# validates if the version is a valid semantic version
# input: version - string
# output: boolean
# --------------------------------------------------------------------------------------------
def valid_semantic_version(version):
    pattern = r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
    return bool(re.match(pattern, version))


def get_current_version(pom_file):
    tree = ET.parse(pom_file)
    
    root = tree.getroot()
    print("Root tag: " + root.tag)
    
    for child in root:
        
        if 'version' in child.tag:
            return child.text

    return None

def increase_version(version, version_type):
    major, minor, patch = re.match(r"(\d+)\.(\d+)\.(\d+)", version).groups()

    if version_type == "major":
        major = str(int(major) + 1)
    elif version_type == "minor":
        minor = str(int(minor) + 1)
    elif version_type == "patch":
        patch = str(int(patch) + 1)

    return major + '.' + minor + '.' + patch

def main():
    pom_file = 'P:\homelab\pom_v_mgr\\test\sample-POM.xml'  # replace with your POM file path
    version_type = "patch"  # replace with "major", "minor", or "patch"

    current_version = get_current_version(pom_file)
    print(valid_semantic_version(current_version)) 
    if current_version is not None:
        print("Current version is: " + current_version)
        new_version = increase_version(current_version, version_type)
        print("Increased version is: " + new_version)
    else:
        print("Version not found in POM file")

if __name__ == "__main__":
    main()
