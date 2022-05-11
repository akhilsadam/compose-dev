import pytest, requests as rqs

# assuming app is running - please do that first! I have implemented this inside the app with the automatic documentation so simply checking output will work!
# only these tests since there was no minimum test requirement!

resp = rqs.get('http://localhost:5026/api/save')
resps = str(resp.content.decode('utf-8')).split('###')
resps2 = ["" if '/piece/CREATE' in r else r for r in resps] # workaround for expected BAD request
resps3 = [r for r in resps if '/piece/CREATE' in r] # workaround for expected BAD request

def test_404():
    assert all('404 Not Found' not in r for r in resps)

def test_400():
    assert all('400 Bad Request' not in r for r in resps2)
    assert all('400 Bad Request' in r for r in resps3)

def test_API_Call():
    assert all('API CALL FAILED' not in r for r in resps)

def test_Exception():
    assert all('Exception' not in r for r in resps2)
    assert all('Exception' in r for r in resps3)

def test_ENDPOINT():
    assert resps.count('ENDPOINT') == resps.count('Description')
    assert resps.count('ENDPOINT') == resps.count('Parameters')
    assert resps.count('ENDPOINT') == resps.count('Responses')
    assert resps.count('ENDPOINT') == resps.count('curl')