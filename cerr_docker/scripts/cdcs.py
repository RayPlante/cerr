#!/usr/bin/python3

from pprint import pprint
from os.path import join
from os import listdir
from glob import glob
import sys
import subprocess
import string
import io
import zipfile
import requests
import re
import os
import json
import codecs
from builtins import str
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_all_templates( username='', password='', cert='', url=''):
    """
    get_all_templates: get all templates from a curator

       Parameters:     username        - username on CDCS instance   (Note:  User must have admin privileges)
                       password        - password on CDCS instance
                       cert            - certificate to use for authentication - blank means no security
                       url             - url of CDCS instance
    """

    template_upload_url = '/rest/template-version-manager/global/'
    turl = url + template_upload_url

    if cert == '':
        response = requests.get(turl, verify=False, auth=(username, password))
    else:
        response = requests.get( turl, verify=True, cert=cert, auth=( username, password))
    response_code = response.status_code
    response_content = json.loads(response.text)
    for rec in response_content:
        cur = rec['current']
        print('Title: ' + rec['title'] + ' ID: ' + rec['id'])
        fetch_url = url + '/rest/template/' + cur + '/'
        if cert == '':
            response = requests.get(fetch_url, verify=False, auth=(username, password))
        else:
            response = requests.get(fetch_url, verify=True, cert=cert, auth=(username, password))
        out = response.json()

    response_code = response.status_code
    if response_code == requests.codes.ok:
        print('status: Templates downloaded.')
    else:
        pprint(response_content)
        pprint(out)
        response.raise_for_status()

    print('status: done.')


def get_template( username='', password='', cert='', url='', title='', verbose=False):
    """
    get_template: get a single template

    parameters:     username        - username on CDCS instance   (Note:  User must have admin privileges)
                    password        - password on CDCS instance
                    cert            - certificate to use for authentication - blank means no security
                    url             - url of CDCS instance
                    title           - Title of template to get
    """

    template_upload_url = '/rest/template-version-manager/global/'
    turl = url + template_upload_url
    fetch_url = ''

    if verbose: print('status: Getting list of Templates...')
    if cert == '':
        response = requests.get(turl, verify=False, auth=(username, password))
    else:
        response = requests.get( turl, verify=True, cert=cert, auth=(username, password))
    response_code = response.status_code
    if verbose: print('Code:' + str(response_code) + ' - ' + str(requests.status_codes._codes[response_code]))
    response_content = json.loads(response.text)
    for rec in response_content:
        if verbose: print(rec['title'])
        if title == rec['title']:
            cur = rec['current']
            fetch_url = url + '/rest/template/' + cur + '/'
    if fetch_url == '':
        response.raise_for_status()
        raise Exception('Error: template not found (Error ', title, ')')
    else:
        turl = fetch_url

    if verbose: print('status: getting specified Template...' + title)
    if cert == '':
        response = requests.get(turl, verify=False, auth=(username, password))
    else:
        response = requests.get( turl, verify=True, cert=cert, auth=(username, password))
    out = response.json()
    if verbose: pprint(out)

    response_code = response.status_code
    if verbose: print('Code:' + str(response_code) + ' - ' + str(requests.status_codes._codes[response_code]))

    if response_code == requests.codes.ok:
        if verbose: print('status: Templates downloaded.')
    else:
        response.raise_for_status()
        raise Exception( '- error: a problem occurred when uploading the schema (Error ', response_code, ')')

    if verbose: print('status: done.')
    return out


def get_data_full( username='', password='', cert='', url='', id=''):
    """
    get_data_full: get data file info including it template's info

    Parameters:     username        - username on CDCS instance   (Note:  User must have admin privileges)
                    password        - password on CDCS instance
                    eurt            - certificate to use for authentication - blank means no security
                    url             - url of CDCS instance
                    id              - id of data file to get info on
    """

    template_upload_url = '/rest/data/get-full'
    turl = url + template_upload_url

    print('status: Getting Data file info.')

    data = {'id': id}
    print('Get:')
    if cert == '':
        response = requests.get( turl, params=data, verify=False, auth=(username, password))
    else:
        response = requests.get( turl, params=data, verify=True, cert=cert, auth=(username, password))
    response_code = response.status_code
    print('Code:' + str(response_code) + ' - ' + str(requests.status_codes._codes[response_code]))
    out = response.json()
    pprint(out)

    if response_code == requests.codes.ok:
        print('- status: downloaded.')
    else:
        response.raise_for_status()
        raise Exception( '- error: a problem occurred when uploading the schema (Error ', response_code, ')')

    print('- status: done.')


def upload_data( username='', password='', cert='', url='', filen='', template_id='', verbose=True):
    """
    upload_data: import data file into a curator using specific template.

    Parameters:     username        - username on CDCS instance   (Note:  User must have admin provledges)
                    password        - password on CDCS instance
                    cert            - certificate to use for authentication - blank means no security
                    url             - url of CDCS instance
                    filen           - data file name to uplaod
                    template_id     - id of template to use
    """

    if verbose: print('status: uploading data file...')
    with open(filen, 'rb') as xml_file:
        xml_content = xml_file.read()

    xml_upload_url = '/rest/data/'
    turl = url + xml_upload_url
    base = os.path.basename(filen)
    if verbose: print('Filename:' + base)
    if verbose: print('Template_id:' + template_id)
    data = {'title': base, 'template': template_id, 'xml_content': xml_content}
    if cert == '':
        response = requests.post( turl, data=data, verify=False, auth=(username, password))
    else:
        response = requests.post( turl, data=data, verify=True, cert=cert, auth=(username, password))
    response_code = response.status_code
    if response_code != requests.codes.created:
        print('Error: Upload failed with status code ' + str(response_code) + ' For:' + base)
        out = response.json()
        pprint(out)
    return response.json()


def upload_blob_file( username='', password='', cert='', url='', filen=''):
    """
    upload_blob_file: import a single blob file into a curator.

       Parameters:     username        - username on CDCS instance   (Note:  User must have admin privileges)
                       password        - password on CDCS instance
                       cert            - certificate to use for authentication - blank means no security
                       url             - url of CDCS instance
                       filen           - name of blob file to load
    """
#
#   Get Global Public Workspace ID
#
    workspace_url = '/rest/workspace/'
    turl = url + workspace_url
    print('status: checking for ID of Global Public Workspace...')
    if cert == '':
        response = requests.get(turl, verify=False, auth=(username, password))
    else:
        response = requests.get( turl, verify=True, cert=cert, auth=( username, password))

    workspace_id = ''
    response_code = response.status_code
    print(response.text)
    response_content = json.loads(response.text)
    for rec in response_content:
        if rec['title'] == "Global Public Workspace":
            workspace_id = rec['id']
    print('Resp: ' + str(response_code))
#
#   If oid is pre-pended to filename remove it  (This is used when a curator is dumped, files get prepened with the ID 
#
    oldid = filen[0:24]
    if all(c in string.hexdigits for c in oldid):
        newfile = filen[25:]
    else:
        newfile = filen

    print('- status: uploading blob files ...')
    xml_upload_url = '/rest/blob/'
    xml_file = open(filen, 'rb')
    xml_content = xml_file.read()
    fd = open(newfile, 'wb')
    fd.write(xml_content)
    xml_file = {'blob': open(newfile, 'rb')}

    turl = url + xml_upload_url
    data = {'filename': newfile}
    print('Post:' +  newfile)
    if cert == '':
        response = requests.post( turl, files=xml_file, data=data, verify=False, auth=( username, password))
    else:
        response = requests.post( turl, files=xml_file, data=data, verify=True, cert=cert, auth=(username, password))
    response_code = response.status_code
    print('Code:' + str(response_code) + ' - ' + str(requests.status_codes._codes[response_code]))
    if response_code == requests.codes.created:
        print('status: uploaded.')
    elif response_code == requests.codes.request_entity_too_large:
        print('Error: Upload File Too Large! Check Webserver file Limit Size.')
    else:
        print('Error: Upload failed with status code: ' + str(response_code) + ' - ' + str(requests.status_codes._codes[response_code]))


def save_blob_to_file( dir='', username='', password='', cert='', url='', bid=''):
    """
    save_blob_to_file: script to get a blob by id from a curator and save it to the original filename it was stored with.

       Parameters:     dir             - directory to store file in
                       username        - username on CDCS instance   (Note:  User must have admin privileges)
                       password        - password on CDCS instance
                       cert            - certificate to use for authentication - blank means no security
                       url             - url of CDCS instance
                       bid             - id of the blod to extract, will create a local file using filename in CDCS of the blob
    """

    print('Get Blob id: ' + str(bid))
    if not os.path.exists(dir):
        os.mkdir(dir)
    print('Bid:' + bid)
    bid = bid.replace('/', '')
    print('Bid:' + bid)
    xml_upload_url = '/rest/blob/' + bid + '/'
    turl = url + xml_upload_url
    if cert == '':
        response = requests.get(turl, verify=False, auth=(username, password), stream=True)
    else:
        response = requests.get(turl, verify=True, cert=cert, auth=(username, password), stream=True)
    response_code = response.status_code
    print('Code:' + str(response_code) + ' - ' + str(requests.status_codes._codes[response_code]))
    xml_upload_url = '/rest/blob/download/' + bid + '/'
    turl = url + xml_upload_url
    if cert == '':
        blobfile = requests.get(turl, verify=False, auth=(username, password), stream=True)
    else:
        blobfile = requests.get(turl, verify=True, cert=cert, auth=(username, password), stream=True)
    out = response.json()
    pprint(out)
    fname = bid + '_' + out['filename']
    print('Save:' + fname)
    with open(dir + fname, 'wb') as fd:
        fd.write(blobfile.content)
    fd.close()
    response_code = blobfile.status_code

    if response_code == requests.codes.ok:
        print('status: uploaded.')
        print('status: blob created: ' + fname)
        ret = bid
    else:
        print('Error: Error getting blob code: ' + str(response_code) + ' - ' + str(requests.status_codes._codes[response_code]))
        ret = 0

    return ret


