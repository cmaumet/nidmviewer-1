'''
viewer.py: part of the nidmviewer package

'''
import os
from nidmviewer.convert import getjson
from nidmviewer.query import get_peaks_and_maps
from nidmviewer.utils import strip_url, get_random_name, get_extension, download_file
from nidmviewer.templates import get_template, add_string, save_template
from nidmviewer.browser import view


"""
generate

will generate a nidmviewer to run locally [not yet developed] or to embed into webserver

nidm_files: one or more nidm files to add to the viewer. Images in the files should be available
      at the specified URL. 
retrieve: If set to False, the images are assumed to be on the same server, and will be 
          served with the given URL. If retrieve is set to True, the images will be retrieved
          first and stored in a temstporary directory. [NOT YET IMPLEMENTED]
base_image: The base image to use for the viewer. Not specifying a base_image will
            yield a black background.
view_in_browser: open a temporary web browser (to run locally). If True, images will be copied
      to a temp folder. If False, image_paths must be relative to web server. File names 
      should be unique. [NOT YET IMPLEMENTED]

"""
def generate(nidm_files,base_image="",retrieve=False,view_in_browser=False,template_choice="index"):

    template = get_template(template_choice)  
        
    # Parse each nidm file, get nifti paths
    peaks,maps = parse_nidm(nidm_files)
    nifti_files = retrieve_nifti(maps,retrieve)

    # We want pandas df in the format of dict/json strings for javascript embed
    for nidm,peak in peaks.iteritems():
        peaks[nidm] = to_dictionary(peak)    

    if view_in_browser==True:
        tmp_nifti_files,copy_list = generate_temp(nifti_files)
        if base_image != "":
            tmp_base_image,base_copy = generate_temp({base_image: {base_image:base_image}})
            copy_list.update(base_copy)
            base_image = base_copy.values()[0]
        template = add_string("[SUB_BRAINMAPS_SUB]",str(tmp_nifti_files),template)
        template = add_string("[SUB_PEAKS_SUB]",str(peaks),template)
        template = add_string("[SUB_BASEIMAGE_SUB]",str(base_image),template)
        view(template,copy_list)

    else:
        # We will embed json/objects in the page to render dynamically
        template = add_string("[SUB_BRAINMAPS_SUB]",str(nifti_files),template)
        template = add_string("[SUB_PEAKS_SUB]",str(peaks),template)
        template = add_string("[SUB_BASEIMAGE_SUB]",str(base_image),template)
        return template


"""
Here we will parse the nidm files (RDF) into a far superior format (json)
It's not pretty, but it's simple to parse a json structure!

"""
def parse_nidm(nidm_files):
    peaks = dict()
    maps = dict()
    for nidm_file in nidm_files:
        nidm_file = os.path.abspath(nidm_file)
        try:
            results = getjson(nidm_file)
            df,brainmaps = get_peaks_and_maps(results)
            peaks[nidm_file] = df
            maps[nidm_file] = brainmaps
        except:
            print "Cannot parse %s, likely bad syntax." %(nidm_file)
    return peaks,maps

"""
Convert a pandas dataframe into the string of a json/dict to 
embed into page

"""
def to_dictionary(df):
    return df.to_dict(orient="records")

"""
Download the image to a temporary folder if the user needs to
retrieve it. Otherwise, return file

"""
def retrieve_nifti(maps,retrieve):
    # Note: retrieve = True has not been tested!
    map_paths = dict()
    for nidm,maplist in maps.iteritems():
        if retrieve:
            single_maps = dict()
            for brainmap_id,brainmap in maplist.iteritems():
                image_ext = get_extension(brainmap)
                temp_path = get_random_name()
                temp_image_path = "%s.%s" %(temp_path,image_ext)
                if download_file(brainmap,temp_image_path):
                    single_maps[strip_url(brainmap_id)] = temp_image_path
        else:
            single_maps = dict()
            for brainmap_id,brainmap in maplist.iteritems():
                single_maps[strip_url(brainmap_id)] = brainmap.encode("utf-8") 
        map_paths[nidm] = single_maps
    return map_paths


def generate_temp(nifti_files):
    # Here we will generate a lookup of temporary files
    new_nifti_files = dict()
    copy_list = dict()
    for nidm_file,maplist in nifti_files.iteritems():
        nidm_directory = os.path.dirname(nidm_file)
        single_maps = dict()
        for brainmap_id,brainmap in maplist.iteritems():
            brainmap_base = os.path.basename(brainmap)
            image_ext = get_extension(brainmap)
            temp_path = get_random_name()
            temp_image_path = "%s.%s" %(temp_path,image_ext)
            single_maps[strip_url(brainmap_id)] = temp_image_path
            copy_list["%s/%s" %(nidm_directory,brainmap_base)] = temp_image_path
        new_nifti_files[nidm_file] = single_maps
    return new_nifti_files,copy_list      


# Now sure if we will need this
def get_bootstrap():
    return ['<script src="https://rawgit.com/vsoch/nidmviewer/master/js/jquery-2.1.4.min.js"></script>','<link rel="stylesheet" type="text/css" href="https://rawgit.com/vsoch/nidmviewer/master/css/bootstrap.min.css">','<script src="https://rawgit.com/vsoch/nidmviewer/master/js/bootstrap.min.js"></script>']