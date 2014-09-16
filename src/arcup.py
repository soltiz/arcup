#!/usr/local/bin/python2.7
# encoding: utf-8
'''
arcup -- shortdesc

arcup is an archive incremental updater intended to update the content of an archive (zip format)


It defines classes_and_methods

@author:     Cedric VAN FRACHEM

@copyright:  2014 Cedric VAN FRACHEM. All rights reserved.

@license:    BSD

@contact:    c.vanfrachem@free.fr

'''
import json
from os.path import os
import zipfile

import click
import hashlib

def get_internal_zip_path(path):
    # intenal name is the file path  stripped of first segment which is normally the name of the root directory created 
    # on archive extraction
    splitted_path=path.split('/')
    return '/'.join(splitted_path[1:])

def get_zip_files_internalpaths_list(zipfile):
    return [ get_internal_zip_path(member) for member in zipfile.namelist() if not member.endswith("/") ]

def external_file_path_from_internal_path(zipfile,internal_path):
    radical=os.path.split(os.path.splitext(zipfile.filename)[0])[-1]
    # the separator within zip archive is always "/" even when produced on windows...
    return radical+'/'+internal_path

def md5_from_zipped_file(zipfile, filename):   
    hasher = hashlib.md5()
    hasher.update(zipfile.read(filename))
    return hasher.hexdigest()

def get_file_infos_from_zip(zipfile):
    # we return internal file name and md5 for all non-directory files within the zipped file
    
    # the separator within zip archive is always "/" even when produced on windows...
    return [ {'file':get_internal_zip_path(member), 'md5': md5_from_zipped_file(zipfile,member)} for member in zipfile.namelist() if not member.endswith("/") ]

@click.group()
def cli():
    pass

@cli.command()
@click.argument('update_archive_filename', type=click.Path(exists=True))
def apply(update_archive_filename):
    print "apply '{}' update archive...".format(update_archive_filename)

@cli.command()
@click.argument('update_archive_filename', type=click.Path(exists=False))
@click.argument('base_version_archive', type=click.Path(exists=True))
@click.argument('new_version_archive', type=click.Path(exists=True))
@click.argument('prerequisites_output_file', type=click.File('w'))
@click.option('--exclude-list', 'exclude_list_file', required=False, type=click.File('w'))
def create(update_archive_filename,base_version_archive, new_version_archive,prerequisites_output_file,exclude_list_file):
    print "create incremental archive '{}'...".format(update_archive_filename)
    prerequisites=[]
    with zipfile.ZipFile(new_version_archive,'r') as myzip:
        new_members_info=get_file_infos_from_zip(myzip)
        print "CVF INFO  : "+json.dumps(new_members_info)    
        for new_member in [memberinfo['file'] for memberinfo in new_members_info]:
            print "NEW MEMBER : " + new_member
        
    with zipfile.ZipFile(base_version_archive,'r') as myzip:
        old_members=get_zip_files_internalpaths_list(myzip)
        for old_member in old_members:
            print "OLD MEMBER : " + old_member
        for new_member_info in [memberinfo for memberinfo in new_members_info]:
                file_name=new_member_info['file']
                if file_name in old_members:
                    print "OVERRIDE FILE > "+file_name
                    prerequisites.append({'file':file_name,'size':3500,'hash':new_member_info['md5']})

    json.dump(prerequisites,prerequisites_output_file)
    #prerequisites_output_file.write("new\n")
    #print json.JSONEncoder().encode(prerequisites)
    #json.dump(prerequisites,prerequisites_output_file,cls=ComplexEncoder)

    
if __name__ == '__main__':
    cli()   