# get all resources
def get_all_data( username='', password='', cert='', url=''):
    """
    Parameters:      username        - username on CDCS instance   (Note:  User must have admin privledges)
                     password        - password on CDCS instance
                     cert            - certificate to use for authentication - blank means no security
                     url             - url of CDCS instance
                     data_file_title - get data file matching this title
    """

    template_upload_url = '/rest/data'
    turl = url + template_upload_url

    print(f'''- status: Getting Data from {turl}''' )
    if cert == '':
        response = requests.get(turl, verify=False, auth=(username, password))
    else:
        response = requests.get(turl, verify=True, cert=cert, auth=( username, password))

    response_code = response.status_code
    print('Code:' + str(response_code) + ' - ' + str(requests.status_codes._codes[response_code]))
    if response_code == requests.codes.ok:
        out = response.json()
        return out
    else:
        print('Error with status code: ' + str(response_code) + ' - ' + str(requests.status_codes._codes[response_code]))
        return None


def get_data_by_title( username='', password='', cert='', url='', data_file_title='', verbose=False):
    """
    Parameters:      username        - username on CDCS instance   (Note:  User must have admin privledges)
                     password        - password on CDCS instance
                     cert            - certificate to use for authentication - blank means no security
                     url             - url of CDCS instance
                     data_file_title - get data file matching this title
    """

    template_upload_url = '/rest/data'
    turl = url + template_upload_url

    if verbose: print('- status: Getting Data file...' + data_file_title)
    data = {'title': data_file_title}
    #data = {'title': 'Al-Beyeler1968.xml'}
    if verbose: print('Get:')
    if verbose: print(turl)
    pprint(data)
    if cert == '':
        response = requests.get(turl, data, verify=False, auth=(username, password))
    else:
        response = requests.get(turl, data=data, verify=True, cert=cert, auth=( username, password))

    response_code = response.status_code
    if verbose: print('Code:' + str(response_code) + ' - ' + str(requests.status_codes._codes[response_code]))
    if response_code == requests.codes.ok:
        out = response.json()
        pprint(out)
        if verbose: print('- status: downloaded.')
    else:
        print('Error: Upload failed with status code: ' + str(response_code) + ' - ' + str(requests.status_codes._codes[response_code]))
    if verbose: print('- status: done.')

# get data with matching title searching in all data (any owner)
def get_data_by_title_all( username='', password='', cert='', url='', data_file_title='', verbose=False):
    """
    Parameters:      username        - username on CDCS instance   (Note:  User must have admin privledges)
                     password        - password on CDCS instance
                     cert            - certificate to use for authentication - blank means no security
                     url             - url of CDCS instance
                     data_file_title - get data file matching this title
    """
    # search through all data (all owners)
    template_upload_url = 'rest/admin/data'
    turl = url + template_upload_url
    data = {'title': data_file_title}
    if verbose: print(turl)
    if cert == '':
        response = requests.get(turl, params=data, verify=False, auth=(username, password))
    else:
        response = requests.get(turl, params=data, verify=True, cert=cert, auth=( username, password))

    response_code = response.status_code
    if verbose: print('Code:' + str(response_code) + ' - ' + str(requests.status_codes._codes[response_code]))
    if response_code == requests.codes.ok:
        out = response.json()
        if verbose: print('- status: resource found.')
        return out
    else:
        print('- status: resource not found: ' + str(response_code) + ' - ' + str(requests.status_codes._codes[response_code]))
        return None


def del_pid( username='', password='', cert='', url='', provider='local', record='', verbose=False):
    """
    del_blob: script to delete a blob data file from a curator.

    Parameters:     username        - username on CDCS instance   (Note:  User must have admin privileges)
                    password        - password on CDCS instance
                    cert            - certificate to use for authentication - blank means no security
                    url             - url of CDCS instance
                    provider        - name of provider ex: 'local'
                    record          - pid to delete
    """

    pid_delete_url = '/pid/rest/' + provider + '/' + record
    turl = url + pid_delete_url

    if verbose: print('status: Deleteing Blob file...' + record)
    if verbose: print('Delete: ' + turl)
    if cert == '':
        del_response = requests.delete(turl, verify=False, auth=(username, password))
    else:
        del_response = requests.delete(turl, verify=True, cert=cert, auth=(username, password))
    if del_response.status_code == 204:
        if verbose: print('- status: ' + record + ' has been deleted.')
    else:
        print('Error: a problem occurred when deleting the blobs with status code: ' + str(del_response.status_code) + ' - ' + str(requests.status_codes._codes[del_response.status_code]))

    if verbose: print('status: done.')

def del_blob( username='', password='', cert='', url='', bid='', verbose=False):
    """
    del_blob: script to delete a blob data file from a curator.

    Parameters:     username        - username on CDCS instance   (Note:  User must have admin privileges)
                    password        - password on CDCS instance
                    cert            - certificate to use for authentication - blank means no security
                    url             - url of CDCS instance
                    bid             - id of blob to delete
    """

    bid = bid.replace('\/', '')
    blob_delete_url = '/rest/blob/' + bid + '/'
    turl = url + blob_delete_url

    if verbose: print('status: Deleteing Blob file...' + bid)
    if verbose: print('Delete: ' + turl)
    if cert == '':
        del_response = requests.delete(turl, verify=False, auth=(username, password))
    else:
        del_response = requests.delete(turl, verify=True, cert=cert, auth=(username, password))
    if del_response.status_code == 204:
        if verbose: print('- status: ' + bid + ' has been deleted.')
    else:
        print('Error: a problem occurred when deleting the blobs with status code: ' + str(del_response.status_code) + ' - ' + str(requests.status_codes._codes[del_response.status_code]))

    if verbose: print('status: done.')


def delete_data( username='', password='', cert='', url='', did='', verbose=False):
    """
    delete_data: script to delete a data file from a curator.

    Parameters:     username        - username on CDCS instance   (Note:  User must have admin privileges)
                    password        - password on CDCS instance
                    cert            - certificate to use for authentication - blank means no security
                    url             - url of CDCS instance
                    did             - id of data file to delete
    """

    data_delete_url = '/rest/data/' + did + '/'
    turl = url + data_delete_url

    if verbose: print('status: Deleteing Data file...' + did)
    if verbose: print('Delete: ' + turl)
    if cert == '':
        del_response = requests.delete(turl, verify=False, auth=(username, password))
    else:
        del_response = requests.delete(turl, verify=True, cert=cert, auth=(username, password))

    if del_response.status_code == 204:
        if verbose: print('- status: ' + did + ' has been deleted.')
    else:
        print('Error: a problem occurred when deleting the data file with status code: ' + str(del_response.status_code) + ' - ' + str(requests.status_codes._codes[del_response.status_code]))

    if verbose: print('status: done.')


