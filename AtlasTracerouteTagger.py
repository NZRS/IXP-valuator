import radix


class AtlasTracerouteTagger:
    labels = []
    radix_t = None

    def __init__(self):
        self.labels = [None]

    def labels(self):
        return self.labels

    def tag(self, tr_obj):
        """
        :param tr_obj: RIPE Atlas traceroute object
        :return: a string with a label
        """

        # Dummy method
        return None

    def extract_hop_count(self, tr_r):
        """
        :param tr_r: RIPE Atlas traceroute object
        :return: a number representing a metric extracted from the traceroute object
        """
        return None

    def extract_max_rtt(self, tr_r):
        return None
