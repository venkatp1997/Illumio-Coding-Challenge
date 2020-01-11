import firewall

if __name__ == "__main__":
    fw1 = firewall.Firewall("test.csv", 1, 1)
    fw2 = firewall.Firewall("test.csv", 65535, 256)
    fw3 = firewall.Firewall("test.csv")

    assert (fw1.accept_packet("inbound", "tcp", 80, "192.168.1.2") == True), "Test Case-1 Failed"
    assert (fw1.accept_packet("inbound", "udp", 53, "192.168.2.1") == True), "Test Case-2 Failed"
    assert (fw1.accept_packet("outbound", "tcp", 10234, "192.168.10.11") == True), "Test Case-3 Failed"
    assert (fw1.accept_packet("inbound", "tcp", 81, "192.168.1.2") == False), "Test Case-4 Failed"
    assert (fw1.accept_packet("inbound","udp", 24,"52.12.48.92") == False), "Test Case-5 Failed"

    assert (fw2.accept_packet("inbound", "tcp", 80, "192.168.1.2") == True), "Test Case-6 Failed"
    assert (fw2.accept_packet("inbound", "udp", 53, "192.168.2.1") == True), "Test Case-7 Failed"
    assert (fw2.accept_packet("outbound", "tcp", 10234, "192.168.10.11") == True), "Test Case-8 Failed"
    assert (fw2.accept_packet("inbound", "tcp", 81, "192.168.1.2") == False), "Test Case-9 Failed"
    assert (fw2.accept_packet("inbound","udp", 24,"52.12.48.92") == False), "Test Case-10 Failed"

    assert (fw3.accept_packet("inbound", "tcp", 80, "192.168.1.2") == True), "Test Case-11 Failed"
    assert (fw3.accept_packet("inbound", "udp", 53, "192.168.2.1") == True), "Test Case-12 Failed"
    assert (fw3.accept_packet("outbound", "tcp", 10234, "192.168.10.11") == True), "Test Case-13 Failed"
    assert (fw3.accept_packet("inbound", "tcp", 81, "192.168.1.2") == False), "Test Case-14 Failed"
    assert (fw3.accept_packet("inbound","udp", 24,"52.12.48.92") == False), "Test Case-15 Failed"