def dump_curator( username='', password='', url='', cert=''):
    """
       dump_curator: get all templates and data files and associated blobs from a 2.0 curator and dump to the local files system

       Parameters:     username        - username on CDCS instance   (Note:  User must have admin priveledges)
                       password        - password on CDCS instance
                       url             - url of CDCS instance
                       cert            - certificate to use for authentication - blank means no security


       creates a directory structure as so:

<Template Title>
    <schema file.xsd>
        <data files>                    <blob files>
        <data_file1.xml>                  <blob_file1>
        <data_file2.xml>                  <blob_file2>
        <data_file3.xml>                  <blob_file3>
        <data_file4.xml>                  <blob_file4>
        <data_file5.xml>                        .
                 .                              .
                 .                              .
                 .                              .
       <data_fileN.xml>                   <blob_fileX>

   This strucure is created by this script . It will pre-pend the blobfile with it's id used in the data file to preserve relationship.

   It will also create a script called "loadata"  that will load the data back into the curator usign the load_curator function in this library.

    """

    template_url = '/rest/template-version-manager/global/'
    turl = url + template_url


    if cert == '':
        print('status: getting Templates (No Cert)...' + turl)
        print(turl)
        print(username, password)
        response = requests.get(turl, verify=False, auth=(username, password))
    else:
        print('status: getting Templates (Cert)...' + turl)
        response = requests.get(turl, verify=True, cert=cert, auth=(username, password))

    print(response)
    response_code = response.status_code

    if response_code == requests.codes.ok:
        out = json.loads(response.text)
        print(out)
    else:
        print('Error: Get Template Global failed with status code: ' + str(response_code) + ' - ' + str(requests.status_codes._codes[response_code]))
        response.raise_for_status()
        raise Exception( '- error: a problem occurred when uploading the schema (Error ', response_code, ')')

    return_code = subprocess.call('rm -rf ./schemas', shell=True)
    return_code = subprocess.call('mkdir ./schemas', shell=True)
    script = open('./loadata', 'w+')
    list1 = re.compile(r'https:\/\/127.0.0.1\/rest\/blob\/download\/(.*?)\<')

    fcount=0;
    for rec in out:
        ver = rec['versions']
        title = rec['title']
        current = rec['current']
        print('Working on;' + title + ' Current: ' + current)
        counter = 0
        for templ in ver:
            counter = counter + 1
            title = title.replace(' ', '-')
            return_code = subprocess.call('mkdir ./schemas/' + title + str(counter), shell=True)
            pprint(templ)
            template_url = '/rest/template/' + templ + '/'
            turl = url + template_url
            pprint(turl)
            if cert == '':
                print('status: getting Templates (No Cert)...' + turl)
                print(turl)
                response1 = requests.get(turl, verify=False, auth=(username, password))
            else:
                response1 = requests.get(turl, verify=True, cert=cert, auth=(username, password))
            print(response1.status_code)
            out1 = json.loads(response1.text)
            print(out1)
            if templ == current:
                fn = 'Cur_' + str(out1['filename'])
            else:
                fn = out1['filename']
            fff = open('./schemas/' + title + str(counter) + '/' + fn, 'w')
            fff.write(out1['content'])
            fff.close()
            script.write( 'python3 load_curator.py ' + username + ' ' + password + ' ' + url + ' schemas/' + title + str(counter) + '  ' + fn + ' ' + title + ' ./schemas/' + title + str(counter) + '/files\n')
            template_upload_url = '/explore/common/rest/local-query'
            #template_upload_url = '/rest/data/query/'
            turl = url + template_upload_url
            print( 'status: Getting Data files associated with template..' + title + ':' + templ)

            data = {
                'query': '{}',
                'all': 'true',
                'templates': '[{"id": "' + templ + '"}]'}

            return_code = subprocess.call('mkdir ./schemas/' + title + str(counter) + '/files', shell=True)

            if cert == '':
                response2 = requests.post( turl, data, verify=False, auth=(username, password))
            else:
                response2 = requests.post( turl, data, verify=True, cert=cert, auth=(username, password))

            response_code = response2.status_code
            print('Code: ',response_code)
            print(turl)
            pprint(response2)

            more = 0
            fcount=0;
            if response_code == requests.codes.ok:
                response_content = response2.json()
                for dataf in response_content:
                    pprint(dataf)
                    if response_content['next'] != 'None':
                        more = 1
                for dataf in response_content['results']:
                    fcount = fcount + 1;
                    print('next:' + str(response_content['next']))
                    print('-------------------------- = ' + dataf['title'])
                    dataf['title'] = dataf['title'].replace('/', '\\')
                    filename = './schemas/' + title + str(counter) + '/files/' + dataf['title']
                    re.sub(r'[^{re.escape(string.printable)}]', '', filename)
                    if not os.path.exists(filename):
                        fff = open( './schemas/' + title + str(counter) + '/files/' + dataf['title'], 'w+')
                    else:
                        fff = open( './schemas/' + title + str(counter) + '/files/' + dataf['title'] + '_' + str(fcount), 'w+')
                    a = dataf['xml_content']
                    a = a.replace(url, 'https://127.0.0.1')
                    fff.write(a)
                    fff.close()
                    result = list1.findall(a)
                    pprint(result)
                    for bid in result:
                        if bid:
                            blobid = save_blob_to_file( './schemas/' + title + str(counter) + '/blobs/', username, password, cert, url, bid,)
                            blobid = 1
                            if blobid != 0:
                                print('save: ' + str(blobid))
                            else:
                                print( 'Error could not open: ' + str(blobid) + '!')

                if more == 1:
                    while str(response_content['next']) != 'None':
                        response2 = requests.get( response_content['next'], data=data, verify=False, auth=( username, password))
                        response_code = response2.status_code

                        if response_code == requests.codes.ok:
                            response_content = response2.json()
                            for dataf in response_content['results']:
                                fcount = fcount + 1;
                                print( '--------------------------' + dataf['title'])
                                dataf['title'] = dataf['title'].replace('/', '\\')
                                filename = './schemas/' + title + str(counter) + '/files/' + dataf['title']
                                if not os.path.exists(filename):
                                    re.sub(r'[^{re.escape(string.printable)}]', '', filename)
                                    fff = open( filename, 'w+')
                                else:
                                    fff = open( filename + '_' + str(fcount), 'w+')
                                a = dataf['xml_content']
                                a = a.replace(url, 'https://127.0.0.1')
                                fff.write(a)
                                fff.close()
                                result = list1.findall(a)
                                for bid in result:
                                    if bid:
                                        blobid = save_blob_to_file( './schemas/' + title + str(counter) + '/blobs/', username, password, cert, url, bid,)
                                        if blobid != 0:
                                            print('save: ' + blobid)
                                        else:
                                            print( 'Error could not open: ' + bid + '!')
                        else:
                            print('Error: Download of ' + filename + ' (' + templ + ') failed status code: ' + str(response_code) + ' - ' + str(requests.status_codes._codes[response_code]))
                            response2.raise_for_status()
                            raise Exception( '- error: a problem occurred when uploading the schema (Error ', response_code, ')')
                    print('Next: ' + str(response_content['next']))
                    print('Previous: ' + str(response_content['previous']))
                    script.write(' #  ' + title + ' - ' + str(counter) + '  ' + str(fcount) + ' Files\n')

    response_code = response.status_code

    script.close()
    if response_code == requests.codes.ok:
        print('- status: ' + str(fcount) + '  Templates/files/blobs have been downloaded.')
    else:
        response.raise_for_status()
        raise Exception( 'error: a problem occurred when downloadong the schema (Error ', response_code, ')')

    print('status: done.')


def save_blob( dir='', username='', password='', cert='', url='', bid=''):
    """
Parameters:     username        - username on CDCS instance   (Note:  User must have admin privileges)
                password        - password on CDCS instance
                cert            - certificate to use for authentication - blank means no security
                url             - url of CDCS instance
                bid             - id of blob to save, fetch and write to file
    """

    print('id: ' + str(bid))
    if not os.path.exists(dir):
        os.mkdir(dir)
    bid = bid.replace('\/', '')
    xml_upload_url = '/rest/blob/' + bid + '/'
    print(xml_upload_url)
    print(url)
    turl = url + xml_upload_url
    print(turl)

    # if cert == '':
    # response = requests.get(turl, verify=False, auth=(username, password), stream=True)
    # else:
    # response = requests.get(turl, verify=True, cert=cert, auth=(username, password), stream=True)
    # out = response.json()

    # pprint(out)

    xml_upload_url = '/rest/blob/download/' + bid + '/'
    turl = url + xml_upload_url

    # if cert == '':
    # blobfile = requests.get(turl, verify=False, auth=(username, password), stream=True)
    # else:
    # blobfile = requests.get(turl, verify=True, cert=cert, auth=(username, password), stream=True)
    # response_code = blobfile.status_code

    print(turl)
    print('Out')
    print(dir)
    print(bid)
    fname = bid + '_'
    print(fname)
    with open(dir + fname, 'wb') as fd:
        fd.write(turl)
    fd.close()
    response_code = requests.codes.ok

    if response_code == requests.codes.ok:
        print('status: blob created: ' + fname)
        ret = bid
    else:
        print('status: Error getting blob: ' + response_code)
        ret = 0

    return ret


def load_curator( username='', password='', url='', schema_path='', schema_filename='', schema_title='', xml_dir='', cert=''):
    """
load_curator: import a template and all data adn blob files into curator.

notes:   reads a directory structure as so:    (As created by dump_curator)

<Template Title>
    <schema file.xsd>
        <data files>                    <blob files>
        <data_file1.xml>                  <blob_file1>
        <data_file2.xml>                  <blob_file2>
        <data_file3.xml>                  <blob_file3>
        <data_file4.xml>                  <blob_file4>
        <data_file5.xml>                        .
                 .                              .
                 .                              .
                 .                              .
       <data_fileN.xml>                   <blob_fileX>

This strucure is created by dump_curator routine in this document. It will pre-pend the blobfile with its id used in the data file.

       Parameters:     username        - username on CDCS instance   (Note:  User must have admin privileges)
                       password        - password on CDCS instance
                       url             - url of CDCS instance
                       schema_path     - Directory path to XSD schema file
                       schema_filename - name of XSD schema file
                       schema_title    - title to use for the Template in CDCS whne uploading XSD schema file
                       xml_dir         - Directory path to XML Data files
                       cert            - certificate to use for authentication - blank means no security
    """
#
#   Get Global Public Workspace ID
#
    workspace_url = '/rest/workspace/'
    turl = url + workspace_url
    print('status: checking for ID of Global Public Workspace...')
    if cert == '':
        response = requests.get(turl, verify=False, auth=(username, password))
    else:
        response = requests.get( turl, verify=True, cert=cert, auth=( username, password))

    workspace_id = ''
    response_code = response.status_code
    print(response_code)
    print(response.text)
    response_content = json.loads(response.text)
    for rec in response_content:
        if rec['title'] == "Global Public Workspace":
            workspace_id = rec['id']
    print('Resp: ' + str(response_code))
#
#   First - see if template title already exists,  add to it if it does, add newif it does not
#

    template_upload_url = '/rest/template-version-manager/global/'
    turl = url + template_upload_url
    print('status: checking for template to use when uploading xml files ...')
    if cert == '':
        response = requests.get(turl, verify=False, auth=(username, password))
    else:
        response = requests.get( turl, verify=True, cert=cert, auth=( username, password))
    print(response)
    response_content = json.loads(response.text)
    print('Get:')
    print(turl)
    response_code = response.status_code
    print('Resp: ' + str(response_code))

#
# This will be default if we do not find it
#

    old_template_id = ''
    template_upload_url = '/rest/template/global/'
    patch_url = ''
    template_id = ''
    for rec in response_content:
        print(rec)
        if schema_title == rec['title']:

            #
            #   Found it, use this instead
            #

            template_id = rec['id']
            old_template_id = rec['current']
            print('Found id=' + str(template_id))
            template_upload_url = '/rest/template-version-manager/' + template_id + '/version/'

    if schema_filename != '':
        print('Load with Schemafile = ' + schema_filename)
        # When downloading, current schema is pre-pended with Cur_
        schema = join(schema_path, schema_filename)
        if schema_filename[0:4] == 'Cur_':
            is_current = 1
            schema_filename = schema_filename[4:]
        else:
            is_current = 0

        print( 'Schema Filename = ' + schema_filename + ' Iscurrent=' + str(is_current))


