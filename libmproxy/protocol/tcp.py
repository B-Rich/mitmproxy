from __future__ import absolute_import
import select, socket
from .primitives import ProtocolHandler

class TCPHandler(ProtocolHandler):
    """
    TCPHandler acts as a generic TCP forwarder.
    Data will be .log()ed, but not stored any further.
    """

    chunk_size = 4096

    def handle_messages(self):
        self.c.establish_server_connection()

        server = "%s:%s" % self.c.server_conn.address()[:2]
        buf = memoryview(bytearray(self.chunk_size))

        conns = [self.c.client_conn.rfile, self.c.server_conn.rfile]
        while not self.c.close:
            r, _, _ = select.select(conns, [], [], 10)
            for rfile in r:
                if self.c.client_conn.rfile == rfile:
                    src, dst = self.c.client_conn, self.c.server_conn
                    direction = "-> tcp ->"
                    src_str, dst_str = "client", server
                else:
                    dst, src = self.c.client_conn, self.c.server_conn
                    direction = "<- tcp <-"
                    dst_str, src_str = "client", server

                closed = False
                if src.ssl_established:
                    # Unfortunately, pyOpenSSL lacks a recv_into function.
                    contents = src.rfile.read(1)  # We need to read a single byte before .pending() becomes usable
                    contents += src.rfile.read(src.connection.pending())
                    if not contents:
                        closed = True
                else:
                    size = src.connection.recv_into(buf)
                    if not size:
                        closed = True

                if closed:
                    conns.remove(src.rfile)
                    # Shutdown connection to the other peer
                    if dst.ssl_established:
                        dst.connection.shutdown()
                    else:
                        dst.connection.shutdown(socket.SHUT_WR)

                    if len(conns) == 0:
                        self.c.close = True
                    continue

                if src.ssl_established or dst.ssl_established:
                    # if one of the peers is over SSL, we need to send bytes/strings
                    if not src.ssl_established:  # only ssl to dst, i.e. we revc'd into buf but need bytes/string now.
                        contents = buf[:size].tobytes()
                    self.c.log("%s %s\r\n%s" % (direction, dst_str, contents[:100]), "debug")
                    dst.connection.send(contents)
                else:
                    # socket.socket.send supports raw bytearrays/memoryviews
                    self.c.log("%s %s\r\n%s" % (direction, dst_str, buf[:100]), "debug")
                    dst.connection.send(buf[:size])