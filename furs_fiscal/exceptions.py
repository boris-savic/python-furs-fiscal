
class FURSException(Exception):
    """
    FURS Exception will be thrown if there was an error communicating with the FURS server.

    FURSException contains both code and message of what went wrong.
    """
    def __init__(self, code, message):
        self.code = code
        self.message = message

        super(FURSException, self).__init__(message)

    def __str__(self):
        return repr("[Code: %s]%s" % (self.code, self.message))


class ConnectionTimedOutException(Exception):
    """
    ConnectionTimedOutException will be thrown if the connection timed out
    """
    pass


class ConnectionException(Exception):
    """
    Connection Exception will be thrown if the server responds with anything else than status code 200
    """
    def __init__(self, code, message):
        self.code = code,
        self.message = message

        super(ConnectionException, self).__init__(message)

    def __str__(self):
        return repr("[Code: %s]%s" % (self.code, self.message))
