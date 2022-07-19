import unittest
from alerts import ControllerAlert, EmailAlert
from config_parser import ConfigProvider
import typewise_alert


class TypewiseTest(unittest.TestCase):
    def test_classify_temperature_breach_for_passive_cooling_with_breach_type_normal(
        self,
    ):
        self.assertTrue(
            typewise_alert.classify_temperature_breach("PASSIVE_COOLING", 20)
            == "NORMAL"
        )

    def test_classify_temperature_breach_for_passive_cooling_with_breach_type_too_low(
        self,
    ):
        self.assertTrue(
            typewise_alert.classify_temperature_breach("PASSIVE_COOLING", -1)
            == "TOO_LOW"
        )

    def test_classify_temperature_breach_for_passive_cooling_with_breach_type_too_high(
        self,
    ):
        self.assertTrue(
            typewise_alert.classify_temperature_breach("PASSIVE_COOLING", 100)
            == "TOO_HIGH"
        )

    def test_classify_temperature_breach_for_hi_active_cooling_with_breach_type_normal(
        self,
    ):
        self.assertTrue(
            typewise_alert.classify_temperature_breach("HI_ACTIVE_COOLING", 20)
            == "NORMAL"
        )

    def test_classify_temperature_breach_for_hi_active_cooling_with_breach_type_too_low(
        self,
    ):
        self.assertTrue(
            typewise_alert.classify_temperature_breach("HI_ACTIVE_COOLING", -1)
            == "TOO_LOW"
        )

    def test_classify_temperature_breach_for_hi_active_cooling_with_breach_type_too_high(
        self,
    ):
        self.assertTrue(
            typewise_alert.classify_temperature_breach("HI_ACTIVE_COOLING", 46)
            == "TOO_HIGH"
        )

    def test_classify_temperature_breach_for_med_active_cooling_with_breach_type_normal(
        self,
    ):
        self.assertTrue(
            typewise_alert.classify_temperature_breach("MED_ACTIVE_COOLING", 20)
            == "NORMAL"
        )

    def test_classify_temperature_breach_for_med_active_cooling_with_breach_type_too_low(
        self,
    ):
        self.assertTrue(
            typewise_alert.classify_temperature_breach("MED_ACTIVE_COOLING", -1)
            == "TOO_LOW"
        )

    def test_classify_temperature_breach_for_med_active_cooling_with_breach_type_too_high(
        self,
    ):
        self.assertTrue(
            typewise_alert.classify_temperature_breach("MED_ACTIVE_COOLING", 41)
            == "TOO_HIGH"
        )

    def test_email_check_and_alert_for_hi_active_cooling_with_breach_type_too_high(
        self,
    ):
        self.assertTrue(
            typewise_alert.check_and_alert(
                EmailAlert("a.b@c.com"), {"coolingType": "HI_ACTIVE_COOLING"}, 50
            ),
            True,
        )

    def test_controller_check_and_alert_for_med_active_cooling_with_breach_type_too_high(
        self,
    ):
        self.assertTrue(
            typewise_alert.check_and_alert(
                ControllerAlert(0xFEED), {"coolingType": "MED_ACTIVE_COOLING"}, -1
            ),
            True,
        )

class ConfigParserTest(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.config = ConfigProvider("stubs/config.ini")

    def test_get_categories(self):
        assert self.config.get_categories() == ("ONE", "TWO", "THREE")

    def test_get_value(self):
        assert self.config.get_value("some_value", float, "ONE") == 10

    def test_get_value_for_invalid_value(self):
        try:
            self.config.get_value("NO_VALUE", str, "ONE")
        except Exception as e:
            assert isinstance(e, ValueError)

class AlertTest(unittest.TestCase):
    def test_send_to_controller(self):
        assert ControllerAlert(0xFEED).send_to_controller("TOO_HIGH") == True
    
    def test_send_to_email(self):
        assert EmailAlert("a.b@c.com").send_to_email("TOO_LOW") == True
    
    def test_send_to_email_for_normal_type(self):
        assert EmailAlert("a.b@c.com").send_to_email("NORMAL") == False
    
    def test_send_to_controller_for_normal_type(self):
        assert ControllerAlert(0xFEED).send_to_controller("NORMAL") == False
    
unittest.main()
