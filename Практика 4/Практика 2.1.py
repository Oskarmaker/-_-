class Dict:
    def __init__(self, **kwargs):
        self.buckets = [[] for _ in range(8)]
        self.size = 0
        for key, value in kwargs.items():
            self[key] = value

    def __setitem__(self, key, value):
        bucket = self.buckets[hash(key) % len(self.buckets)]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self.size += 1
        if self.size > len(self.buckets) * 0.75:
            self.resize()

    def __getitem__(self, key):
        bucket = self.buckets[hash(key) % len(self.buckets)]
        for k, v in bucket:
            if k == key:
                return v
        raise KeyError(key)

    def __len__(self):
        return self.size

    def __delitem__(self, key):
        bucket = self.buckets[hash(key) % len(self.buckets)]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self.size -= 1
                return
        raise KeyError(key)

    def __iter__(self):
        for bucket in self.buckets:
            for key, _ in bucket:
                yield key

    def __contains__(self, key):
        try:
            _ = self[key]
            return True
        except KeyError:
            return False

    def resize(self):
        old_buckets = self.buckets
        self.buckets = [[] for _ in range(len(self.buckets) * 2)]
        self.size = 0
        for bucket in old_buckets:
            for key, value in bucket:
                self[key] = value

    def __repr__(self):
        items = []
        for bucket in self.buckets:
            for key, value in bucket:
                items.append(f"{key!r}: {value!r}")
        return "{" + ", ".join(items) + "}"


def test_my_dict():
    d = Dict()
    d['a'] = 1
    assert d['a'] == 1
    assert len(d) == 1
    assert 'a' in d

    d = Dict(b=2, c=3)
    assert d['b'] == 2
    assert d['c'] == 3
    del d['b']
    assert 'b' not in d

    keys = list(d)
    assert keys == ['c']


if __name__ == "__main__":
    test_my_dict()