#   If oid is pre-pended to filename remove it
#
#
        oldid = schema_filename[0:24]
        if all(c in string.hexdigits for c in oldid):
            newfile = schema_filename[25:]
        else:
            newfile = schema_filename
        newfile = schema_filename

        with codecs.open(schema, 'rb', encoding='utf-8') as template_file:
            template_content = template_file.read()
        data = {
            'title': schema_title,
            'filename': newfile,
            'content': template_content}
        print('Load Template')
        turl = url + template_upload_url
        if cert == '':
            response = requests.post( turl, json=data, verify=False, auth=( username, password))
        else:
            response = requests.post( turl, json=data, verify=True, cert=cert, auth=( username, password))
        print('Post: ' + turl)
        response_code = response.status_code
        print('Resp: ' + str(response.status_code))
        #print(response)
        response_content = json.loads(response.text)
        if response_code == requests.codes.created:
            template_id = str(response_content['id'])
            print( 'status: Template has been uploaded with template_id = ' + str(template_id))
            if is_current == 1:
                patch_url = url + '/rest/template/version/' + template_id + '/current/'
                print('patch: ' + patch_url)
                if cert == '':
                    patch_response = requests.patch( patch_url, verify=False, auth=( username, password))
                else:
                    patch_response = requests.patch( patch_url, verify=True, cert=cert, auth=( username, password))
                print('Response: ' + patch_response.text)
        else:
            print('Error: Upload of ' + newfile + ' failed status code: ' + str(response_code) + ' - ' + str(requests.status_codes._codes[response_code]))
            raise Exception( '- error: a problem occurred when uploading the schema (Error ' + str(response_code) + ')')
    else:
        print('Load with Title = ' + schema_title)
        template_id = old_template_id
        template_content = ''

    # upload the directory full of XML files using:
    # the XML schema      : schema/<title>.xsd
    # the set of XML files: schema/<title>/files/<xml filenames>*.xml
    #  look in the data files for blobs that need loading

    print('Status: uploading xml files ...')
    xml_upload_url = '/rest/data/'
    for xml_filename in listdir(xml_dir):
        with codecs.open(join(xml_dir, xml_filename), mode='r', encoding='utf-8') as xml_file:
            print('file: ' + xml_filename)
            xml_content = xml_file.read()
            turl = url + xml_upload_url
            oldid = xml_filename[0:24]
            if all(c in string.hexdigits for c in oldid):
                newfile = xml_filename[25:]
            else:
                newfile = xml_filename
            newfile = xml_filename

            list1 = re.compile(r'https:\/\/127.0.0.1\/rest\/blob\/download\/(.*?)\<')
            result = list1.findall(xml_content)
            xml_content = xml_content.replace('https://127.0.0.1', url)
            print('Result')
            print(result)
            for bid in result:
                if bid:
                    print('List1:' + bid + '   file:' + xml_filename)
                    blobid = load_blob( username, password, cert, url, schema_path, bid)
                    if blobid != 0:
                        xml_content = xml_content.replace( str(bid), str(blobid))
                        print('replace - ' + bid + ' -' + blobid)
                    else:
                        print('Error could not open: ' + bid + '!')

            list1 = re.compile(r'\\u0[0-9A-Fa-f][0-9A-Fa-f][0-9A-Fa-f]')
            result = list1.findall(xml_content)
            print('Unicode Characters:')
            print(result)
            for bid in result:
                if bid:
                    new=bid
                    new = new.replace('\\u0','&#x')
                    new = new + ';'
                    xml_content = xml_content.replace( str(bid), str(new))
                    print('replace - ' + bid + ' -' + new)

            print(turl)
            print(xml_filename)
            print(template_id)
            print('New file=' + newfile)
            newfile = newfile.replace( '_', ' ')
            data = {
                'title': newfile,
                'template': template_id,
                'xml_content': xml_content}
            
            print('Post:')
            pprint(data)
            if cert == '':
                response_str = requests.post( turl, data, verify=False, auth=( username, password))
            else:
                response_str = requests.post( turl, data, verify=True, cert=cert, auth=( username, password))
            response_code = response_str.status_code
            if response_code == requests.codes.created:
                print('Resp XML: ')
                response_content = json.loads(response_str.text)
                data_id = str(response_content['id'])
                patch_url = url + '/rest/data/' + data_id + '/assign/' + workspace_id
                print('patch: ' + patch_url)
                if cert == '':
                    patch_response = requests.patch( patch_url, verify=False, auth=( username, password))
                else:
                    patch_response = requests.patch( patch_url, verify=True, cert=cert, auth=( username, password))
                print('Response: ' + patch_response.text)
                print('status: ' + xml_filename + ' has been uploaded.')
            else:
                response_content = json.loads(response_str.text)
                pprint(response_content)
                print('Error: Upload of ' + xml_filename + ' failed status code: ' + str(response_code) + ' - ' + str(requests.status_codes._codes[response_code]))
    print('status: done.')


def load_blob(username='', password='', cert='', url='', dir='', bid=''):
    """
    load_blob: load a blob from directory wiht "bid" in filename (from download, ID preserves link to data)

       Parameters:     username        - username on CDCS instance   (Note:  User must have admin privileges)
                       password        - password on CDCS instance
                       cert            - certificate to use for authentication - blank means no security
                       url             - url of CDCS instance
                       dir             - Directory path to blob file
                       bid             - id of blob file to load
    """

    bid = bid.replace('/', '')
    print('id: ' + str(bid))
    print(dir + '/blobs/' + bid + '*')
    blob_file = glob(dir + '/blobs/' + bid + '*')
    print('Blobfile: ' + bid)
    pprint(blob_file)
    bfile = blob_file[0]
    print('Blobfile: ' + bfile)
    newfile = bfile
    newfile = newfile.replace(dir + '/blobs/' + bid + '_', '')
    print('New: ' + str(newfile))
    xml_test_url = '/rest/blob/' + bid + '/'
    blob_exists = url + xml_test_url
    print('Check Blob:' + blob_exists)
    if cert == '':
        response = requests.get( blob_exists, verify=False, auth=( username, password), stream=True)
    else:
        response = requests.get( blob_exists, verify=True, cert=cert, auth=( username, password), stream=True)
    with open('/tmp/blob', 'wb') as fd:
        fd.write(response.content)
    print('Get:')
    response_code = response.status_code
    print('Resp: ' + str(response.status_code))
    ret = bid

    if response_code == requests.codes.ok:
        out = response.json()
        print(out)
        print("status: blob exists don't upload.")
    else:
#
#   Get Global Public Workspace ID
#
        workspace_url = '/rest/workspace/'
        turl = url + workspace_url
        print('status: checking for ID of Global Public Workspace...')
        if cert == '':
            response = requests.get(turl, verify=False, auth=(username, password))
        else:
            response = requests.get( turl, verify=True, cert=cert, auth=( username, password))

        workspace_id = ''
        response_code = response.status_code
        print(response.text)
        response_content = json.loads(response.text)
        for rec in response_content:
            if rec['title'] == "Global Public Workspace":
                workspace_id = rec['id']
        print('Resp: ' + str(response_code))
        print('Open blob')
        print(str(bfile))
        xml_file = open(str(bfile), 'rb')
        xml_content = xml_file.read()
        xml_file.close()
        print('Open New')
        fd = open(newfile, 'wb')
        fd.write(xml_content)
        fd.close()
        xml_file = {'blob': open(newfile, 'rb')}
        xml_upload_url = '/rest/blob/'
        turl = url + xml_upload_url
        print(turl)
        data = {'filename': newfile}
        print('Filename:' + newfile)
        print('Post:')
        if cert == '':
            response = requests.post( turl, files=xml_file, data=data, verify=False, auth=( username, password))
        else:
            response = requests.post( turl, files=xml_file, data=data, verify=True, cert=cert, auth=( username, password))
        response_code = response.status_code
        print(response_code)
        print('Resp: ')
        pprint(response)
        if (response_code == 413):
            print("Error uploading, you exceeded the max upload file size!")
        else:
            print(response)
            print('json:')
            out = response.json()
            print(out)
        if response_code == requests.codes.created:
            ret = out['id']
            patch_url = url + '/rest/blob/' + ret + '/assign/' + workspace_id
            print('patch: ' + patch_url)
            if cert == '':
              patch_response = requests.patch( patch_url, verify=False, auth=( username, password))
            else:
              patch_response = requests.patch( patch_url, verify=True, cert=cert, auth=( username, password))
            print('Response: ' + patch_response.text)
            print('status: ' + newfile + ' has been uploaded.')
            print('Remove: ' + newfile)
            os.remove(newfile);
        else:
            print('Remove: ' + newfile)
            os.remove(newfile);
            print('Error: Upload of ' + newfile + ' failed status code: ' + str(response_code) + ' - ' + str(requests.status_codes._codes[response_code]))
            print('Error: Blob Upload failed with status code ')
            print(response_code)
            print(response)
            #print('xml_content:')
            #print(xml_file)
            ret = 0

    print('Return: ' + str(ret))
    return ret


def get_types_data(username='', pwd='', cert='', url=''):
    """
       Parameters:     username        - username on CDCS instance   (Note:  User must have admin provledges)
                       password        - password on CDCS instance
                       cert            - certificate to use for authentication - blank means no security
                       url             - url of CDCS instance
    """
    types20_url = "/rest/types20/select/all"
    turl = url + types20_url

    # get the types20 using REST
    print('- status: getting types20...')
    print("Get:")
    if cert == '':
        response = requests.get(turl, verify=False, auth=(username, pwd))
    else:
        response = requests.get(turl, verify=True, cert=cert, auth=(username, pwd))
    out = response.json()
    # response.json()
    with open('types20.json', 'wb') as fd:
        for chunk in response.iter_lines( chunk_size=512, decode_unicode=None, delimiter=None):
            fd.write(chunk)
    response_code = response.status_code
    print("Resp: ")
    print(response.status_code)

    if response_code == requests.codes.ok:
        print("- status: types20.json has been downloaded.")
    else:
        response.raise_for_status()
        raise Exception( "- error: a problem occurred when gettign the types20 (Error ", str(response_code) + ' - ' + str(requests.status_codes._codes[response_code]), ")")

    print('- status: done.')


