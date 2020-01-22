# Last Updated | 2019-12-30
# Python Modules
import os
from typing import List

# Third Party Modules
import pandas as pd
from datetime import datetime

# Local Modules
from digital_manuscript import BnF
from recipe import Recipe

versions = ['tc', 'tcn', 'tl']
properties = ['animal', 'body_part', 'currency', 'definition', 'environment', 'material', 'medical', 'measurement',
              'music', 'plant', 'place', 'personal_name', 'profession', 'sensory', 'tool', 'time', 'weapon']
m_path = f'{os.getcwd()}/../m-k-manuscript-data'
test_path = f'{os.getcwd()}/test'

def update_metadata(manuscript: BnF) -> None:
  """
  Update /m-k-manuscript-data/metadata/entry_metadata.csv with the current manuscript. Create a Pandas DataFrame
  indexed by entry. Create data columns, and remove the column that contains the entry objects. Save File.

  Input:
    manuscript -- Python object of the manuscript defined in digital_manuscript.py
  Output:
    None
  """
  df = pd.DataFrame(columns=['entry'], data=manuscript.entries.values())
  df['folio'] = df.entry.apply(lambda x: x.folio)
  df['folio_display'] = df.entry.apply(lambda x: x.folio.lstrip('0'))
  df['div_id'] = df.entry.apply(lambda x: x.identity)
  df['categories'] = df.entry.apply(lambda x: (', '.join(x.categories)))
  df['heading_tc'] = df.entry.apply(lambda x: x.title['tc'])
  df['heading_tcn'] = df.entry.apply(lambda x: x.title['tcn'])
  df['heading_tl'] = df.entry.apply(lambda x: x.title['tl'])
  df['margins'] = df.entry.apply(lambda x: len(x.margins))
  df['del_tags'] = df.entry.apply(lambda x: '; '.join(x.del_tags))
  df['figures'] = df.entry.apply(lambda x: 'unknown')
  for prop in properties:
    df[prop] = df.entry.apply(lambda x: '; '.join(x.get_prop(prop=prop, version='tc')))
  df.drop(columns=['entry'], inplace=True)
  # df.to_csv(f'{m_path}/metadata/entry_metadata.csv', index=False)
  df.to_csv(f'{test_path}/entry_metadata.csv', index=False)

def update_ms(manuscript: BnF) -> None:
  """
  Update /m-k-manuscript-data/ms-txt/ with the current manuscript from /ms-xml/. For each version and for each
  entry in the manuscript, open the 

  Input:
    manuscript -- Python object of the manuscript defined in digital_manuscript.py
  Output:
    None
  """
  for version in versions:
    current_folio = ''
    for identity, entry in manuscript.entries.items():
      if identity:
        folio, num = tuple(identity.split('_'))
        num = int(num)

        filename = f'{m_path}/ms-txt/{version}_{folio}_preTEI.txt'
        f = open(filename, 'r')
        text = f.read()
        # print(entry.identity, filename, text, '\n\n')
        f.close()

        # f = open(filename, 'w')
        # f.write(entry.text(version, xml=False))
        # f.close()

def update_all_folios(manuscript: BnF) -> None:
  """
  Update /m-k-manuscript-data/allFolios/ with the current manuscript from /ms-xml/. 

  Input:
    manuscript -- Python object of the manuscript defined in digital_manuscript.py
  Output:
    None
  """
  for b in [True, False]:
    for version in versions:
      text = ''
      folder = 'xml' if b else 'txt'

      for identity, entry in manuscript.entries.items():
        new_text = entry.text(version, xml=b)
        text = f'{text}\n\n{new_text}' if text else new_text

      # f = open(f'{m_path}/allFolios/{folder}/all_{version}.{folder}', 'w')
      f = open(f'{test_path}/{folder}/all_{version}.{folder}', 'w')
      f.write(text)
      f.close()

def update_time():
  """ Extract timestamp at the top of this file and update it. """
  # Initialize date to write and container for the text
  now_str = str(datetime.now()).split(' ')[0]
  lines = []

  # open file, extract text, and modify
  with open('./update.py', 'r') as f:
    lines = f.read().split('\n')
    lines[0] = f'# Last Updated | {now_str}'
  
  # write modified text
  f = open('./update.py', 'w')
  f.write('\n'.join(lines))
  f.close

def update():
  manuscript = BnF()

  update_metadata(manuscript)
  print('updated metadata')

  # update_ms not yet functional
  # update_ms(manuscript)
  # print('updated /ms/')

  update_all_folios(manuscript)
  print('updated /allFolios/')
  
  update_time()

update()