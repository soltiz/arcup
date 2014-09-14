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

import click

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
    
    #print "outputing to '{}'...".form(prerequisites_output_file.name)
    prerequisites.append({'file':'bob/bill','size':3500,'hash':'abcdef'})
    prerequisites.append({'file':'bob/bill','size':3500,'hash':'abcdef'})
    json.dump(prerequisites,prerequisites_output_file)
    #prerequisites_output_file.write("new\n")
    #print json.JSONEncoder().encode(prerequisites)
    #json.dump(prerequisites,prerequisites_output_file,cls=ComplexEncoder)

    
if __name__ == '__main__':
    cli()   