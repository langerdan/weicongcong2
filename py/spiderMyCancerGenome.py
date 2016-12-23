#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROGRAM : spiderMyCancerGenome
# AUTHOR  : codeunsolved@gmail.com
# CREATED : November 11 2016
# VERSION : v0.0.1a

import os
import re
import time
import base64
import requests
import argparse

from bs4 import BeautifulSoup
from tornado import httpclient, gen, ioloop, queues

from config import mysql_config
from lib.base import print_colors
from lib.database_connector import MysqlConnector


def update_disease():
    def get_genes():
        r_gene = requests.get('https://www.mycancergenome.org/api/sp-genome/get-genes-for-disease/?disease=%s' % option['value'], headers=headers, cookies=cookies) # seems only need headers
        if r_gene.status_code == 200:
            for key in r_gene.json():
                import_disease([str(option.string), int(option['value']), str(key), r_gene.json()[key]])
        else:
            print print_colors("[ERROR] CODE: %d - failed to get genes for disease: %s" % (r_gene.status_code , option.string),'red')
            get_genes()

    r = requests.get('https://www.mycancergenome.org/')
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')
        select_disease = soup.find('select', attrs={'id': 'DiseaseDropdown'})
        for option in select_disease.find_all('option', attrs={'value': re.compile('\d+')}):
            get_genes()
    else:
        print print_colors("[ERROR] CODE: %d - failed to get disease at 'https://www.mycancergenome.org/'" % r.status_code,'red')
        update_disease()


def import_disease(data):
    insert_g = ("INSERT INTO MyCancerGenome_Disease "
                "(disease, disease_value, gene, gene_value) "
                "VALUES (%s, %s, %s, %s)")
    if m_con.query("SELECT id FROM MyCancerGenome_Disease "
                   "WHERE disease=%s AND gene=%s ",
                   data[::2]).rowcount == 1:
        print print_colors("=>ignore %s" % data, 'yellow')
    else:
        print print_colors("=>insert %s" % data, 'green')
        m_con.insert(insert_g, data)


def update_variant():
    def get_variant():
        r = requests.get('https://www.mycancergenome.org/content/disease/%s' % re.sub(' ', '-', d.lower()))
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            variant_list = soup.select("#content-navigation div:nth-of-type(1)>ul li.menu_li a")
            for v in variant_list:
                gene = re.match('(\S+)', str(v.string)).group(1)
                variant_form = re.match('\S+\s+(\S+)', str(v.string)).group(1)
                import_variant([d, gene, variant_form, str(v.string), str(v['href'])])
        else:
            print print_colors("[ERROR] CODE: %d - failed to get variant for disease: %s" % (r.status_code , d),'red')
            get_variant()

    disease = set()
    cursor = m_con.query("SELECT disease FROM MyCancerGenome_Disease ")
    for row in cursor: # return a set() with unicode!!!
        if row[0] not in disease:
            disease.add(str(row[0]))

    for d in disease:
        get_variant()


def import_variant(data):
    insert_g = ("INSERT INTO MyCancerGenome_Variant "
                "(disease, gene, variant_form, variant, variant_url) "
                "VALUES (%s, %s, %s, %s, %s)")
    if m_con.query("SELECT id FROM MyCancerGenome_Variant "
                   "WHERE disease=%s AND variant=%s ",
                   [data[0], data[3]]).rowcount == 1:
        print print_colors("=>ignore %s" % data, 'yellow')
    else:
        print print_colors("=>insert %s" % data, 'green')
        m_con.insert(insert_g, data)


def get_variant_url():
    return [str(x[0]) for x in m_con.query("SELECT variant_url FROM MyCancerGenome_Variant ").fetchall()]


def import_variant_details(data):
    if m_con.query("SELECT id FROM MyCancerGenome_Variant "
                   "WHERE last_update=%s AND variant_url=%s ",
                   data[-2:]).rowcount == 1:
        print print_colors("=>ignore %s" % data[2], 'yellow')
    else:
        print print_colors("=>update %s" % data[2], 'green')
        m_con.query("UPDATE MyCancerGenome_Variant "
                    "SET variant_table=%s, variant_details=%s, last_update=%s "
                    "WHERE variant_url=%s ", data)
        m_con.cnx.commit()


def check_variant_details(u):
    return m_con.query("SELECT last_update FROM MyCancerGenome_Variant "
                       "WHERE variant_url=%s ", [u]).fetchone()[0]


@gen.coroutine
def get(url):
    try:
        resp = yield httpclient.AsyncHTTPClient().fetch(url)
    except Exception as e:
        print print_colors('Exception: %s %s' % (e, url), 'red')
        raise gen.Return([])
    else:
        raise gen.Return(resp)


