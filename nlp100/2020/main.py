from __future__ import annotations

import re
from typing import Generator, Iterable

mediawiki_text = """
| languages2                = {{hlist
 <!--Anglo-->
  | [[Scots language|Scots]]
  | [[Ulster Scots dialects|Ulster Scots]]
 <!--Brittonic-->
  | [[Welsh language|Welsh]]
  | [[Cornish language|Cornish]]
 <!--Goidelic-->
  | [[Scottish Gaelic]]<!--Keep "Scottish Gaelic"; people will find "Gaelic" confusing, as the Irish language is also commonly called "Gaelic"-->
  | [[Irish language|Irish]]
  }}
| ethnic_groups                = {{ublist |item_style=white-space:nowrap;
  | 87.1% [[White British|White]]<ref group=note>"This category could include Polish responses from the country specific question for Scotland which would have been outputted to ‘Other White’ and then included under ‘White’ for UK ... ‘White Africans’ may also have been recorded under ‘Other White’ and then included under ‘White’ for UK."</ref>
  | 7.0% [[British Asian|Asian]]
  | 3.0% [[Black British|Black]]
  | 2.0% [[Mixed (United Kingdom ethnicity category)|Mixed]]
  | 0.9% others
  }}
"""



def main():
    for block in Block.from_stream(mediawiki_text.split("\n")):
        print(block)


if __name__ == "__main__":
    main()
