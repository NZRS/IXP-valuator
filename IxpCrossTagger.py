from AtlasTracerouteTagger import AtlasTracerouteTagger
from ripe.atlas.sagan import TracerouteResult
import radix


class IxpCrossTagger(AtlasTracerouteTagger):
    ixp_networks = []
    radix_t = None

    def __init__(self, ixp_networks=None):
        self.radix_t = radix.Radix()
        for network in ixp_networks:
            self.radix_t.add(network=network)

    def tag(self, tr_r):
        # Validate the object received is of the right type
        if not isinstance(tr_r, TracerouteResult):
            raise TypeError("Parameter provided is not of the right type")

        # Iterate over the list of address in the traceroute
        # if there is an address in the IXP (local, non-local) return the tag
        for hop in tr_r.hops:
            addr_in_hop = set()
            for packet in hop.packets:
                if packet.origin is not None:
                    addr_in_hop.add(packet.origin)

            for addr in addr_in_hop:
                # Lookup with address in the Radix Table of known IXPs
                # TODO: Figure it out the right mask depending on the address
                #  family
                entry = self.radix_t.search_best(network=addr)
                # If found, return the tag we have
                if entry is not None:
                    return 'IXP'

        # If we reach this point, none of the addresses matched a known IXP
        return 'no-IXP'

    def extract_hop_count(self, tr_r):
        return tr_r.total_hops

    def extract_max_rtt(self, tr_r):
        # Rather that finding the max value, we look at the last hop in the
        # trace and use the corresponding RTT
        for hop in reversed(tr_r.hops):
            addr_in_hop = set()
            rtt_sum = 0.0
            rtt_cnt = 0
            for packet in hop.packets:
                if packet.origin is not None:
                    addr_in_hop.add(packet.origin)
                if packet.rtt is not None:
                    rtt_sum += packet.rtt
                    rtt_cnt += 1

            if len(addr_in_hop) > 0:
                # This one is good to use
                rtt_avg = rtt_sum / rtt_cnt
                return rtt_avg

        return 0
