# Main Logic

The first observation is that we can reduce the problem to a 2D point overlap with rectangle problem by considering each case (inbound, TCP), (inbound, UDP), (outbound, TCP) and (outbound, UDP) separately. After doing this, we can see that each rule is two intervals: one interval in the port space and another interval in the IP space. This can be visualized as a rectangle and each packet can be visualized as a point. Now, we just need to check if a point belongs to at least one rectangle. 

The next observation is that accept_packet queries can be executed in O(1) if we store a 2D array of (all ports x all IP Addresses). However, this takes an enormous amount of space. So, we can construct bins for both ports and IP Addresses that span across a particular range. For example, we can have bins of 10000 ports which means that rules that have ports between 1-10000 belong to the first bin, rules that have ports between 100001-20000 in the second bin and so on. For IP Addresses, bins were constructed using only the first field for simplicity. For example, if the bin size is specified to be 10, then all IPs between (0-9.255.255.255) belong to the first bin and so on. We can have different bin sizes for ports and IP Addresses.

Now, each rule can belong to one or more bins and each packet belongs to exactly bin and all rules in that bin are checked to see if they can accept that packet.

# Optimizations that could be performed

* After a packet is determined to be in a particular bin, all rules are checked within that bin using a linear scan approach. This can be optimized further by using 2D binary search.
* We can resize the bins dynamically to reduce cost of searching in bins that are highly populated.

# Testing
* Naive cases like rules spanning across all IPs were considered.
* Bucket size of size 1 was considered. 
* Packets belonging to boundaries of rules were considered to see if they are accepted.
* Normal inputs were considered.

# Running
* Tests can be run using `python3 test.py`
* firewall module needs to be imported if it needs to be used in other files.

# Teams Interested
* Platform Team
* Policy Team
