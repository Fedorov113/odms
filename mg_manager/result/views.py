import json
import os

import requests
from rest_framework import status
from rest_framework.response import Response

from rest_framework import generics, mixins, viewsets

from odms import settings
from .serializers import ProfileResultSerializer, ProfileResultFullSerializer
from rest_framework.views import APIView
from django.http import HttpResponse

from .models import GeneralResult, ProfileResult, Mp2Result, get_mg_sample_container, get_mg_sample_container_file
from ..models import MgFile, MgSampleContainer

# from explorer.file_system import metaphlan2 as mp2
# from explorer.file_system.file_system_helpers import get_general_taxa_comp_for_sample


# class Mp2BoxAPIView(APIView):
#     def get(self, request):
#         # Parse query
#         query_params = self.request.query_params
#         containers = query_params.get('containers', None)
#         if containers[-1] == ',':
#             containers = containers[0:-1]
#         containers = containers.split(',')
#
#         samples_loc = {}  # Dictionary of format {sample_name: file_location}
#         for cont in containers:
#             cont_obj = MgSampleContainer.objects.get(pk=cont)
#             mp2_def = Mp2Result.objects.get(mg_container=cont_obj, params='def')
#             samples_loc[mp2_def.report.path.split('/')[-1].replace('.mp2', '')] = mp2_def.report.path
#
#         # Load Data
#         mp2_data = mp2.read_mp2_data(samples_loc, level='o__', org='Bacteria', norm_100=False)
#         mp2box = mp2_data.set_index('sample').T
#         mp2box = mp2box.fillna('none')
#         # Transform to json
#         mp2_box_dict = mp2box.to_dict(orient='index')
#         # mp2_box_json = json.dumps(mp2_box_dict)
#         # mp2_box_json = list(mp2_box_json)
#         final_dict = {'df': 'df', "preproc": 'preproc', 'mp2box': mp2_box_dict}
#         return HttpResponse(json.dumps(mp2_box_dict), content_type='application/json')


# class GeneralTaxaComposition(APIView):
#     def get(self, request):
#         query_params = self.request.query_params
#         containers = query_params.get('containers', None)
#         if containers[-1] == ',':
#             containers = containers[0:-1]
#         containers = containers.split(',')
#
#         res = []
#         for cont in containers:
#             centr_wc = 'datasets/{df}/taxa/{preproc}/centr__def/{sample}/{sample}_krak.tsv'
#             cont_obj = MgSampleContainer.objects.get(pk=cont)
#             centr_loc = centr_wc.format(
#                 df=cont_obj.mg_sample.dataset_hard.df_name,
#                 preproc=cont_obj.preprocessing,
#                 sample=cont_obj.mg_sample.name_on_fs
#             )
#             abs_loc = os.path.join(settings.PIPELINE_DIR, centr_loc)
#             if os.path.isfile(abs_loc):
#                 rr = get_general_taxa_comp_for_sample(abs_loc)
#                 if rr is not None:
#                     res.append(rr)
#             # samples_loc[mp2_def.report.path.split('/')[-1].replace('.mp2', '')] = mp2_def.report.path
#
#         return HttpResponse(json.dumps(res), content_type='application/json')


class ProfileResultList(generics.ListCreateAPIView):  # Detail View
    queryset = ProfileResult.objects.all()
    serializer_class = ProfileResultSerializer


class ProfileResultDetail(generics.RetrieveUpdateDestroyAPIView):  # Detail View
    queryset = ProfileResult.objects.all()
    serializer_class = ProfileResultFullSerializer


class ResultView(APIView):
    """
    Accepts result from processing system and saves it internally
    """
    def post(self, request):
        data = request.data
        gr = GeneralResult(name=data['result'], input_objects=data['input_objects'],
                           raw_res=json.dumps(data['raw_res']))
        gr.save()
        return HttpResponse(json.dumps('At least we are here'), content_type='application/json')


class ResultRequest(APIView):
    """
    Accepts result request from client and sends it to processing system.
    """

    def post(self, request):

        res_request = json.loads(request.body)
        print(res_request)

        input_objects = res_request['input_objects']

        # check that input objects is registered
        if not (input_objects[0] == 'MgSampleFile' or input_objects[0] == 'MgSampleContainer'):
            return Response('Unknown input object', status=status.HTTP_400_BAD_REQUEST)

        if input_objects[0] == 'MgSampleContainer':
            containers = MgSampleContainer.objects.select_related("mg_sample")\
                .select_related("mg_sample__dataset_hard").in_bulk(res_request['input'])

            res_request['input'] = []
            for cont in containers.values():
                res_request['input'].append({
                            'prefix': cont.mg_sample.dataset_hard.fs_prefix,
                            'df': cont.mg_sample.dataset_hard.df_name,
                            'sample': cont.mg_sample.name_on_fs,
                            'preproc': cont.preprocessing
                        })
        print(res_request)

        # # Make request to asshole
        url = settings.ASSHOLE_URL + 'explorer/request_result/'
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        r = requests.post(url, data=json.dumps(res_request), headers=headers)
        print(r)
        return HttpResponse(json.dumps({'start': 'SUCCESS'}), content_type='application/json')