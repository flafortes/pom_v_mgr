# POM Semver Version Manager

If you're looking to update the version of your Java-based POM application, but you're reluctant or unable to introduce additional Maven tools due to the necessity of extra dependencies, we've got you covered.

This straightforward script is specifically designed to help you effortlessly increment the versions, without adding any further requirements.
We adhere strictly to the [Semantic Versioning](https://semver.org/) (SemVer) standard, providing you with the ability to enhance Major, Minor, Patch, and Prerelease versions at will. Dive in and simplify your versioning process today!

This Python script allows you to manage versions in a Project Object Model (POM) file according to the [Semantic Versioning](https://semver.org/) (SemVer) standard. The `pom_v_mgr.py` script reads the current version from a POM file and increases the major, minor, or patch version as specified.


### Maven Tools for Version Management

Maven offers a number of tools and plugins designed to streamline and automate version management for your projects:

1. **Maven Versions Plugin**: A versatile tool for managing versions in your POM files, this plugin can update dependency versions, plugin versions, and even the project version itself. It offers a variety of goals including:
2. **Maven Release Plugin**: This plugin simplifies release management, including version control. It provides a two-step release process:

While these tools can be invaluable for managing version control, they also add complexity and require a suitable Maven environment. If you're looking for a simpler solution or wish to avoid adding these dependencies, consider using simple scripts or other version management methods.


## Prerequisites

This script requires Python 3.5 or later.
Understand that this script is designed to work with POM files that follow the [Semantic Versioning](https://semver.org/) standard. If your POM file does not follow this standard, the script will not work as expected.


## Usage

To utilize this script, you can use the following command structure:

```python
pom_v_mgr.py increase --type <version_type> --pom <path_to_your_pom_file>
```

For instance, if you wish to increment the prerelease version of your POM file located at `sample-POM.xml`, you would execute the following command:

```python
pom_v_mgr.py increase --type prerelease --pom 'sample-POM.xml'
```

Simply replace `<version_type>` with the version type you want to increase (major, minor, patch, prerelease), and `<path_to_your_pom_file>` with the path to your POM file.


## License

This project is licensed under the terms of the MIT license.

## Contributing

Please feel free to submit issues, fork the repository and send pull requests!
