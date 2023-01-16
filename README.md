# PySearch

```python
from pysearch import GoogleSearch, BingSearch
from pprint import pprint

with GoogleSearch() as search:
    search.query = "github"
    search.page = 2
    pprint(search.links)
```
