# Copyright 2017-present Open Networking Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import base64
import jinja2
import json
from synchronizers.new_base.modelaccessor import *
from synchronizers.new_base.policy import Policy

from xosconfig import Config
from multistructlog import create_logger

log = create_logger(Config().get('logging'))


class ServiceOneInstancePolicy(Policy):

    def handle_create(self, service_instance):
        log.info("handle_create")
        return self.handle_update(service_instance)

    def handle_update(self, service_instance):
        compute_service = KubernetesService.objects.first()
        compute_service_instance_class = Service.objects.get(id=compute_service.id).get_service_instance_class()

        exampleservice = service_instance.owner.leaf_model

        slice = exampleservice.slices.first()

        image = slice.default_image

        name="serviceone-%s" % service_instance.id
        compute_service_instance = compute_service_instance_class(slice=slice, owner=compute_service, image=image, name=name, no_sync=True)
        compute_service_instance.save()

    def handle_delete(self, service_instance):
        log.info("handle_delete")
        if service_instance.compute_instance:
            log.info("has a compute_instance")
            service_instance.compute_instance.delete()
            service_instance.compute_instance = None
            # TODO: I'm not sure we can save things that are being deleted...
            service_instance.save(update_fields=["compute_instance"])
