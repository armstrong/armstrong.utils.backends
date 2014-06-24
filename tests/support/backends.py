import fudge

from armstrong.utils.backends.base import DID_NOT_HANDLE


TestArgs = fudge.Fake().expects('__init__').with_args('arg1', kw=1)


class Skip(object):
    func = fudge.Fake().is_callable()\
        .with_args('arg1', kw=1).returns(DID_NOT_HANDLE)


class UseThisOne(object):
    func = fudge.Fake().is_callable()\
        .with_args('arg1', kw=1).returns("backend returned me")
