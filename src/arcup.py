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

def string_matches_one_pattern_of(the_string,patterns_list):
    for pattern in patterns_list:
        if the_string==pattern:
            print "CVF SHOULD IGNORE =>"+the_string
            return True
    return False

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
    return [ 
            {'file':get_internal_zip_path(member), 
             'md5': md5_from_zipped_file(zipfile,member),
             'size': zipfile.getinfo(member).file_size} for member in zipfile.namelist() if not member.endswith("/") ]

@click.group()
def cli():
    pass

@cli.command()
@click.argument('update_archive_filename', type=click.Path(exists=True))
@click.argument('target_directory', type=click.Path(exists=True))
@click.argument('prerequisites_file', type=click.Path(exists=True))
def apply(update_archive_filename,target_directory,prerequisites_file):
    print "apply '{}' update archive to directory '{}'...".format(update_archive_filename,target_directory)

@cli.command()
@click.argument('update_archive_filename', type=click.Path(exists=False))
@click.argument('base_version_archive', type=click.Path(exists=True))
@click.argument('new_version_archive', type=click.Path(exists=True))
@click.argument('prerequisites_output_file', type=click.File('w'))
@click.option('--exclude-patterns-list', 'exclude_list_file', required=False, type=click.File('r'))
def create(update_archive_filename,base_version_archive, new_version_archive,prerequisites_output_file,exclude_list_file):
    if exclude_list_file is None:
        exclude_patterns=[]
    else:
        exclude_patterns=exclude_list_file.readlines()
    print "create incremental archive '{}'...".format(update_archive_filename)
    prerequisites=[]
    files_to_include=[]
    with zipfile.ZipFile(new_version_archive,'r') as newzip:
        print "Computing new files signatures..."
        new_members_info=get_file_infos_from_zip(newzip)
        
        with zipfile.ZipFile(base_version_archive,'r') as oldzip:
            print "Comparing with base files list..."
            old_members=get_zip_files_internalpaths_list(oldzip)
            for new_member_info in [memberinfo for memberinfo in new_members_info]:
                file_name=new_member_info['file']
                if string_matches_one_pattern_of(file_name,exclude_patterns):
                    print "IGNORING > "+file_name
                else:
                    if file_name in old_members:
                        file_changed=False
                        old_full_filename=external_file_path_from_internal_path(oldzip, file_name)
                        old_filesize=oldzip.getinfo(old_full_filename).file_size
                        if new_member_info['size']!=old_filesize:
                            file_changed=True
                        else:
                            old_md5=md5_from_zipped_file(oldzip, old_full_filename)
                            file_changed=(old_md5!=new_member_info['md5'])
                        if file_changed:
                            print "UPDATED > "+file_name
                            files_to_include.append(file_name)
                        else:
                            prerequisites.append({'file':file_name,'size':new_member_info['size'],'hash':new_member_info['md5']})
                    else:
                        print "NEW > "+file_name
                        files_to_include.append(file_name)
        json.dump(prerequisites,prerequisites_output_file)
        print "Building update archive..."
        with zipfile.ZipFile(update_archive_filename,'w') as updatezip:
            for file_name in files_to_include:
                full_filename=external_file_path_from_internal_path(newzip, file_name)
                updatezip.writestr(file_name,newzip.read(full_filename))


    
if __name__ == '__main__':
    cli()   