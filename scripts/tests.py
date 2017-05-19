#--coding: utf-8--
import urllib2
import sys
project_branch=123
go_pipeline_label=321
project_commit=333


project_version = '{branch}-{label}.git{commit}'.format(
            branch = project_branch,
            label = go_pipeline_label,
            commit = project_commit
        )

print project_version