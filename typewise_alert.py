from alerts import ControllerAlert, EmailAlert
from config_parser import ConfigProvider
from bisect import bisect_right


def serialize_limits_to_dict():
    config = ConfigProvider("config.ini")
    categories = config.get_categories()
    breach_types = ("TOO_LOW", "NORMAL", "TOO_HIGH")
    return {
        category: {
            "breach_limits": [
                config.get_value(field, float, category) for field in ["MIN", "MAX"]
            ],
            "breach_types": breach_types,
        }
        for category in categories
    }


def classify_temperature_breach(coolingType, temperatureInC):
    cooling_config = serialize_limits_to_dict()[coolingType]
    return cooling_config["breach_types"][
        bisect_right(cooling_config["breach_limits"], temperatureInC)
    ]


def check_and_alert(alertTarget, batteryChar, temperatureInC):
    breachType = classify_temperature_breach(batteryChar["coolingType"], temperatureInC)
    return alertTarget.send_alert(breachType)