def delete_all(username='', pwd='', url='', cert='', template=''):

    template_url = '/rest/template-version-manager/global/'
    turl = url + template_url

    blobid = delete_all_blobs(username, pwd, cert, url)
    if blobid == requests.codes.ok:
        blobid = del_all_xslts(username, pwd, url)
        if blobid == requests.codes.ok:
            blobid = del_all_types(username, pwd, url)

    print('status: getting Templates...' + turl)

    response = requests.get(turl, verify=False, auth=(username, pwd))
    response_code = response.status_code
    print('Code:' + str(response_code) + ' - ' + str(requests.status_codes._codes[response_code]))
    pprint(response)
    out = json.loads(response.text)

    for rec in out:
        ver = rec['versions']
        title = rec['title']
        current = rec['current']
        print('Working on;' + title + ' Current: ' + current)
        counter = 0
        for templ in ver:
            counter = counter + 1
            template_url = '/rest/template/' + templ + '/'
            turl = url + template_url
            response1 = requests.get(turl, verify=False, auth=(username, pwd))
            print(response1.status_code)
            out1 = json.loads(response1.text)
            template_upload_url = '/rest/data/query/'
            turl = url + template_upload_url
            print( 'status: Getting Data files associated with template..' + title + ':' + templ)
            data = {
                'query': '{}',
                'all': 'true',
                'templates': '[{"id": "' + templ + '"}]'}
            response2 = requests.post( turl, data, verify=False, auth=( username, pwd))
            dout = response2.json()

            for dataf in dout:
                print('--------------------------' + dataf['title'])
                delete_data(username, pwd, cert, url, dataf['id'])

    response_code = response.status_code

    if response_code == requests.codes.ok:
        print('- status: Templates/files/blobs have been deleted.')
    else:
        response.raise_for_status()
        raise Exception( "Error: a problem occurred when downloading the schem (Error ", str(response_code) + ' - ' + str(requests.status_codes._codes[response_code]), ")")

    print('status: done.')


def delete_all_blobs( username='', password='', cert='', url=''):
    """

    delete_all_blobs:  delete all blobs in a curator

    Parameters:     username        - username on CDCS instance   (Note:  User must have admin privileges)
                    password        - password on CDCS instance
                    cert            - certificate to use for authentication - blank means no security
                    url             - url of CDCS instance
    """

    blob_upload_url = '/rest/admin/blob/'
    turl = url + blob_upload_url

    print('status: Getting Blob files:', turl)
    if cert == '':
        response = requests.get(turl, verify=False, auth=(username, password))
    else:
        response = requests.get( turl, verify=True, cert=cert, auth=( username, password))

    pprint(response)
    for item in response.json():
        print(item['id'])
        blob_upload_url = '/rest/blob/' + item['id'] + '/'
        turl = url + blob_upload_url
        if cert == '':
            del_response = requests.delete( turl, verify=False, auth=( username, password))
        else:
            del_response = requests.delete( turl, verify=True, cert=cert, auth=( username, password))
        if del_response.status_code == 204:
            print('- status: ' + item['id'] + 'has been deleted.')
        else:
            del_response.raise_for_status()
            print(' error deleting: ' + item['id'])
            raise Exception( '- error: a problem occurred when deleting the blobs (Error ', del_response.status_code, ')')

    response_code = response.status_code
    print('Resp: ')
    print(response.status_code)

    if response_code == requests.codes.ok:
        print('- status: All blobs have been deleted.')
    else:
        response.raise_for_status()
        raise Exception( '- error: a problem occurred when deletng the blobs (Error ', response_code, ')')

    print('- status: done.')

def delete_all_registry(username='', pwd='', url='', cert='',):

    template_url = '/rest/template-version-manager/global'
    turl = url + template_url

    print('status: getting Templates...' + turl)

    response = requests.get(turl, verify=False, auth=(username, pwd))
    response_code = response.status_code
    print('Code:' + str(response_code) + ' - ' + str(requests.status_codes._codes[response_code]))
    pprint(response)
    out = json.loads(response.text)

    for rec in out:
        ver = rec['versions']
        title = rec['title']
        current = rec['current']
        print('Working on;' + title + ' Current: ' + current)
        counter = 0
        for templ in ver:
            counter = counter + 1
            template_url = '/rest/template/' + templ + '/'
            turl = url + template_url
            response1 = requests.get(turl, verify=False, auth=(username, pwd))
            print(response1.status_code)
            out1 = json.loads(response1.text)
            template_upload_url = '/rest/data/query/'
            turl = url + template_upload_url
            print( 'status: Getting Data files associated with template..' + title + ':' + templ)
            data = {
                'query': '{}',
                'all': 'true',
                'templates': '[{"id": "' + templ + '"}]'}
            response2 = requests.post( turl, data, verify=False, auth=( username, pwd))
            dout = response2.json()

            for dataf in dout:
                print('--------------------------' + dataf['title'])
                delete_data(username, pwd, cert, url, dataf['id'])

    response_code = response.status_code

    if response_code == requests.codes.ok:
        print('- status: Templates/files have been deleted.')
    else:
        response.raise_for_status()
        raise Exception( 'error: a problem occurred when downloadong the schema (Error ', response_code, ')')

    print('status: done.')


def del_all_xslts( username='', password='', cert='', url=''):
    """
    del_all_xslts: delete all xslts from a curator.

    Parameters:     username        - username on CDCS instance   (Note:  User must have admin privileges)
                    password        - password on CDCS instance
                    cert            - certificate to use for authentication - blank means no security
                    url             - url of CDCS instance
                    bid             - id of blob to delete
    """

    xml_upload_url = '/rest/xslt/'
    turl = url + xml_upload_url
    if cert == '':
        response = requests.get(turl, verify=False, auth=(username, password))
    else:
        response = requests.get( turl, verify=True, cert=cert, auth=( username, password))
    out = response.json()
    response_code = blobfile.status_code

    print('status: Getting Xslt files...')
    if cert == '':
        response = requests.get(turl, verify=False, auth=(username, password))
    else:
        response = requests.get( turl, verify=True, cert=cert, auth=( username, password))
    for item in response.json():
        blob_upload_url = '/rest/blob/' + item['id'] + '/'
        turl = url + blob_upload_url
        if cert == '':
            del_response = requests.delete( turl, verify=False, auth=( username, password))
        else:
            del_response = requests.delete( turl, verify=True, cert=cert, auth=( username, password))
        if del_response.status_code == 204:
            print('status: ' + item['id'] + 'has been deleted.')
        else:
            del_response.raise_for_status()
            print(' error deleting: ' + item['id'])
            raise Exception( '- error: a problem occurred when deleting the xslt (Error ', del_response.status_code, ')')

    if response_code == requests.codes.ok:
        print('status: xslt deleted: ' + fname)
        ret = requests.codes.ok
    else:
        print('status: Error getting xslts: ' + response_code)
        ret = 0

    return ret


def del_all_types( username='', password='', cert='', url=''):
    """
    del_all_types: delete all types from a curator.

    Parameters:     username        - username on CDCS instance   (Note:  User must have admin privileges)
                    password        - password on CDCS instance
                    cert            - certificate to use for authentication - blank means no security
                    url             - url of CDCS instance
                    bid             - id of blob to delete
    """

    xml_upload_url = '/composer/rest/type-version-manager/global/'
    turl = url + xml_upload_url
    if cert == '':
        response = requests.get(turl, verify=False, auth=(username, password))
    else:
        response = requests.get( turl, verify=True, cert=cert, auth=( username, password))
    out = response.json()
    response_code = blobfile.status_code

    print('status: Getting types files...')
    if cert == '':
        response = requests.get(turl, verify=False, auth=(username, password))
    else:
        response = requests.get( turl, verify=True, cert=cert, auth=( username, password))
    for item in response.json():
        blob_upload_url = '/rest/blob/' + item['id'] + '/'
        turl = url + blob_upload_url
        if cert == '':
            del_response = requests.delete( turl, verify=False, auth=( username, password))
        else:
            del_response = requests.delete( turl, verify=True, cert=cert, auth=( username, password))
        if del_response.status_code == 204:
            print('status: ' + item['id'] + 'has been deleted.')
        else:
            del_response.raise_for_status()
            print(' error deleting: ' + item['id'])
            raise Exception( '- error: a problem occurred when deleting the types (Error ', del_response.status_code, ')')

    if response_code == requests.codes.ok:
        print('status: xslt deleted: ' + fname)
        ret = requests.codes.ok
    else:
        print('status: Error getting xslts: ' + response_code)
        ret = 0

    return ret

def change_owner(username='', pwd='', url='', cert='', new_user=''):

    new_id=''
    for id in range (50):
       get_userid_url = '/rest/user/' + str(id)
       turl = url + get_userid_url
       print("turl:" + turl)
       response = requests.get(turl, verify=False, auth=(username, password))
       response_code = response.status_code
       print(response_code)
       print(response.text)
       print('Code:' + str(response_code) + ' - ' + str(requests.status_codes._codes[response_code]))
       out = json.loads(response.text)
       try:
         myid = out['id']
         user = out['username']
         if (user == new_user):
           new_id=myid
       except KeyError:
           print('')
   
    if (new_id == ''):
       print("No user : " + new_user )
    else:
       print("Id : " + str(new_user) + ":" +str(new_id))
#
# XML Files
#
       template_url = '/rest/admin/data'
       turl = url + template_url
       print('status: getting data...' + turl)

       response = requests.get(turl, verify=False, auth=(username, pwd))
       out = json.loads(response.text)

       response_code = response.status_code
       print('Code:' + str(response_code) + ' - ' + str(requests.status_codes._codes[response_code]))
       if response_code == requests.codes.ok:
         for rec in out:
             print('Response :')
             pprint(rec)
             id = rec['id']
             print('Get id =' + id)
             data_owner_url = '/rest/data/' + str(id) + '/change-owner/' + str(new_id)
             durl = url + data_owner_url
             print('status: Changing Owner...' + new_user)
             print('Change: ' + durl)
             del_response = requests.patch(durl, verify=False, auth=(username, pwd))
             if del_response.status_code == 200:
               print('- status: ' + str(id) + ' has been changed, now owned by ' + new_user)
             else:
               print('Error: a problem occurred when changing the data file with status code: ' + str(del_response.status_code) + ' - ' + str(requests.status_codes._codes[del_response.status_code]))
  
