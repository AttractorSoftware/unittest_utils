from time import sleep
from unittest import TestCase

from commons.types import Object
from lettuce_webdriver.util import assert_true
from nose.tools import assert_equal
from unittest_utils import repeat_until_timeout, TimeoutError, TIMEOUT_OCCURRED

TIMEOUT_SECONDS = 1
SLEEP_INTERVAL = 0.1
FIRST_CALL = 1
CALL_WITH_TIMEOUT = TIMEOUT_SECONDS / SLEEP_INTERVAL
LAST_CALL_BEFORE_TIMEOUT = CALL_WITH_TIMEOUT - 1
ASSERTION_ERROR = "Assertion Error"
PING = "ping"


class TestRepeatUntilTimeoutDecorator(TestCase):
    def setUp(self):
        self.stub = Stub()

    def test_raise_timeout(self):
        self.stub.will_return_after_first_call()
        self.stub.will_execute_one_call_longer_than_timeout()
        try:
            self.stub.decodated_method(PING)
            assert_true(False, "should raise Timeout Error")
        except TimeoutError as e:
            assert_equal(TIMEOUT_OCCURRED, e.__str__())
        assert_equal(FIRST_CALL, self.stub.calls_counter, "Should call only %s time(s)" % FIRST_CALL)

    def test_raise_assertion(self):
        self.stub.will_return_after_timeout()
        try:
            self.stub.decodated_method(PING)
            assert_true(False, "should raise Assertion Error")
        except AssertionError as e:
            assert_equal(ASSERTION_ERROR, e.__str__())
        assert_equal(CALL_WITH_TIMEOUT, self.stub.calls_counter, "Should call only %s time(s)" % CALL_WITH_TIMEOUT)

    def test_return_value_before_timeout(self):
        self.stub.will_return_before_timeout()
        pong = self.stub.decodated_method(PING)
        assert_equal(PING, pong)
        assert_equal(LAST_CALL_BEFORE_TIMEOUT, self.stub.calls_counter, "Should call only %s time(s)" % LAST_CALL_BEFORE_TIMEOUT)

    def test_return_value_after_first_call(self):
        self.stub.will_return_after_first_call()
        pong = self.stub.decodated_method(PING)
        assert_equal(PING, pong)
        assert_equal(FIRST_CALL, self.stub.calls_counter, "Should call only %s time(s)" % FIRST_CALL)


class Stub(Object):
    sleep_interval = SLEEP_INTERVAL
    calls_counter = 0
    trigger_return_after_call_number = 0

    @repeat_until_timeout(TIMEOUT_SECONDS)
    def decodated_method(self, ping):
        self.increment_calls_counter()
        sleep(self.sleep_interval)
        if self.is_time_to_return():
            print "return"
            return ping
        print "raise"
        raise AssertionError(ASSERTION_ERROR)

    def will_return_after_first_call(self):
        self.set_calls_limit(1)

    def will_return_after_timeout(self):
        self.set_calls_limit(CALL_WITH_TIMEOUT + 1)

    def will_return_before_timeout(self):
        self.set_calls_limit(CALL_WITH_TIMEOUT - 1)

    def will_execute_one_call_longer_than_timeout(self):
        self.sleep_interval = TIMEOUT_SECONDS + 1

    def set_calls_limit(self, call_number):
        self.trigger_return_after_call_number = call_number

    def increment_calls_counter(self):
        self.calls_counter += 1

    def is_time_to_return(self):
        return self.calls_counter >= self.trigger_return_after_call_number

