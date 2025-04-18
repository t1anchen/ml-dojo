from __future__ import annotations

import re
from pprint import pprint
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


class Block:
    def __init__(self, name: str, lines: list[str], block_type: str):
        self.content = lines
        self.block_type = block_type
        self.name = name

    def __str__(self):
        return str(self.to_dict())

    def to_dict(self) -> dict[str, str]:
        return {
            "content": "\n".join(self.content),
            "block_type": self.block_type,
            "name": self.name,
        }

    @staticmethod
    def from_stream(stream: Iterable[str]) -> Generator[Block, None, None]:
        collected: list[str] = []
        name = "Unknown"
        block_type = "Unknown"
        block_start, block_end = "{{,}}".split(",")
        is_selected = False
        block_name_pat = re.compile(r"\|\s*(\w+)\s*=\s*\{\{(\w+)\s*.*")
        for line in stream:
            if block_start in line and block_end in line:
                block_pos_start, block_pos_end = line.find(
                    block_start
                ), line.find(block_end)
                collected.append(line[block_pos_start + 2 : block_pos_end])
                is_selected = False
                if matched := block_name_pat.match(line):
                    name = matched.group(1)
                    block_type = matched.group(2)
            elif block_start in line:
                block_pos_start = line.find(block_start)
                collected.append(line[block_pos_start + 2 :])
                is_selected = True
            elif block_end in line:
                block_pos_end = line.find(block_end)
                collected.append(line[:block_pos_end])
                yield Block(name, collected, block_type)
                collected.clear()
                is_selected = False
            else:
                if is_selected:
                    collected.append(line)


def main():
    for block in Block.from_stream(mediawiki_text.split("\n")):
        pprint(block)


if __name__ == "__main__":
    main()
