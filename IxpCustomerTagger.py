from AtlasTracerouteTagger import AtlasTracerouteTagger
from ripe.atlas.sagan import TracerouteResult
import radix


class IxpCustomerTagger(AtlasTracerouteTagger):
    radix_t = None

    def __init__(self, cust_networks=None):
        self.radix_t = radix.Radix()
        self.labels = ['IXP-customer', 'non-IXP-customer']
        for network in cust_networks:
            self.radix_t.add(network=network)

    def tag(self, tr_r):
        # Validate the object received is of the right type
        if not isinstance(tr_r, TracerouteResult):
            raise TypeError("Parameter provided is not of the right type")

        # Lookup in the list of customer networks the source address of this
        # traceroute
        entry = self.radix_t.search_best(network=tr_r.source_address)
        if entry is not None:
            return 'IXP-customer'
        else:
            return 'non-IXP-customer'

    def name_probe(self, tag, probe_id):
        if tag == 'IXP-customer':
            return "C%d" % probe_id
        else:
            return "NC%d" % probe_id

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
