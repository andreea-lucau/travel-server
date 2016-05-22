import argparse
import getpass
import textwrap
import xmlrpclib

HOST = "localhost"
PORT = 8888
PATH = "/travel"


def handle_command_line():
    parser = argparse.ArgumentParser(conflict_handler="resolve")
    parser.add_argument("-h", "--host", default=HOST, metavar="host")
    parser.add_argument("-p", "--port", default=PORT, metavar="port")
    parsed_args = parser.parse_args()
    return parsed_args.host, parsed_args.port


def login():
    username = getpass.getuser()
    password = getpass.getpass()
    if not password:
        return None, None
    print '[', password, ']'
    return username, password


def print_usage():
    options = textwrap.dedent("""\
        Options:
            add_country <country> <cities>
            add_city <country> <city>
            get <country>
            quit
            """)
    print options



def interact(manager, sessionId):
    print_usage()

    while True:
        option = raw_input("Option:")
        if option == "quit":
            return
        elif option.startswith("add_country "):
            option, country, cities = option.split(" ")
            manager.add_country(sessionId, country, cities.split(","))
        elif option.startswith("add_city "):
            option, country, city = option.split(" ")
            manager.add_city_for_country(sessionId, country, city)
        elif option.startswith("get "):
            option, country = option.split(" ")
            print manager.get_cities_for_country(sessionId, country)
        else:
            print "Unknown option: '{}".format(option)


def main():
    host, port = handle_command_line()
    username, password = login()
    if username:
        try:
            manager = xmlrpclib.ServerProxy(
                    'http://{}:{}{}'.format(host, port, PATH))
            sessionId, name = manager.login(username, password)
            print "Welcome, {}, to travel manager".format(name)
            interact(manager, sessionId)
        except Exception as ex:
            print "Communication failure: %s", str(ex)
            raise ex

if __name__ == "__main__":
    main()
