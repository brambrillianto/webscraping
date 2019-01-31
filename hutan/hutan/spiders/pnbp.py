# -*- coding: utf-8 -*-
import scrapy


class PnbpSpider(scrapy.Spider):
    name = 'pnbp'
    allowed_domains = ['sipnbp.phpl.menlhk.net:8080']
    api_url = 'http://sipnbp.phpl.menlhk.net:8080/simpnbp/rpt_kab_lalu?p_prov={}&p_kab={}&p_awal=2018&p_akhir=2018'


    def start_requests(self):

        # Navigating the Spider 
        provinsi = [
            'Aceh','Sumatera Utara','Sumatera Barat','Jambi','Sumatera Selatan','Riau','Bengkulu','Lampung','Kepulauan Bangka Belitung','DKI Jakarta',
            'Jawa Barat','Banten','Jawa Tengah','DI Yogyakarta','Jawa Timur','Kalimantan Barat','Kalimantan Tengah','Kalimantan Selatan','Kalimantan Timur','Sulawesi Utara',
            'Gorontalo','Sulawesi Tengah','Sulawesi Tenggara','Sulawesi Selatan','Bali','Nusa Tenggara Barat','Maluku','Papua','Nusa Tenggara Timur','Maluku Utara',
            'Kepulauan Riau','Papua Barat','Sulawesi Barat','Kalimantan Utara',
                ]
        jumlahKab = [23, 15, 19, 11, 17, 12, 10, 15, 7, 6, 27, 8, 35, 5, 38, 14, 14, 13, 10, 15, 6, 13, 17, 24, 9, 10, 11, 29, 22, 10, 7, 13, 6, 5]
        dictjumlahKab = dict(zip(provinsi, jumlahKab))
        
        urls = []
        for kdP in range(1, len(dictjumlahKab)+1):
            for kdK in range(1, dictjumlahKab[provinsi[kdP-1]]+1):
                if len(str(kdP)) == 1:
                    if len(str(kdK)) == 1:
                        url = self.api_url.format('0'+str(kdP), '0'+str(kdK))
                    else:
                        url = self.api_url.format('0'+str(kdP), str(kdK))
                else:
                    if len(str(kdK)) == 1:
                        url = self.api_url.format(str(kdP), '0'+str(kdK))
                    else:
                        url = self.api_url.format(str(kdP), str(kdK))
                urls.append(url)
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):

        jenis_izin = response.xpath('//tr[td[@colspan="11"]]/td[2]/text()').extract()
        item = {} 

        for no_izin, izin in enumerate(jenis_izin):
            wbs = response.xpath('//tr[td[@colspan="11"]][1]/following-sibling::tr[@class="sorot" and count(preceding-sibling::tr[td[text()="Sub Total"]])={}]/td[2]/text()'.format(no_izin)).extract()
            for no_wb, wb in enumerate(wbs):
                item["kabupaten"] = response.xpath('//td[@valign="top"]/p[3]/text()').extract_first()
                item["provinsi"] = response.xpath('//td[@valign="top"]/p[4]/text()').extract_first()
                item["tahun"] = response.xpath('//li[@class="TabbedPanelsTab"]/text()').extract_first()
                item["nama_wajib_bayar"] = wb
                item["DR"] = response.xpath('//tr[td[@colspan="11"]][1]/following-sibling::tr[@class="sorot" and count(preceding-sibling::tr[td[text()="Sub Total"]])={}]/td[3]//text()'.format(no_izin)).extract()[no_wb]
                item["PSDH"] = response.xpath('//tr[td[@colspan="11"]][1]/following-sibling::tr[@class="sorot" and count(preceding-sibling::tr[td[text()="Sub Total"]])={}]/td[4]//text()'.format(no_izin)).extract()[no_wb]   
                yield item

        urls = response.xpath('//a/@onclick').extract()

        for url in urls:
            url = re.search('\(([^)]+)', url).group(1)
            url = url.replace("'", "")
            url = reponse.urljoin(url)
            yield scrpy.Request(url=url, callback=self.parse_details)

    def parse_details(self, response):
        pass