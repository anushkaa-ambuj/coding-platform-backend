import http.client

conn = http.client.HTTPSConnection("judge0-ce.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "2835b604c6msh0217cec4fcd6b58p1fc7f0jsnb44766040dff",
    'x-rapidapi-host': "judge0-ce.p.rapidapi.com"
}

conn.request("GET", "/submissions/2e979232-92fd-4012-97cf-3e9177257d10?base64_encoded=true&fields=*", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))