#
# BLOB Files
#
       template_url = '/rest/blob'
       turl = url + template_url
       print('status: getting blobs...' + turl)

       response = requests.get(turl, verify=False, auth=(username, pwd))
       out = json.loads(response.text)

       response_code = response.status_code
       print('Code:' + str(response_code) + ' - ' + str(requests.status_codes._codes[response_code]))
       if response_code == requests.codes.ok:
         for rec in out:
             print('Response :')
             pprint(rec)
             id = rec['id']
             print('Get id =' + id)
             data_owner_url = '/rest/blob/' + str(id) + '/change-owner/' + str(new_id)
             durl = url + data_owner_url
             print('status: Changing Owner...' + new_user)
             print('Change: ' + durl)
             del_response = requests.patch(durl, verify=False, auth=(username, pwd))
             if del_response.status_code == 200:
               print('- status: ' + str(id) + ' has been changed, now owned by ' + new_user)
             else:
               print('Error: a problem occurred when changing the data file with status code: ' + str(del_response.status_code) + ' - ' + str(requests.status_codes._codes[del_response.status_code]))
  
   
       if response_code == requests.codes.ok:
         print('- status: files owners changed.')
       else:
         response.raise_for_status()
         raise Exception( 'error: a problem occurred when changing owner (Error ', response_code, ')')
   
       print('status: done.')


def export_data_by_template_json( username='', password='', cert='', url='', template_file_title=''):
    """
    export_data_by_template: script to export data from a curator by template in JSON format

    Parameters:     username            - username on CDCS instance   (Note:  User must have admin privileges)
                    password            - password on CDCS instance
                    cert                - certificate to use for authentication - blank means no security
                    url                 - url of CDCS instance
                    template_file_title - title of Template in CDCS to get all data files uploaded using it.
    """

    template_url = '/rest/template-version-manager/global'
    turl = url + template_url

    current = ''
    print('status: getting Template... Title:' + template_file_title)
    print('turl: ' + turl)
    if cert == '':
        response = requests.get(turl, verify=False, auth=(username, password))
    else:
        response = requests.get( turl, verify=True, cert=cert, auth=( username, password))
    out = json.loads(response.text)
    for rec in out:
        if rec['title'] == template_file_title:
            current = rec['current']
            print('Found:' + current)

    #query_url = '/explore/common/rest/local-query'
    query_url = '/rest/data/query/'
    turl = url + query_url

    if current == '':
        response.raise_for_status()
        raise Exception( 'Error: No Template named (' + template_file_title + ')')

    id_list = []

    print('status: Query Data using template...')
    data = {'query': '{}', 'all': 'true', 'templates': '[{"id":"' + current + '"}]'}
    print('Post:')
    if cert == '':
        response = requests.post( turl, data=data, verify=False, auth=( username, password))
    else:
        response = requests.post( turl, data=data, verify=True, cert=cert, auth=( username, password))
    out = response.json()
    response_code = response.status_code
    print('Code:' + str(response_code) + ' - ' + str(requests.status_codes._codes[response_code]))
    ids = [did['id'] for did in out]

    print('ID:' + str(ids))

# get JSON Exporter

    exporter_url = '/exporter/rest/exporter/'
    turl = url + exporter_url
    if cert == '':
        response = requests.get(turl, verify=False, auth=(username, password))
    else:
        response = requests.get( turl, verify=True, cert=cert, auth=( username, password))
    out = json.loads(response.text)
    exporter_id = []
    for rec in out:
        if rec['name'] == 'JSON':
            exporter_id.append(rec['id'])
            print('Found JSON exporter:')

    exporter_url = '/exporter/rest/exporter/export/'
    turl = url + exporter_url

    print('status: Exporting Data files using template...')

    data = {'exporter_id_list': exporter_id, 'data_id_list': ids}

    print('Post:')
    if cert == '':
        response = requests.post( turl, json=data, verify=False, auth=( username, password))
    else:
        response = requests.post( turl, json=data, verify=True, cert=cert, auth=( username, password))
    response_code = response.status_code
    print('Code:' + str(response_code) + ' - ' + str(requests.status_codes._codes[response_code]))
    out = response.json()
    #pprint(out)
    if response_code == requests.codes.ok:
        print('status: downloaded.')
    else:
        response.raise_for_status()
        raise Exception( 'Error: a problem occurred when uploading the schema (Error ', response_code, ')')
    print('- status: done.')

    # get zip file

    exporter_url = '/exporter/rest/exporter/export/download/' + out['id'] + '/'
    turl = url + exporter_url
    print(turl)
    if cert == '':
        blobfile = requests.get( turl, verify=False, auth=( username, password), stream=True)
    else:
        blobfile = requests.get( turl, verify=True, cert=cert, auth=( username, password), stream=True)
    response_code = blobfile.status_code
    print('Unziping.')
    return_code = subprocess.call('rm -rf ./JSON_Files', shell=True)
    return_code = subprocess.call('mkdir ./JSON_Files', shell=True)
    zip = zipfile.ZipFile(io.StringIO(blobfile.content))
    zip.extractall('./JSON_Files')

    if response_code == requests.codes.ok:
        print('status: JSON Files created: ')
    else:
        response.raise_for_status()
        raise Exception('Error getting data (Error ', response_code, ')')

def export_data_by_template_csv( username='', password='', cert='', url='', template_file_title=''):
    """
    export_data_by_template: script to export data from a curator by template in CSV format

    Parameters:     username            - username on CDCS instance   (Note:  User must have admin privileges)
                    password            - password on CDCS instance
                    cert                - certificate to use for authentication - blank means no security
                    url                 - url of CDCS instance
                    template_file_title - title of Template in CDCS to get all data files uploaded using it.
    """

    template_url = '/rest/template-version-manager/global'
    turl = url + template_url

    current = ''
    print('status: getting Template... Title:' + template_file_title)
    if cert == '':
        response = requests.get(turl, verify=False, auth=(username, password))
    else:
        response = requests.get( turl, verify=True, cert=cert, auth=( username, password))
    out = json.loads(response.text)
    for rec in out:
        if rec['title'] == template_file_title:
            current = rec['current']
            print('Found:' + current)

    #query_url = '/explore/common/rest/local-query'
    query_url = '/rest/data/query/'
    turl = url + query_url

    if current == '':
        response.raise_for_status()
        raise Exception( 'Error: No Template named (' + template_file_title + ')')

    id_list = []

    print('status: Query Data using template...')
    data = {'query': '{}', 'all': 'true', 'templates': '[{"id":"' + current + '"}]'}
    print('Post:')
    if cert == '':
        response = requests.post( turl, data=data, verify=False, auth=( username, password))
    else:
        response = requests.post( turl, data=data, verify=True, cert=cert, auth=( username, password))
    out = response.json()
    response_code = response.status_code
    print('Code:' + str(response_code) + ' - ' + str(requests.status_codes._codes[response_code]))
    ids = [did['id'] for did in out]

    print('ID:' + str(ids))

# get CSV Exporter

    exporter_url = '/exporter/rest/exporter/'
    turl = url + exporter_url
    if cert == '':
        response = requests.get(turl, verify=False, auth=(username, password))
    else:
        response = requests.get( turl, verify=True, cert=cert, auth=( username, password))
    out = json.loads(response.text)
    exporter_id = []
    for rec in out:
        if rec['name'] == 'CSV_MDTA':
            exporter_id.append(rec['id'])
            print('Found CSV exporter:')

    exporter_url = '/exporter/rest/exporter/export/'
    turl = url + exporter_url

    print('status: Exporting Data files using template...')

    data = {'exporter_id_list': exporter_id, 'data_id_list': ids}

    print('Post:')
    if cert == '':
        response = requests.post( turl, json=data, verify=False, auth=( username, password))
    else:
        response = requests.post( turl, json=data, verify=True, cert=cert, auth=( username, password))
    response_code = response.status_code
    print('Code:' + str(response_code) + ' - ' + str(requests.status_codes._codes[response_code]))
    out = response.json()
    #pprint(out)
    if response_code == requests.codes.ok:
        print('status: downloaded.')
    else:
        response.raise_for_status()
        raise Exception( 'Error: a problem occurred when uploading the schema (Error ', response_code, ')')
    print('- status: done.')

    # get zip file

    exporter_url = '/exporter/rest/exporter/export/download/' + out['id'] + '/'
    turl = url + exporter_url
    print(turl)
    if cert == '':
        blobfile = requests.get( turl, verify=False, auth=( username, password), stream=True)
    else:
        blobfile = requests.get( turl, verify=True, cert=cert, auth=( username, password), stream=True)
    response_code = blobfile.status_code
    print('Unziping.')
    return_code = subprocess.call('rm -rf ./CSV_Files', shell=True)
    return_code = subprocess.call('mkdir ./CSV_Files', shell=True)
    zip = zipfile.ZipFile(io.StringIO(blobfile.content))
    zip.extractall('./CSV_Files')

    if response_code == requests.codes.ok:
        print('status: CSV Files created: ')
    else:
        response.raise_for_status()
        raise Exception('Error getting data (Error ', response_code, ')')


