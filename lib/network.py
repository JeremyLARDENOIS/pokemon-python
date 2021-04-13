####SERVER
import sys

verbose = sys.argv[0].endswith("server.py")

def send_msg (conn,msg):
    """Send a message msg to conn connection
    Arguments: conn, msg
    """
    msg = str(msg)
    data = msg.encode("utf-8")
    conn.sendall(data)
    addr = str(conn).split(',')[6].split("'")[1]    #Get IP from conn
    port = str(conn).split(',')[7].split(")")[0][1:]#Get port from conn
    if (verbose):
        print(addr,port,"->", msg)

def recv_msg (conn):
    """ Get a message from conn connection
    Arguments: conn
    Return: msg
    """
    data = conn.recv(255)
    msg  = data.decode("utf-8")
    addr = str(conn).split(',')[6].split("'")[1]    #Get IP from conn
    port = str(conn).split(',')[7].split(")")[0][1:]#Get port from conn
    if (verbose):
        print(addr,port,"<-", msg)
    return msg

def send (conn,msg):
    """
    Allow to send a message msg on a connection conn on a safe way    
    Arguments: conn, msg
    """
    send_msg(conn,"READ");          # Send "READ"
    status = recv_msg(conn)         # Recv status
    # If status is "OK", we send the message 
    if (status == "OK"):            
        send_msg(conn,msg);         
        status = recv_msg(conn)    
        # While status isn't "OK", we send the message again 
        while (status != "OK"):   
            send_msg(conn,msg)
            status = recv_msg(conn)
    # If status isn't "OK", we try again
    else:
        send(conn,msg)

def recv (conn):
    """
    Allow to receive a message msg from a connection conn on a safe way    
    Arguments: conn
    Return: msg
    """
    send_msg(conn,"WRITE")          # Send "WRITE"
    msg = recv_msg(conn)            # We receive the message
    if (msg == ""):                 # If no message, try again
        msg = recv(conn)
    else:                           # If receive something
        send_msg(conn,"OK")         # Send "OK"
        recv_msg(conn)              # Client answer "OK" too
    return msg

def broadcast(conns, msg):
    """
    Send a message to all users
    Arguments: msg
    """
    for conn in conns:
        send(conn,msg)

def recv2(conns):
    """
    Receive message from all users
    Returns: (msg1, msg2)
    """
    conn1 = conns[0]
    conn2 = conns[1]

    send_msg(conn1,"WRITE2")        # Send "WRITE2" to player 1
    send_msg(conn2,"WRITE2")        # Send "WRITE2" to player 2
    
    status1 = recv_msg(conn1)       # Receive status from player 1
    status2 = recv_msg(conn2)       # Receive status from player 2

    # If all status is "OK"
    if ((status1 == "OK")and(status2 == "OK")):
        send_msg(conn1,"SEND")      # Send "SEND" to player 1
        msg1 = recv_msg(conn1)      # Receive msg from player 1
        send_msg(conn2,"SEND")      # Send "SEND" to player 2
        msg2 = recv_msg(conn2)      # Receivemsg from player 2
        send_msg(conn1,"OK")        # Send "OK" to player 1
        recv_msg(conn1)             # Receive status from player 1
        send_msg(conn2,"OK")        # Send "OK" to player 2
        recv_msg(conn2)             # Receive status from player 2
    else:                           # If one of status isn't "OK"
        return recv2()              # Try again

    return (msg1,msg2)


### CLIENT

# def send_msg (msg):
#     """
#     Send a message to server
#     Argument: msg
#     """
#     data = msg.encode("utf-8")
#     socket.sendall(data)

# def recv_msg ():
#     """
#     Receive a message from server
#     Return: msg
#     """
#     data = socket.recv(255)
#     msg = data.decode("utf-8") 
#     return msg



