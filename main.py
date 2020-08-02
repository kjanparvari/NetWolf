# from netwolf import Manager


def main():
    # Manager.Manager().tmp()
    from netwolf.Serialization import encode, decode
    HEADER = 64
    msg_length = 143
    send_length = str(msg_length)
    for i in range(0, HEADER - len(str(msg_length))):
        send_length += " "
    print(len(send_length))
    print(int(send_length))


if __name__ == '__main__':
    main()
