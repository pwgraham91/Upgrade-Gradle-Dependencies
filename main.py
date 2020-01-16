import json
import re

import requests
from packaging import version


def run():
    with open('build.gradle') as file:
        lines = file.read()
        regex_results = re.findall(
            r"[i|I]mplementation [\"|']([a-zA-Z\.\-\d]+):([a-zA-Z\.\-\d]+):([\d\.\-\w]+)[\"|']",
            lines)

        for dependency in regex_results:
            latest_version = get_latest_version(dependency[0], dependency[1])
            if latest_version:
                current_version = dependency[2]
                should_upgrade = version.parse(latest_version) > version.parse(current_version)
                if should_upgrade:
                    print("{}:{} should upgrade from {} to {}".format(dependency[0], dependency[1], current_version,
                                                                      latest_version))


def get_latest_version(part_1, part_2):
    result = requests.get("https://search.maven.org/solrsearch/select?q={}&start=0&rows=2".format(
        "{}%20AND%20a:{}".format(part_1, part_2)))
    jsonified_result = json.loads(result.text)
    docs = jsonified_result["response"]["docs"]
    if len(docs) > 0:
        return docs[0]["latestVersion"]
    else:
        print("no result for {}:{}".format(part_1, part_2))


if __name__ == "__main__":
    run()
