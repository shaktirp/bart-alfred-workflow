import sys
import requests

from workflow import Workflow

def main(wf):
    srcStation = wf.args[0]
    url = "http://api.bart.gov/api/etd.aspx?cmd=etd&orig=" + srcStation + "&key=MW9S-E7SL-26DU-VV8V&json=y"
    bartDoc = 'https://api.bart.gov/docs/overview/abbrev.aspx'

    r = requests.get(url)

    if r.status_code == 200:
        try:
            for dest in r.json()['root']['station'][0]['etd']:
                estimateString = ''
                for estimate in dest['estimate']:
                    estimateString += estimate['minutes'] + ' '
                wf.add_item(dest['destination'], estimateString)
        except Exception as e:
            wf.add_item('Invalid argument. For Example: powl | civc', bartDoc, copytext=bartDoc)
    else:
        wf.add_item('Service is down')

    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))
