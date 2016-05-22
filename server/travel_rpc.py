import argparse
import datetime
import logging
import SimpleXMLRPCServer

import travel


HOST = "localhost"
PORT = 8888
PATH = "/travel"


def handle_command_line():
    parser = argparse.ArgumentParser(conflict_handler="resolve")
    parser.add_argument("-h", "--host", default=HOST, metavar="host")
    parser.add_argument("-p", "--port", default=PORT, metavar="port")
    parsed_args = parser.parse_args()
    return parsed_args.host, parsed_args.port


def setup_logging():
    logging.basicConfig(
        format='%(asctime)s %(filename)s %(funcName)s:%(lineno)d %(levelname)s:%(message)s',
        level=logging.INFO,
    )


def setup(host, port):
    travel_manager = travel.Manager()
    server = SimpleXMLRPCServer.SimpleXMLRPCServer(
        (host, port), requestHandler=RequestHandler, logRequests=False)
    server.register_introspection_functions()
    for method in (
            travel_manager.login,
            travel_manager.get_cities_for_country,
            travel_manager.add_country,
            travel_manager.add_city_for_country):
        server.register_function(method)

    return travel_manager, server


class RequestHandler(SimpleXMLRPCServer.SimpleXMLRPCRequestHandler):
    rpc_paths = (PATH,)


def main():
    host, port = handle_command_line()
    setup_logging()
    travel_manager, server = setup(host, port)

    logging.info("Meter server startup at {} on {}: {}{}".format(
        datetime.datetime.now(), host, port, PATH))

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logging.info("Meter server shutdown at {}".format(
            datetime.datetime.now()))


if __name__ == "__main__":
    main()
