import fudge

from armstrong.utils.backends.base import BackendDidNotHandle


TestArgs = fudge.Fake().expects('__init__').with_args('arg1', kw=1)


class Skip(object):
    func = fudge.Fake().is_callable()\
        .with_args('arg1', kw=1).raises(BackendDidNotHandle)


class UseThisOne(object):
    func = fudge.Fake().is_callable()\
        .with_args('arg1', kw=1).returns("backend returned me")
