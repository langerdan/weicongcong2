#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PROGRAM : spider_mycancergenome
# AUTHOR  : codeunsolved@gmail.com
# CREATED : November 11 2016
# VERSION : v0.0.1a

import os
import re
import time
import requests
import argparse

from tornado import httpclient, gen, ioloop, queues
from bs4 import BeautifulSoup

from base import print_colors
from database_connector import MysqlConnector
from config import mysql_config


def update_disease():
    def get_genes():
        r_gene = requests.get('https://www.mycancergenome.org/api/sp-genome/get-genes-for-disease/?disease=%s' % option['value'], headers=headers, cookies=cookies)
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
        print print_colors("=>ignore", 'yellow')
    else:
        print print_colors("=>insert %s" % data, 'green')
        m_con.insert(insert_g, data)


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
    concurrency = 1

    unfetched = []
    if args.database:
        cursor = m_con.query("SELECT Assembly, RefSeqFTP, SpeciesName FROM bacteria_genomes WHERE Assembly LIKE '%'", '')
        results = [[x_i, x] for x_i, x in enumerate(cursor.fetchall())]
        for result in results:
            if result[1][1] and not result[1][2]:
                unfetched.append([result[0], str(result[1][0])])
    if args.input:
        with open(args.input, 'rb') as acc_file:
            for line_i, line in acc_file:
                unfetched.append(len(unfetched) + line_i, line.strip())

    start = time.time()
    q_get = queues.Queue()
    fetching, fetched = set(), set()

    @gen.coroutine
    def fetch():
        (i, acc) = yield q_get.get()
        try:
            print print_colors('<No.%d/%d - %s>' % (i, len(unfetched), acc))
            if acc in fetching:
                print print_colors('fetching!', 'red')
            else:
                fetching.add(acc)
                response = yield get('https://www.ncbi.nlm.nih.gov/genome/?term=%s' % acc)
                if response:
                    fetched.add(acc)
                    soup = BeautifulSoup(response.body, "html.parser")
                    lineage_span = soup.find('span', class_='GenomeLineage')
                    if lineage_span:
                        lineage = lineage_span.find_all('a')
                        lineage_info = [str(lineage[0].string), str(lineage[2].string), str(lineage[-2].string), acc]
                    else:
                        print print_colors('No items found![%s]' % acc, 'red')
                        lineage_info = ['NO_ITEMS_FOUND', 'NO_ITEMS_FOUND', 'NO_ITEMS_FOUND', acc]
                    if args.database:
                        update_lineage(lineage_info)
                        cursor = m_con.query("SELECT Level FROM bacteria_genomes WHERE Assembly=%s", [acc])
                        lineage_info.append(cursor.fetchone()[0])
                    if args.output:
                        output_dir(args.output, lineage_info)
                else:
                    print print_colors('FAILED! put into queue[%s]' % acc, 'red')
                    fetching.remove(acc)
                    q_get.put(i, acc)
        finally:
            q_get.task_done()

    @gen.coroutine
    def worker():
        while True:
            yield fetch()

    [q_get.put(y) for y in unfetched]

    for _ in range(concurrency):
        worker()

    yield q_get.join()
    assert fetching == fetched
    print('==================\nDone in %d seconds' % (time.time() - start))

if __name__ == '__main__':
    # parse args
    parser = argparse.ArgumentParser(prog='spider_mycancergenome', description="catch gene info from My Cancer Genome")
    parser.add_argument('-u', '--update_disease', action='store_true', help='update Disease - Gene list')

    args = parser.parse_args()

    gene_list = ['AKT1', 'ALK', 'BRAF', 'BRCA1', 'BRCA2', 'CTNNB1', 'DDR2', 'EGFR', 'ESR1', 'FGFR1', 'FGFR2', 'FGFR3', 
                 'GNA11', 'GNAQ', 'HER2', 'HRAS', 'IDH1', 'IDH2', 'KIT', 'KRAS', 'MAP2K1', 'MET', 'NF1', 'NRAS', 'NTRK1', 
                 'PDGFRA', 'PIK3CA', 'PTEN', 'RET', 'RICTOR', 'ROS1', 'SMAD4', 'SMO', 'TP53', 'TSC1']

    headers = {
        'Host': 'www.mycancergenome.org',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
        'DNT': '1',
        'Referer': 'https://www.mycancergenome.org/',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4'
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
    if args.update_disease is not None:
        update_disease()
    ioloop.IOLoop.current().run_sync(main)
    m_con.done()

