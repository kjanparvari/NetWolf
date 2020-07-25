from netwolf import Members
from netwolf import Serialization
from netwolf import Manager


def main():
    # from netwolf.Serialization import serialize, deserialize
    # from netwolf.Members import Member, MembersManager
    Manager.Manager().tmp()
    # members = [Member("member 1", "192.168.1.1"), Member("member 2", "192.168.1.2"),
    #            Member("member 3", "192.168.1.3"),
    #            Member("member 4", "192.168.1.4"), Member("member 5", "192.168.1.5"),
    #            Member("member 6", "192.168.1.6")]
    # mm = MembersManager(None)
    # s = serialize(members)
    # d = deserialize(s)
    # mm.printList(d)


if __name__ == '__main__':
    main()