@gen.coroutine
def main():
    concurrency = args.concurrency

    unfetched = get_variant_url()

    start = time.time()
    q_get = queues.Queue()
    fetching, fetched = set(), set()

    @gen.coroutine
    def fetch():
        url = yield q_get.get()
        try:
            print print_colors('<No.%d/%d - %s>' % (unfetched.index(url) + 1, len(unfetched), url))
            if url in fetching:
                print print_colors('fetching!', 'red')
            else:
                fetching.add(url)
                if not args.update:
                    if check_variant_details(url):
                        print print_colors('Pass!', 'grey')
                        fetched.add(url)
                    else:
                        response = yield get(url)
                        if response:
                            fetched.add(url)
                            soup = BeautifulSoup(response.body, "html.parser")
                            variant_details = str(soup.select("#section-content-container div[class='section-content active']")[0])
                            variant_table = str(soup.select("#section-content-container div[class='section-content active'] table")[0])
                            last_update = str(soup.select("#section-content-container div[class='section-content active'] p")[-1].text)
                            import_variant_details([variant_table, variant_details, last_update, url])
                        else:
                            print print_colors('FAILED! put into queue[%s]' % url, 'red')
                            fetching.remove(url)
                            q_get.put(url)
                else:
                    response = yield get(url)
                    if response:
                        fetched.add(url)
                        soup = BeautifulSoup(response.body, "html.parser")
                        variant_details = str(soup.select("#section-content-container div[class='section-content active']")[0])
                        variant_table = str(soup.select("#section-content-container div[class='section-content active'] table")[0])
                        last_update = str(soup.select("#section-content-container div[class='section-content active'] p")[-1].text)
                        import_variant_details([variant_table, variant_details, last_update, url])
                    else:
                        print print_colors('FAILED! put into queue[%s]' % url, 'red')
                        fetching.remove(url)
                        q_get.put(url)
        finally:
            q_get.task_done()

    @gen.coroutine
    def worker():
        while True:
            yield fetch()

    [q_get.put(x) for x in unfetched]

    for _ in range(concurrency):
        worker()

    yield q_get.join()
    assert fetching == fetched
    print('==================\nDone in %d seconds' % (time.time() - start))

if __name__ == '__main__':
    # parse args
    parser = argparse.ArgumentParser(prog='spider_mycancergenome', description="catch gene info from My Cancer Genome")
    parser.add_argument('-ud', '--update_disease', action='store_true', help='update Disease - Gene list')
    parser.add_argument('-uv', '--update_variant', action='store_true', help='update Disease - Variant list')
    parser.add_argument('-u', '--update', action='store_true', help='update MyCancerGenome')
    parser.add_argument('-c', '--concurrency', metavar='N', type=int, default=1, help='set concurrency for crawling variant details')

    args = parser.parse_args()

    gene_list = ['AKT1', 'ALK', 'BRAF', 'BRCA1', 'BRCA2', 'CTNNB1', 'DDR2', 'EGFR', 'ESR1', 'FGFR1', 'FGFR2', 'FGFR3', 
                 'GNA11', 'GNAQ', 'HER2', 'HRAS', 'IDH1', 'IDH2', 'KIT', 'KRAS', 'MAP2K1', 'MET', 'NF1', 'NRAS', 'NTRK1', 
                 'PDGFRA', 'PIK3CA', 'PTEN', 'RET', 'RICTOR', 'ROS1', 'SMAD4', 'SMO', 'TP53', 'TSC1']

    headers = {
        'urlept': 'application/json, text/javascript, */*; q=0.01',
        'urlept-Encoding': 'gzip, deflate, sdch, br',
        'urlept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Host': 'www.mycancergenome.org',
        'DNT': '1',
        'Pragma': 'no-cache',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
        'Referer': 'https://www.mycancergenome.org/',
    }

    cookies = {
        '__utma': '58548534.227184441.1478824675.1478831916.1478844130.3',
        '__utmb': '58548534.10.9.1478844309665',
        '__utmc': '58548534',
        '__utmt': '1',
        '__utmz': '58548534.1478824675.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
        'mcg_local_data': 'GLeNdEZAT6EiZDGC0uYwmi1CATEs7bqDSgUcgAM2MtYtsKjTOiGA2sgItZsODUUbXXB8lQX%2BT7VGbAZKDmcHJmHpHPE%2BE4FZuK54SjL0ruUtpHuSxUfMbO45telAA912629YvEC3aO4YMxrCgtzuu47QqwWMQ622ZscMmxUdMzfqbzZsLPfOICuyRaioCAu3%2FUKqWRYRbsl%2FzzylmUlzq7iyyRkW0nzZaoZdV0%2B%2FvuSvj1rFT89avjRnV4uvZRJAmIwY0iv7RPD6FoOkRzc85NqC%2BZb4PVfiJE1YbRXtnJati4GhT1T0TOGCsUjUyJqa%2BA3%2ByIAjcrwRM8%2F9hQAqqVr%2BDCQfO380s2CtGDIEad0VB4nRlmwRpLHeUc%2F%2B%2F%2Fe9XxTlbwDItxd0HTgulX%2FYi33VP1PphqmU%2BF2Q1DZ6rg0sJi8%2BuxOf9N%2FtOWJt9zeZezmJF9ejzzPe8HwUcRoq0lPMl%2FAFdluK8foSavlzQNg%2FqNzvCt%2BZHGsWZZrFb2RT2e0d12b989a87c895d42c5d7d0dfe9987a20b7d5'
    }

    m_con = MysqlConnector(mysql_config, 'KnowledgeDB')
    if args.update_disease:
        update_disease()
    if args.update_variant:
        update_variant()
    ioloop.IOLoop.current().run_sync(main)
    m_con.done()
