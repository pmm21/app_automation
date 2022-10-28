import re
from bs4 import BeautifulSoup as bts
from lxml import html


class GGSR():

  def bts_get_text(self, tree_element):
    return bts(html.tostring(tree_element), 'html.parser').getText().strip()

  def get_top_nav_data(self, top_nav):
    return [self.bts_get_text(item) for item in top_nav[0].xpath('.//div[@class="hdtb-mitem"]')] if top_nav else []

  def get_result_stats_data(self, result_stats):

    return re.search("[\d+(\,|\.)]+", result_stats[0].text)[0].replace(',','').replace('.','') if result_stats else ''

  def get_relate_search_data(self, relate_search):
    return [self.bts_get_text(item) for item in relate_search[0].xpath('.//a[@class="k8XOCe R0xfCb VCOFK s8bAkb"]')] if relate_search else []

  def get_feature_snipet_data(self, feature_snipet):
    output = dict(())
    if len(feature_snipet)>0:
      main_info = feature_snipet[0].xpath('.//div[@class="yuRUbf"]/a')[0]
      output['title'] = self.bts_get_text(main_info.xpath('.//h3')[0])
      output['link'] = main_info.xpath('./@href')[0]
      if len(feature_snipet[0].xpath('.//table'))>0:
        output['type'] = 'TABLE'
      else:
        output['type'] = 'TEXT'
      return output
    return output

  def get_gg_shoping_data(self, gg_shoping):
    return [{
          'title':self.bts_get_text(item.xpath('.//a[@class="plantl pla-unit-title-link"]')[0]),
          'price':self.bts_get_text(item.xpath('.//div[@class="T4OwTb"]')[0]),
          'link':item.xpath('.//a[@class="plantl pla-unit-title-link"]/@href')[0],
          'source':self.bts_get_text(item.xpath('.//div[@class="LbUacb"]')[0])
      } for item in gg_shoping[0].xpath('.//div[@class="mnr-c pla-unit"]')] if len(gg_shoping)>0 else []

  def get_kg_table_data(self, kg_table):
    if len(kg_table)>0:
      return True
    else:
      return False

  def get_news_table_data(self, news_table):
    output = {
        'item_type':'news_table',
        'data':[]
    }
    for item in news_table.xpath('.//a[@class="WlydOe"]'):
      output['data'].append({
        'link':item.xpath('./@href')[0],
        'source':self.bts_get_text(item.xpath('.//div[@class="CEMjEf NUnG9d"]')[0]),
        'title':self.bts_get_text(item.xpath('.//div[@class="mCBkyc tNxQIb ynAwRc nDgy9d"]')[0])
    })
    return output
  
  def get_video_table_data(self, video_table):
    output = {
        'item_type':'video_table',
        'data':[url for url in video_table.xpath('.//a/@href')]
    }
    return output

  def get_map_table_data(self, map_table):
    output = {
        'item_type':'map_table',
        'data':[]
    }
    for item in map_table.xpath('.//div[@jscontroller="AtSb"]'):
      item_data = {
          'name':self.bts_get_text(item.xpath('.//div[@class="dbg0pd"]')[0]),
          'info':[self.bts_get_text(s_item) for s_item in item.xpath('.//div[@class="rllt__details"]/*')[1:]],
      }
      web_e = item.xpath('.//a[@class="yYlJEf Q7PwXb L48Cpd"]')
      if len(web_e)>0:
        item_data['website'] = web_e[0].xpath('./@href')
      else:
        item_data['website'] = ''
      output['data'].append(item_data)
    return output

  def get_img_table_data(self, img_table):
    return {
        'item_type':'img_table',
        'data':[self.bts_get_text(item) for item in img_table.xpath('.//div[@class="xlY4q VDgVie VIZLse"]')]
    }

  def get_organic_result_info(self, organic_result):
    main_info = organic_result.xpath('.//div[contains(@class, "Z26q7c UK95Uc jGGQ5e")]/div/a')[0]
    output = {
      'item_type':'organic_result',
      'title':self.bts_get_text(main_info.xpath('.//h3')[0]),
      'link':main_info.xpath('./@href')[0],
      'des':self.bts_get_text(organic_result.xpath('.//div[contains(@class,"VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc")]')[0]),
      'review/price':'',
      'faqs':[],
      'Pros_and_cons':[],
      'events':[],
      'sitelinks':[],
      'table':[],
      'img':False,
      'imgs':False
    }
    review = organic_result.xpath('.//div[@class="fG8Fp uo4vr"]')
    if len(review)>0:
      output['review/price'] = self.bts_get_text(review[0])

    faqs = organic_result.xpath('.//div[@class="Okagcf"]')
    if len(faqs)>0:
      for item in faqs[0].xpath('.//g-accordion-expander[@jscontroller="Bnimbd"]'):
        item_data = item.xpath('./*')
        q = self.bts_get_text(item_data[0])
        a = self.bts_get_text(item_data[1])
        output['faqs'].append({'question':q, 'answer':a})

    events = organic_result.xpath('.//div[@class="P1usbc"]')
    if len(events)>0:
      for item in events[0].xpath('.//div[@class="VNLkW"]'):
        time = self.bts_get_text(item.xpath('.//div[@class="i4vd5e"]')[0])
        e_name = self.bts_get_text(item.xpath('.//div[@class="G1Rrjc"]')[0])
        output['events'].append({'time':time, 'e_name':e_name})
    
    sitelinks = organic_result.xpath('.//div[@class="HiHjCd"]')
    if len(sitelinks)>0:
      for item in sitelinks[0].xpath('.//a'):
        a = item.xpath('./@href')
        text = self.bts_get_text(item)
        output['sitelinks'].append({'a':a,'text':text})
    table = organic_result.xpath('.//div[@class="IThcWe"]')
    if len(table)>0:
      for item in table[0].xpath('.//div[@class="YgpRwf"]'):
        output['table'].append([self.bts_get_text(s_item) for s_item in item.xpath('./*')])

    if organic_result.xpath('.//div[@class="LicuJb uhHOwf BYbUcd"]'):
      output['img'] = True
    if organic_result.xpath('.//div[@class="d86Vh KUuaG"]'):
      output['imgs'] = True

    pros_and_cons = organic_result.xpath('.//span[@class="s8CFQb"]')
    if pros_and_cons:
      output['Pros_and_cons'] = [self.bts_get_text(s_item) for s_item in pros_and_cons]
    
    return output

  def get_faq_table_data(self, FAQ_Table):
    if FAQ_Table:
      return self.bts_get_text(FAQ_Table)
    return ''

  def get_twitter_table_data(self, twitter_table):
    output = dict(())
    if len(twitter_table)>0:
      info = twitter_table[0].xpath('.//div[@class="M42dy qkbjle"]')[0]
      output['title']= self.bts_get_text(info.xpath('.//h3')[0]),
      output['link']= info.xpath('.//a/@href')[0],
      output['s_link']= [item.xpath('.//a/@href')[0] for item in twitter_table.xpath('.//div[@jsname="O2za3e"]')]
    return output

  map_table__class = ['ixfGmd','N60sec']
  news_table__class = ['aUSklf']
  video_table__class = ['o0igqc']
  organic_results__class = ['GLI8Bc UK95Uc', 'kvH3mc BToiNc UK95Uc']

  def check_center_col_element_data(self, element):
    id_ = element.get('id')
    class_ = element.get('class')
    if element.tag == 'div':
      if class_ in self.map_table__class:
        return self.get_map_table_data(element)
      elif class_ in self.video_table__class:
        return self.get_video_table_data(element)
      elif class_ in self.organic_results__class:
        return self.get_organic_result_info(element)
    if element.tag == 'g-section-with-header':
      if element.xpath('.//div[@id="iur"]'):
        return self.get_img_table_data(element)
      else:
        return self.get_news_table_data(element)
    return 0

  def get_center_col_data(self, center_col):
    data = []
    def get_data_with_structure(data, element):
      e_data = self.check_center_col_element_data(element)
      if e_data == 0:
        childs = element.xpath('./*')
        if childs:
          for child in childs:
            data = get_data_with_structure(data, child)
      else:
        data.append(e_data)
      return data
    return get_data_with_structure(data, center_col[0]) if center_col else []

  def get_upon_map(self, tree):
    M8OgIe =tree.xpath('.//div[@class="M8OgIe"]')
    if M8OgIe:
      return self.get_map_table_data(M8OgIe[0])
    else:
      return {
          'item_type':'map_table',
          'data':[]
        }

  def __init__(self, tree):
    self.top_nav = self.get_top_nav_data(tree.xpath('.//div[@id="hdtb-msb"]'))
    self.result_stats = self.get_result_stats_data(tree.xpath('.//div[@id="result-stats"]'))
    self.gg_shoping = self.get_gg_shoping_data(tree.xpath('.//div[contains(@class, "cu-container")]'))
    self.twitter_table = self.get_twitter_table_data(tree.xpath('.//div[@class="g eejeod"]'))
    self.FAQ_Table = self.get_faq_table_data(tree.xpath('.//div[@class="AuVD cUnQKe"]'))
    self.feature_snipet = self.get_feature_snipet_data(tree.xpath('.//block-component'))
    self.kg_table = self.get_kg_table_data(tree.xpath('.//div[@class="liYKde g VjDLd"]'))
    self.relate_search = self.get_relate_search_data(tree.xpath('.//div[@class="oIk2Cb"]'))
    self.top_map = self.get_upon_map(tree)
    self.center_col = self.get_center_col_data(tree.xpath('.//div[@id="center_col"]'))
    self.rhs = tree.xpath('.//div[@id="rhs"]')
    if self.rhs:
      self.rhs_gg_shoping = self.get_gg_shoping_data(self.rhs[0].xpath('.//div[contains(@class, "cu-container")]'))
    else:
      self.rhs_gg_shoping = []
    
    self.top_ads = tree.xpath('.//div[@class="qGXjvb"]')
    self.bot_ads = tree.xpath('.//div[@id="bottomads"]')

    self.output_data = {
        'top_nav':self.top_nav,
        'result_stats':self.result_stats,
        'gg_shoping': self.gg_shoping,
        'twitter_table': self.twitter_table,
        'FAQ_Table': self.FAQ_Table,
        'feature_snipet': self.feature_snipet,
        'kg_table': self.kg_table,
        'top_map': self.top_map,
        'center_col': self.center_col,
        'relate_search': self.relate_search
    }