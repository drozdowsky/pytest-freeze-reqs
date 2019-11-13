pytest freeze reqs
=================
Pytest plugin that tests if requirements are frozen.  
\*\*/req\*.txt and \*\*/req\*.pip are the patterns of path to match.

## ok and not ok lines in requirements.txt
```
Django<2.2  # ok
Django>=1.0  # not ok
requests  # not ok
requests>1.0,<2.3  # ok
```

## example error
```
================================== FAILURES ===================================
_________________ requirement: Django is not frozen properly. _________________
requirement freeze test failed
   improperly frozen requirement: 'Django': [('>=', '1.0')]
   try e.g. Django==1.0
________________ requirement: requests is not frozen properly. ________________
requirement freeze test failed
   improperly frozen requirement: 'requests': []
   try e.g. requests==1.0
========================= 2 failed, 8 passed in 0.35s =========================
```

## usage
```sh
# just add --freeze_reqs arg to pytest
pytest --freeze_reqs

# if you want to run only freeze_reqs tests
pytest -m freeze_reqs --freeze_reqs
```

## pytest.ini configuration
```
# here you can configure paths/files to ignore
# these are checked with contain.
freeze-reqs-ignore-paths=requirement_local.txt
                         requirements/req_dev.txt

# here you can configure paths/files to include
# these are checked with contain.
freeze-reqs-include-paths=requirements/base.txt
                          requirements/development.txt
```
