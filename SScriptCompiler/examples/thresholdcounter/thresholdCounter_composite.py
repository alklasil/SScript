import sys

# SSCript
from src.SComposite import SComposite

# programData
from examples.thresholdcounter.thresholdCounter import get_programData as thresholdCounter
from examples.logger import get_programData as logger


argv = sys.argv[1:]


def get_compositeData(argv=argv):

    # TODO: rm logger, add requestStingGenerator related programData
    #       (current compositeData was used for testing)

    compositeData = {
        "thresholdcounter": {
            'programData': thresholdCounter(argv)
        },
        "logger": {
            'programData': logger(),
            'variableNameValuePairs': 'thresholdcounter',
            'confs': 'thresholdcounter'
        }
    }

    return compositeData


def main(argv=argv):

    composite = SComposite(get_compositeData(argv))

    composite.compile()


if __name__ == "__main__":
    # execute only if run as a script
    main(argv)