def get_all_xslt(username='', password='', url='', cert=''):
    """
    get_all_xslt: script to get all xslt from a curator to a directoy called xslt

       Parameters:     username        - username on CDCS instance   (Note:  User must have admin privileges)
                       password        - password on CDCS instance
                       url             - url of CDCS instance
                       cert            - certificate to use for authentication - blank means no security
    """

    xslt20_url = '/rest/xslt/'
    turl = url + xslt20_url

    # get the xslt20 using REST

    print('status: getting xslt...')
    if cert == '':
        response = requests.get(turl, verify=False, auth=(username, password))
    else:
        response = requests.get( turl, verify=True, cert=cert, auth=( username, password))
    response_code = response.status_code

    if response_code == requests.codes.ok:
        print('- status: xslt have been downloaded.')
    else:
        response.raise_for_status()
    pprint(response)
    out = json.loads(response.text)
    return_code = subprocess.call('rm -rf ./xslt', shell=True)
    return_code = subprocess.call('mkdir ./xslt', shell=True)
    for rec in out:
        id = rec['id']
        name = rec['name']
        print('Working on;' + name + ' Id: ' + id)
        xslt_url = '/rest/xslt/' + id + '/'
        turl = url + xslt_url
        if cert == '':
            xsltfile = requests.get( turl, verify=False, auth=( username, password), stream=True)
        else:
            xsltfile = requests.get( turl, verify=True, cert=cert, auth=( username, password), stream=True)
        exout = json.loads(xsltfile.text)
        a = exout['content']
        print(a)
        with open('./xslt/' + name + '.xsl', 'wb') as fd:
            fd.write(a.encode('utf8'))
        fd.close()
    response_code = response.status_code

    if response_code == requests.codes.ok:
        print('- status: xslt have been downloaded.')
    else:
        response.raise_for_status()
        raise Exception( '- error: a problem occurred when getting the xslt20 (Error ', response_code, ')')

    print('- status: done.')


def upload_types( username='', password='', cert='', url='', types_dir='',):
    """
    upload_types: upload all types files in <directory> into a curator.

    Parameters:     username        - username on CDCS instance   (Note:  User must have admin privileges)
                    password        - password on CDCS instance
                    cert            - certificate to use for authentication - blank means no security
                    url             - url of CDCS instance
                    types_dir       - Directory path to XML types files
    """

    print('- status: uploading types files ...')
    types_upload_url = '/composer/rest/type/global/'
    for types_filename in listdir(types_dir):
        with open(join(types_dir, types_filename), 'r') as types_file:
            types_content = types_file.read()
            turl = url + types_upload_url
            data = {
                'title': types_filename,
                'filename': types_filename,
                'content': types_content}
            print('Post:' + types_filename)
            #print(data)
            if cert == '':
                response_str = requests.post( turl, data, verify=False, auth=( username, password))
            else:
                response_str = requests.post( turl, data, verify=True, cert=cert, auth=( username, password))
            response_code = response_str.status_code
            response = json.loads(response_str.text)
            if response_code == requests.codes.ok:
                print('- status: uploaded.')
                patch_url = url + '/composer/rest/type/version/' + str(response['id']) + '/current/'
                print('patch:' + patch_url)
                if cert == '':
                    response = requests.patch( patch_url, verify=False, auth=( username, password))
                else:
                    response = requests.patch( patch_url, verify=True, cert=cert, auth=( username, password))
                print(response_code)
            else:
                print( '- error: Upload failed with status code:' + str(response_code))
                pprint(response)


def upload_xslts( username='', password='', cert='', url='', xml_dir=''):
    """
    program: upload_xlsts: upload all xlst files in <directory> into a curator.

    Parameters:     username        - username on CDCS instance   (Note:  User must have admin privileges)
                    password        - password on CDCS instance
                    cert            - certificate to use for authentication - blank means no security
                    url             - url of CDCS instance
                    xml_dir         - Directory path to XSLT Data files
    """

    print('- status: uploading xslt files ...')
    xml_upload_url = '/rest/xslt/'
    for xml_filename in listdir(xml_dir):
        with open(join(xml_dir, xml_filename), 'r') as xml_file:
            print(url)
            print(xml_filename)
            xml_content = xml_file.read()
            turl = url + xml_upload_url
            name = xml_filename.replace('\.xsl', '')
            data = {
                'name': name,
                'filename': xml_filename,
                'instance_name': name,
                'title': name,
                'content': xml_content,
            }
            print('Post:')
            print(turl)
            print('turl:')
            print(username)
            print(password)
            if cert == '':
                response_str = requests.post( turl, data, verify=False, auth=( username, password))
            else:
                response_str = requests.post( turl, data, verify=True, cert=cert, auth=( username, password))
            response_code = response_str.status_code
            print('Resp: ')

            # print response_str.text

            if response_code == requests.codes.created:
                print('- status: uploaded.')
            else:
                print('- error: Upload failed with status code ')
                print(response_code)
                print(':')
                response = json.loads(response_str.text)
                print(response)


def get_template_xslt(username='', password='', url='', cert='', template=''):
    """
    get_template_xslt: script to get all xslts of a template by name

       Parameters:     username        - username on CDCS instance   (Note:  User must have admin privileges)
                       password        - password on CDCS instance
                       url             - url of CDCS instance
                       cert            - certificate to use for authentication - blank means no security
                       template        - template name
    """

# Get ID of the template
    template_upload_url = '/rest/template-version-manager/global/'
    turl = url + template_upload_url
    fetch_url = url + '/rest/template/xsl_rendering'
    print('status: getting template ID...')
    if cert == '':
        response = requests.get(turl, verify=False, auth=(username, password))
    else:
        response = requests.get( turl, verify=True, cert=cert, auth=(username, password))
    print('Get Template ID:')
    response_code = response.status_code
    print('Code:' + str(response_code) + ' - ' + str(requests.status_codes._codes[response_code]))
    response_content = json.loads(response.text)
    for rec in response_content:
        if template == rec['title']:
            cur = rec['current']
            title= rec['title']

    if cur == '':
        response.raise_for_status()
        raise Exception('Error: template not found (Error ', template, ')')
    else:
        print('status: getting xsls...')
    if cert == '':
        response = requests.get(fetch_url, verify=False, auth=(username, password))
    else:
        response = requests.get(fetch_url, verify=True, cert=cert, auth=(username, password))
    response_code = response.status_code
    print('Code:' + str(response_code) + ' - ' + str(requests.status_codes._codes[response_code]))
    out = response.json()
    for rec in out:
        if cur == rec['template']:
            xslt_id = rec['id']
            temp_id = rec['template']
            list_id = rec['list_xslt']
            detail_id = rec['detail_xslt']

    if xslt_id == '':
        print('Could not find xslt')
    else:
        print('Template: ' + title + ' Template ID: ' + temp_id + '  List: ' + list_id + '  Detail : ' + detail_id )

def replace_xslt(username='', password='', url='', cert='', xslt='', xslt_name=''):
    """
    replace_xslt: script to replace an xslt file 

       Parameters:     username        - username on CDCS instance   (Note:  User must have admin privileges)
                       password        - password on CDCS instance
                       url             - url of CDCS instance
                       cert            - certificate to use for authentication - blank means no security
                       xslt            - xslt file
                       xslt_name       - xslt name in CDCS
    """

# Get ID of the xslt
    xslt_url = url + '/rest/xslt/'
    print('status: getting xslt ID...')
    if cert == '':
        response = requests.get(xslt_url, verify=False, auth=(username, password))
    else:
        response = requests.get( xslt_url, verify=True, cert=cert, auth=(username, password))
    print('Get Xslt ID:')
    response_code = response.status_code
    print('Code:' + str(response_code) + ' - ' + str(requests.status_codes._codes[response_code]))
    response_content = json.loads(response.text)
    for rec in response_content:
        if xslt_name == rec['name']:
            cur = rec['id']
            filen = rec['filename']
            fetch_url = url + '/rest/xslt/' + cur + '/'

    xml_file = open(xslt, 'rb')
    xml_content = xml_file.read()
    print(xml_content)
    data = {
        'name': xslt_name,
        'filename': filen,
        'content': xml_content,
    }
    if cur == '':
        response.raise_for_status()
        raise Exception('Error: xslt not found (Error ', xslt_name, ')')
    else:
        print('status: getting xsls...')
    if cert == '':
        response = requests.patch(fetch_url, data, verify=False, auth=(username, password))
    else:
        response = requests.patch(fetch_url, data, verify=True, cert=cert, auth=(username, password))
    response_code = response.status_code
    response_content = json.loads(response.text)
    pprint(response_content)
    print('Code:' + str(response_code) + ' - ' + str(requests.status_codes._codes[response_code]))


