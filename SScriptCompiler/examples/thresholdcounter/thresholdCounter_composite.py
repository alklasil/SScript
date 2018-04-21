import sys

# SSCript
from src.SComposite import SComposite

# programData
from examples.advanced.thresholdcounter.thresholdCounter import get_programData as thresholdCounter
from examples.simple.logger import get_programData as logger


argv = sys.argv[1:]


def get_compositeData(argv=argv):

    # TODO: rm logger, add requestStingGenerator related programData
    #       (current compositeData was used for testing)

    compositeData = {
        "programData": {
            "thresholdcounter": thresholdCounter(argv),
            "logger": logger()
        },
        "shared": {
            "variableNameValuePairs": [
                ["thresholdcounter", "logger"]
            ],
            "confs": [
                ["thresholdcounter", "logger"]
            ]
        }
    }

    return compositeData


def main(argv=argv):

    composite = SComposite(get_compositeData(argv))

    composite.compile()


if __name__ == "__main__":
    # execute only if run as a script
    main(argv)
