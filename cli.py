import argparse
from typing import Optional
from typing import Sequence
from interface.common.validation import Validations
from interface.utilities.remote_client import RemoteClientUtility
from interface.utilities.package_util import PackageVersionIncrement, LatestPackage
from interface.common.constants import ErrorCodesMessages
from interface.pages.configration import load_configuration

def package_validation(package_name: str) -> str:
    """
    Package Name validation for maintaining standards
    """
    validation = Validations()
    if validation.check_artifact_string(package_name) is False:
        return ErrorCodesMessages.PKG_NAME_ERR.value
    return package_name


def cli(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description='ADHOC package Utility CLI tool commands')

    parser.add_argument(
        '-p', '--package', type=package_validation,
        default='',
        help='''package name as per Standards\
            DEPLOYME-10.XX.XXX.XXXX (default: %(default)s)''')

    # sub-commands
    subparsers = parser.add_subparsers(
        dest='command',
        help='commands')
    subparsers.required = True

    status_parser = subparsers.add_parser(
        'create', help="create package of unix or database type")
    status_parser.add_argument(
        '-t', '--type',
        choices=('unix', 'database'),
        default="unix",
        help="unix/database type category package (default: %(default)s)")
    status_parser.add_argument(
        '-s', '--script_name', default="deployment.sh",
        help="deployment script Name (default: %(default)s)")

    test_parser = subparsers.add_parser(
        'test',
        help="test artifact with environment config")
    test_parser.add_argument(
        '-e', '--env', default="ASIA",
        choices=('ASIA', 'EMEA', 'NAM', 'SEPA', 'AMER', 'DATABASE'),
        help="test with Environment config file\
            placed inside package (default: %(default)s)")

    upgrade_parser = subparsers.add_parser(
        'upgrade', help="upgrade package version Major Minor Release")
    upgrade_parser.add_argument(
        '-u', '--upgrade_version',
        default="release",
        choices=('major', 'minor', 'release', 'backout'),
        help="upgrade package version (default: %(default)s)")

    parser.add_argument(
        '-V', '--version',
        action='version', version='%(prog)s 1.0.0')

    args = parser.parse_args(argv)

    return vars(args)


def main():
    commands = cli()

    print(f"Paramter Selected: {commands}\n")

    config = load_configuration()

    PKG = LatestPackage(config['repo_config'], config['serv_config'], config['artf_config']).get_latest_local()
    if commands.get('package') is None:
        v = f'DEPLOYME-10.0.0.{PKG}'
        PACKAGE_NAME = PackageVersionIncrement().increment_package_ver(v)
    else:
        PACKAGE_NAME = commands.get('package')

    if commands.get('command') == "create":
        serverClient = RemoteClientUtility(config['serv_config'], config['repo_config'])
        if commands.get('script_name') is None:
            script_name = 'deployment_script.sh'
        else:
            script_name = commands.get('script_name')
        output = serverClient.execute_package_utility(
            PACKAGE_NAME,
            commands.get('type'),
            script_name)
        print(f"{output[0][0]}")

    if commands.get('command') == "test":
        serverClient = RemoteClientUtility(config['serv_config'], config['repo_config'])
        output = serverClient.execute_package_utility(
            PACKAGE_NAME,
            commands.get('command'),
            commands.get('env'))
        string = ""
        print(f"{string.join(output[0])}")

    if commands.get('command') == "upgrade":
        serverClient = RemoteClientUtility(config['serv_config'], config['repo_config'])
        if commands.get('upgrade_version') == "major":
            UPGRADE_NAME = PackageVersionIncrement().\
                upgrade_pkg_major_ver(PACKAGE_NAME)
        elif commands.get('upgrade_version') == "minor":
            UPGRADE_NAME = PackageVersionIncrement().\
                upgrade_pkg_minor_ver(PACKAGE_NAME)
        elif commands.get('upgrade_version') == "backout":
            UPGRADE_NAME = PackageVersionIncrement().\
                backout_package_ver(PACKAGE_NAME)
        else:
            UPGRADE_NAME = PackageVersionIncrement().\
                increment_package_ver(PACKAGE_NAME)
        output = serverClient.execute_package_utility(
            PACKAGE_NAME,
            commands.get('command'),
            UPGRADE_NAME)
        string = ""
        if output[0] != []:
            print(string.join(output[0]))
        else:
            print(output[1][0])

if __name__ == "__main__":
    exit(main())