def dump_registry( username='', password='', url='', cert=''):
    """
       dump_registry: get all data files from a 2.0 registry and dump to the local files system

       Parameters:     username        - username on CDCS instance   (Note:  User must have admin priveledges)
                       password        - password on CDCS instance
                       url             - url of CDCS instance
                       cert            - certificate to use for authentication - blank means no security


       creates a directory structure as so:

res-md.xsd
    <res-md.xsd>
        <published>                    
           <data_file1.xml>               
           <data_file2.xml>              
           <data_file3.xml>             
           <data_file4.xml>            
           <data_file5.xml>           
                    .                
                    .               
                    .              
          <data_fileN.xml>        
        <uppublished>                    
           <data_file1.xml>               
           <data_file2.xml>              
        <drafts>                    
           <data_file1.xml>               
           <data_file2.xml>              
   
   This strucure is created by this script . It will pre-pend the blobfile with it's id used in the data file to preserve relationship.

   It will also create a script called "loadreg"  that will load the data back into the curator usign the load_curator function in this library.

    """

    template_url = '/rest/template-version-manager/global/'
    turl = url + template_url

    print('status: getting res-md...' + turl)

    if cert == '':
        response = requests.get(turl, verify=False, auth=(username, password))
    else:
        response = requests.get(turl, verify=True, cert=cert, auth=(username, password))

    response_code = response.status_code

    if response_code == requests.codes.ok:
        out = json.loads(response.text)
    else:
        print('Error: Registry Dump failed with status code: ' + str(response_code) + ' - ' + str(requests.status_codes._codes[response_code]))
        response.raise_for_status()
        raise Exception( 'Error: a problem occurred when dumping the registry (Error ', response_code, ')')

    return_code = subprocess.call('rm -rf ./schemas', shell=True)
    return_code = subprocess.call('mkdir ./schemas', shell=True)
    script = open('./loadreg', 'w+')

    for rec in out:
        ver = rec['versions']
        title = rec['title']
        current = rec['current']
        print('Working on;' + title + ' Current: ' + current)
        counter = 0
        for templ in ver:
            counter = counter + 1
            title = title.replace(' ', '-')
            return_code = subprocess.call('mkdir ./schemas/' + title + str(counter), shell=True)
            template_url = '/rest/template/' + templ + '/'
            turl = url + template_url
            if cert == '':
                response1 = requests.get(turl, verify=False, auth=(username, password))
            else:
                response1 = requests.get(turl, verify=True, cert=cert, auth=(username, password))
            out1 = json.loads(response1.text)
            if templ == current:
                fn = 'Cur_' + str(out1['filename'])
            else:
                fn = out1['filename']
            fff = open('./schemas/' + title + str(counter) + '/' + fn, 'w')
            fff.write(out1['content'])
            fff.close()

            script.write( 'python3 load_registry.py ' + username + ' ' + password + ' ' + url + '  \'\'  ' +  '  ' + title + ' ./schemas/' + title + str(counter) + '/active' + '  1\n')
            process_content('active',username, password, url, title, templ, counter)
            script.write( 'python3 load_registry.py ' + username + ' ' + password + ' ' + url + '  \'\'  ' +  '  ' + title + ' ./schemas/' + title + str(counter) + '/inactive' + '  1\n')
            process_content('inactive',username, password, url, title, templ, counter)
            script.write( 'python3 load_registry.py ' + username + ' ' + password + ' ' + url + '  \'\'  ' +  '  ' + title + ' ./schemas/' + title + str(counter) + '/deleted' + '  1\n')
            process_content('deleted',username, password, url, title, templ, counter)
            script.write( 'python3 load_registry.py ' + username + ' ' + password + ' ' + url + '  \'\'  ' +  '  ' + title + ' ./schemas/' + title + str(counter) + '/published' + '  1\n')
            process_content('published',username, password, url, title, templ, counter)
            script.write( 'python3 load_registry.py ' + username + ' ' + password + ' ' + url + '  \'\'  ' +  '  ' + title + ' ./schemas/' + title + str(counter) + '/unpublished' + '  1\n')
            process_content('unpublished',username, password, url, title, templ, counter)
            script.write( 'python3 load_registry.py ' + username + ' ' + password + ' ' + url + '  \'\'  ' +  '  ' + title + ' ./schemas/' + title + str(counter) + '/all' + ' 1\n')
            process_content('all',username, password, url, title, templ, counter)

    response_code = response.status_code
    script.close()

    if response_code == requests.codes.ok:
        print('Status: Templates/files have been downloaded.')
    else:
        print('Code: ' + str(response_code) + ' - ' + str(requests.status_codes._codes[response_code]))
        response.raise_for_status()
        raise Exception( 'Error: a problem occurred when dumping the Registry(Error ', response_code, ')')

    print('status: done.')


def process_content(which='',username='', password='', url='', title='', templ='', counter=''):

     template_upload_url = '/explore/common/rest/local-query'
     #template_upload_url = '/rest/data/query/'
     turl = url + template_upload_url

     cert =''
     if which == 'active':  
        data = { 'query': '{"Resource.@status": "active"}'}
     elif which == 'inactive':  
        data = { 'query': '{"Resource.@status": "inactive"}'}
     elif which == 'deleted':  
        data = { 'query': '{"Resource.@status": "deleted"}'}
     elif which == 'published':  
        data =  { 'query': '{}', 'workspaces':'[{"id": "GLOBAL_WORKSPACE_ID"}]'}
     elif which == 'unpublished':  
        data =  { 'query': '{}', 'workspaces':'[{"id": "None"}]'}
     else: 
        data = { 'query': '{}', 'all': 'true', 'templates': '[{"id": "' + templ + '"}]'}

     return_code = subprocess.call('mkdir ./schemas/' + title + str(counter) + '/' + which, shell=True)

     pprint(turl)
     pprint(data)
     if cert == '':
         response2 = requests.post( turl, data, verify=False, auth=(username, password))
     else:
         response2 = requests.post( turl, data, verify=True, cert=cert, auth=(username, password))

     response_code = response2.status_code

     nfiles=0;
     if response_code == requests.codes.ok:
         response_content = response2.json()
         print ('Count:',  response_content['count'])
         while ((str(response_content['next']) != 'None') or (nfiles < response_content['count'])):
             for dataf in response_content['results']:
                 nfiles = nfiles + 1
                 print( '--------------------------' + dataf['title'],' ---> ', str(nfiles)) 
                 pprint(dataf)
                 print( '--------------------------' + dataf['title'],' ---> ', str(nfiles)) 
                 print( '--------------------------' + dataf['title'],' ---> ', str(nfiles)) 
                 filename = './schemas/' + title + str(counter) + '/' + which + '/' + dataf['title']
                 filename = filename.replace(' ', '-')
                 print(filename)
                 if ( ".xml" in filename) == False:
                     print("Noxml")
                     filename = filename + ".xml"
                 else:
                     print("xml")
                 re.sub(r'[^{re.escape(string.printable)}]', '', filename)
                 print(filename)
                 if not os.path.exists(filename):
                    fff = open( filename, 'w+')
                 else:
                    fff = open( filename + '_' + str(nfiles), 'w+')
                 a = dataf['xml_content']
                 a = a.replace(url, 'https://127.0.0.1')
                 fff.write(a)
                 fff.close()
             if(str(response_content['next']) != 'None'): 
                response2 = requests.get( response_content['next'], data=data, verify=False, auth=( username, password))
                response_code = response2.status_code
                response_content = response2.json()
                if response_code != requests.codes.ok:
                   response2.raise_for_status()
                   raise Exception( '- error: a problem occurred when uploading the schema (Error ', response_code, ')')
         print('Processed Files: ', nfiles)

def load_registry( username='', password='', url='', cert='', template='', files_dir='', published = ''):
    """
       load_registry:  load all data files into a 2.0 registry  that were dumped using dump_registry

       Parameters:     username        - username on CDCS instance   (Note:  User must have admin priveledges)
                       password        - password on CDCS instance
                       url             - url of CDCS instance
                       cert            - certificate to use for authentication - blank means no security
                       files_dir       - directory files are in 
                       publishded      -  1 - publish file when loading


       loads a directory structure as so:

res-md.xsd
    <res-md.xsd>
        <published>                    
           <data_file1.xml>               
           <data_file2.xml>              
           <data_file3.xml>             
           <data_file4.xml>            
           <data_file5.xml>           
                    .                
                    .               
                    .              
          <data_fileN.xml>        
        <uppublished>                    
           <data_file1.xml>               
           <data_file2.xml>              
        <drafts>                    
           <data_file1.xml>               
           <data_file2.xml>              
   
   This strucure is created by this script . It will pre-pend the blobfile with it's id used in the data file to preserve relationship.

   It will also create a script called "loadreg"  that will load the data back into the curator usign the load_curator function in this library.

    """

    # list all templates via rest adn get id for res-md.xsd
    registry_url = "/rest/template-version-manager/global"
    turl = url + registry_url 

    schema_name= template

    data={"title" : schema_name}

    if cert == '':
        response = requests.get(turl, verify=False, auth=(username, password))
    else:
        response = requests.get(turl, verify=True, cert=cert, auth=(username, password))
    
    response_code = response.status_code
    print('Code:' + str(response_code) + ' - ' + str(requests.status_codes._codes[response_code]))
    template_id = ''
    title = ''
    response = json.loads(response.text)

    # 1. there should (in a default registry) only be a single entry in this table - a single schema, res-md.xsd
    # 2. loop through and get the entry whose title is res-md.xsd.
    # 3. its template-id is its 'current' field.
    templates = response
    print(templates)
    for e in templates:
        title = e['title']
        template_id = e['current']
        if ( title == schema_name ):
            break

    if ( title != schema_name ):
        print("- error: failed with status code " + str(response_code) + ": " + str(response))
        print("- error: could not find template id for [" + schema_name + "]")
        exit()

    # 1. once we successfully get the template-id, we are ready to upload xml files
    # 2. setup the rest call for uploading an xml file - and then loop through all xml files, executing that.

    rest_xml_upload_url = "/rest/data/"
    turl = url + rest_xml_upload_url  

    print('status: uploading xml files ...') 
    for xml_filename in listdir(files_dir):
        print("Loading:" + xml_filename)
        with codecs.open(join(files_dir, xml_filename), mode='r', encoding='utf-8') as xml_file:
            xml_content = xml_file.read()
            xml_content = xml_content.replace('https://127.0.0.1', url)
            xml_content = xml_content.encode('utf8')
            turl = url + rest_xml_upload_url
            data = {
                "title": xml_filename,
                "template": template_id,
                "xml_content": xml_content
            }
            print(turl)
            #pprint(data)
            response_str = requests.post(turl, data=data, verify=False, auth=(username, password))
            response_code = response_str.status_code
            response = json.loads(response_str.text)
            publish_url = ""
            if 'id' in response:
                id=response['id']     
                publish_url = url + '/rest/data/' + id + "/publish/"
            print(publish_url)

            if response_code == requests.codes.created:
               if ( ( publish_url != "") & (published == "1")):
                  response1 = requests.patch(publish_url,  verify=False, auth=(username, password))
                  response_code1 = response1.status_code
                  if response_code1 == requests.codes.ok:
                     print("status: " + xml_filename + " has been uploaded as Published.")
                  else:
                     print('Error: Patch failed with status code: ' + str(response_code1) + ' - ' + str(requests.status_codes._codes[response_code1]))
                     raise Exception("- error: a problem occurred when loading the file (Error ", response_code1, ")")
               else:
                  print("status: " + xml_filename + " has been uploaded as Un-Published.")
                    
            else:
               print('Error: Store file  - ' + xml_filename + ' with status code: ' + str(response_code) + ' - ' + str(requests.status_codes._codes[response_code]))

