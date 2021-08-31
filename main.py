# https://playwright.dev/python/docs/intro/
# pip install playwright
# Skip browser downloads: https://playwright.bootcss.com/python/docs/installation#skip-browser-downloads
# set PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1
# python -m playwright install
from playwright.sync_api import sync_playwright
# https://matplotlib.org/stable/index.html
# pip install -U matplotlib
import matplotlib.pyplot as plt

import os
import sys
import xml.etree.ElementTree as ET
import math
import operator
import csv
import argparse


# ----------------------------------------------------------------------------------------------------------------------------------

def VisImportanceByWeight(importance_links, weight_links):
    fig, ax = plt.subplots()
    ax.scatter(weight_links, importance_links)
    ax.invert_xaxis()
    plt.show()

# ----------------------------------------------------------------------------------------------------------------------------------

def VisTypesLinks(group_type_link, group_links):
    explode = [0.05] * len(group_type_link)
    index, value = max(enumerate(group_links), key=operator.itemgetter(1))
    explode[index] = 0.1

    plt.pie(group_links, explode=explode, labels=group_type_link, autopct='%02.02f%%', shadow=True)
    plt.axis('equal')
    plt.show()

# ----------------------------------------------------------------------------------------------------------------------------------

def VisRelationLinks(group_relation_links):
    plt.pie(group_relation_links, explode=[0.1, 0.1], labels=['INTERNAL', 'EXTERNAL'], autopct='%02.02f%%', shadow=True)
    plt.axis('equal')
    plt.show()

# ----------------------------------------------------------------------------------------------------------------------------------

def LinkAnalysis():
    importance_weight_links = []
    group_link = {}
    count_external_link = 0
    count_internal_link = 0

    xmlRoot = ET.parse('WebPageSegmentation.xml').getroot()

    for xmlLink in xmlRoot.findall('.//link'):
        if xmlLink.attrib['Adr'] == '':
            continue

        if xmlLink.attrib['External'] == 'true':
            count_external_link += 1
            continue

        count_internal_link += 1

        xmlparent = xmlRoot.find('.//*[@ID="' + xmlLink.attrib['ID'] + '"]...')
        xmlgrandparent = xmlRoot.find('.//*[@ID="' + xmlparent.attrib['ID'] + '"]...')
        importance = float(xmlgrandparent.attrib['importance'])
        internal_id = xmlgrandparent.attrib['internal_id']

        if not internal_id in group_link:
            group_link[internal_id] = 0
        group_link[internal_id] += 1

        if math.isnan(importance):
            importance = 0
        weight = float(xmlLink.attrib['Weight'])
        importance_weight_links.append({'Importance': int(importance), 'Weight': weight, 'Link': xmlLink.attrib['Adr']})

    VisRelationLinks([count_internal_link, count_external_link])

    group_type_link = []
    group_values_link = []
    for key,val in group_link.items():
        group_type_link.append(key)
        group_values_link.append(val)
    VisTypesLinks(group_type_link, group_values_link)

    VisImportanceByWeight([d['Importance'] for d in importance_weight_links], [d['Weight'] for d in importance_weight_links])

    #importance_links.sort(key=operator.itemgetter('Importance'), reverse=True)
    with open('importance_weight_links.csv', 'w', encoding='utf-8', newline='') as outcsv:
        writer = csv.DictWriter(outcsv, fieldnames=["Importance", "Weight", "Link"])
        writer.writeheader()
        writer.writerows(importance_weight_links)

# ----------------------------------------------------------------------------------------------------------------------------------

def WebPageSegmentation():
    xmlRoot = ET.parse('WebPageSegmentation.xml').getroot()
    for block in xmlRoot.iter('Block'):
        if 'importance' in block.attrib:
            print(
                f"=> Block Ref: {block.attrib['Ref']} Importance: {block.attrib['importance']}")
        else:
            continue

        # Links
        childLinks = block.find('Links')
        if childLinks is not None and len(childLinks.attrib['IDList']) > 0:
            print(f'-> Link: {len(childLinks)}')
            for childLink in childLinks:
                print(
                    f"[{childLink.attrib['Name'].strip()}] -> {childLink.attrib['Adr']}")

        # Images
        childImgs = block.find('Imgs')
        if childImgs is not None and len(childImgs.attrib['IDList']) > 0:
            print(f'-> Image: {len(childImgs)}')

        # Texts
        childTexts = block.find('Txts')
        if childTexts is not None and len(childTexts.attrib['Txt'].strip()) > 0:
            print('-> Text')
            print(f"[{childTexts.attrib['Txt'].strip()}]")

# ----------------------------------------------------------------------------------------------------------------------------------

def Playwright(site_url):
    # https://playwright.dev/python/docs/api/class-playwright/
    pw = sync_playwright().start()
    browser = pw.chromium.launch(headless=False, executable_path="C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")  # , slow_mo=50)

    page = browser.new_page()
    response = page.goto(site_url)

    # https://cdnjs.com/
    page.add_script_tag(url='https://cdnjs.cloudflare.com/ajax/libs/jquery/3.4.1/jquery.min.js')
    page.add_script_tag(path=os.path.join('www', 'bomlib.js'))
    page.add_script_tag(path=os.path.join('www', 'polyk.js'))
    page.add_script_tag(path=os.path.join('www', 'md5.js'))

    bomversion = page.evaluate("""() => { return bomversion; } """)
    pac = 6
    print('Using BoM algorithm v{} pAC={}'.format(bomversion, pac))

    auxr = page.evaluate("""([responseHeaders, pac]) => {
        /**
        * @param {Object} object
        * @param {string} key
        * @return {string||undefined} value || undefined
        */
        window.getKeyCase = function(obj,key) {
            const re = new RegExp(key,"i");
            return Object.keys(obj).reduce((result,key)=>{
                if (!result) {
                    return key.match(re) || undefined
                } else {
                    return result;
                }
            },undefined);
        }

        window.responseHeaders = responseHeaders;
        window.numLinks = 0;
        window.totalLinks = document.getElementsByTagName("a").length;

        return startSegmentation(window, pac, 50, 'vixml');
    }""", [response.headers, pac] )

    with open("WebPageSegmentation.xml", 'w', encoding='utf-8') as text_file:
        print(f"{auxr}", file=text_file)

    browser.close()
    pw.stop()

# ----------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    if sys.version_info.major < 3 or sys.version_info.minor < 7:
        print("[ERROR] Make sure you have Python 3.7+ installed, quitting.\n\n")
        sys.exit(1)
    print("Python {0:s} {1:d}bit on {2:s}\n".format(" ".join(item.strip() for item in sys.version.split("\n")), 64 if sys.maxsize > 0x100000000 else 32, sys.platform))

    parser  = argparse.ArgumentParser(description="LinkContext: Catégorisation des liens par segmentation d’une page HTML.")
    parser.add_argument('-u', '--url', type=str, help='URL de la page a analyser.')
    args = parser.parse_args()
    if not args.url :
        parser.print_help()
        sys.exit(1)

    Playwright(args.url)

    LinkAnalysis()
