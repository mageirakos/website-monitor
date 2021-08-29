import requests
# import json



def request(url, headers):
    """
    Return the response from the url with the information saved in
    a python dictionary.

    :param url : the url upon which the request is made
    :out r_dict: json response in python dict format
    """
    r = requests.get(url, headers=headers)
    status_code = r.status_code
    c_type = r.headers['content-type']
    return status_code