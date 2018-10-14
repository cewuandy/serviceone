import base64
import jinja2
import json
from synchronizers.new_base.modelaccessor import *
from synchronizers.new_base.policy import Policy

from xosconfig import Config
from multistructlog import create_logger

log = create_logger(Config().get('logging'))


class ServiceOneInstancePolicy(Policy):
    model_name = "ServiceOneInstance"

    def handle_create(self, service_instance):
        return self.handle_update(service_instance)

    def handle_update(self, service_instance):
        compute_service = KubernetesService.objects.first()

        serviceone = service_instance.owner.leaf_model

        slice = Slice.objects.filter(name="serviceone")[0]
        image = Image.objects.filter(name="cewuandy/apache2")[0]

        name="serviceone-%s" % service_instance.id
        instance = compute_service_instance_class(slice=slice, owner=compute_service, image=image, name=name, no_sync=True)
        instance.save()

    def handle_delete(self, service_instance):
        log.info("handle_delete")
        log.info("has a compute_instance")
        service_instance.compute_instance.delete()
        service_instance.compute_instance = None
        # TODO: I'm not sure we can save things that are being deleted...
        service_instance.save(update_fields=["compute_instance"])