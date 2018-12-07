# Copyright 2013 B1 Systems GmbH
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tables
from horizon import tabs
from math import sqrt

from openstack_dashboard import api
from openstack_dashboard.dashboards.admin.hypervisors \
    import tables as project_tables
from openstack_dashboard.dashboards.admin.hypervisors \
    import tabs as project_tabs
from random import randint


class AdminIndexView(tabs.TabbedTableView):
    tab_group_class = project_tabs.HypervisorHostTabs
    template_name = 'admin/hypervisors/index.html'
    page_title = _("All Hypervisors")

    def get_context_data(self, **kwargs):
        context = super(AdminIndexView, self).get_context_data(**kwargs)
        zun_used = {'cpu_used': 0, 'mem_used': 0, 'disk_used': 0,
                    'total_containers': 0}
        try:
            zun_used = api.zun.host_stats(self.request)
        except Exception:
            exceptions.handle(self.request,
                              _('Unable to retrieve container statistics.'))

        try:
            context["stats"] = api.nova.hypervisor_stats(self.request)
            context['stats'].vcpus_used += int(zun_used['cpu_used'])
            context['stats'].memory_mb_used += zun_used['mem_used']
            context['stats'].local_gb_used += zun_used['disk_used']
            context['stats'].running_vms += zun_used['total_containers']
        except Exception:
            exceptions.handle(self.request,
                              _('Unable to retrieve hypervisor statistics.'))
        return context


class AdminDetailView(tables.DataTableView):
    table_class = project_tables.AdminHypervisorInstancesTable
    template_name = 'admin/hypervisors/detail.html'
    page_title = _("NUMA Topology")

    def get_hypervisor_numa_topology(self):
        numa_topology = []
        try:
            id, name = self.kwargs['hypervisor'].split('_', 1)
            result = api.nova.hypervisor_search(self.request,
                                                name)
            for hypervisor in result:
                if str(hypervisor.id) == id:
                    try:
                        numa_topology += hypervisor.numa_topology
                    except AttributeError:
                        pass
        except Exception:
            exceptions.handle(
                self.request,
                _('Unable to retrieve hypervisor instances list.'))
        return numa_topology

    def get_nova_data(self):
        instances = []
        try:
            id, name = self.kwargs['hypervisor'].split('_', 1)
            result = api.nova.hypervisor_search(self.request,
                                                name)
            for hypervisor in result:
                if str(hypervisor.id) == id:
                    try:
                        instances += hypervisor.servers
                    except AttributeError:
                        pass
        except Exception:
            exceptions.handle(
                self.request,
                _('Unable to retrieve hypervisor instances list.'))
        data = []
        for instance in instances:
            d = {'type': 'Nova'}
            for key in instance:
                if key in ['uuid', 'hostname', 'name']:
                    d[str(key)] = str(instance[key])
                elif key == 'numa_topology' and instance[key] is not None:
                    cpu = {}
                    memory = {}
                    for k in instance[key]['cpu']:
                        cpu[str(k)] = sorted(instance[key]['cpu'][k])
                        memory[str(k)] = instance[key]['memory'][k]
                    d[str(key)] = dict(cpu=cpu, memory=memory)
                else:
                    d[str(key)] = instance[key]
            data.append(d)
        return data

    def get_zun_data(self):
        instances = []
        try:
            id, name = self.kwargs['hypervisor'].split('_', 1)
            result = api.zun.host_show(self.request, id=name)
            instances = result.containers
        except Exception:
            exceptions.handle(
                self.request,
                _('Unable to retrieve host container instances list.'))
        data = []
        for instance in instances:
            d = {'type': 'Zun'}
            for key in instance:
                if key in ['uuid', 'hostname', 'name']:
                    d[str(key)] = str(instance[key])
                elif key == 'numa_topology' and instance[key] is not None:
                    cpu = {}
                    memory = {}
                    for k in instance[key]['cpu']:
                        cpu[str(k)] = sorted(instance[key]['cpu'][k])
                        memory[str(k)] = instance[key]['memory'][k]
                    d[str(key)] = dict(cpu=cpu, memory=memory)
                else:
                    d[str(key)] = instance[key]
            data.append(d)
        return data

    def get_data(self):
        instances = self.get_nova_data() + self.get_zun_data()
        # print('DetailView.instances', instances)
        return instances

    def get_col_row(self, num):
        row = 1
        for high in [1] + [2 * x for x in range(1, int(sqrt(num) / 2) + 1)]:
            length = num / high
            if num % high == 0 and length > high:
                row = length
        return {'col': [c for c in range(num / row)],
                'row': [r for r in range(row)]}

    def get_context_data(self, **kwargs):
        context = super(AdminDetailView, self).get_context_data(**kwargs)
        hypervisor_name = self.kwargs['hypervisor'].split('_', 1)[1]
        breadcrumb = [(hypervisor_name, None)]
        context['custom_breadcrumb'] = breadcrumb
        hypervisor_numa_topology = self.get_hypervisor_numa_topology()
        instances = context['hypervisor_instances_table'].data
        numa_topology = {}
        for node_id in [str(nid) for nid in
                        range(len(hypervisor_numa_topology))]:
            numa_topology[node_id] = {'instances': {}, 'memory_data': [],
                                      'memory_name': [], 'memory_hostname': []}
            for node in hypervisor_numa_topology:
                if node_id == str(node['id']):
                    numa_topology[node_id]['cpuset'] = node['cpuset']
                    numa_topology[node_id]['cpu_col_row'] = self.get_col_row(
                        len(node['cpuset']))
                    numa_topology[node_id]['siblings'] = node['siblings']
                    numa_topology[node_id]['memory'] = node['memory']
                    numa_topology[node_id]['memory_free'] = node['memory']
            num = 0
            for instance in instances:
                numa_topology[node_id]['instances'][instance['name']] = 0
                if instance['numa_topology'] is not None:
                    for key in instance['numa_topology']['cpu']:
                        if key == node_id:
                            numa_topology[key]['memory_data'].append(
                                [instance['numa_topology']['memory'][key]])
                            numa_topology[key]['memory_name'].append(
                                instance['name'])
                            numa_topology[key]['memory_hostname'].append(
                                instance['hostname'])
                            numa_topology[key]['memory_free'] -= \
                                instance['numa_topology']['memory'][key]
                            if len(instance['numa_topology']['cpu'][key]) != 0:
                                numa_topology[key]['instances'][
                                    instance['name']] = []
                                for cpu in instance['numa_topology']['cpu'][
                                    key]:
                                    numa_topology[key]['instances'][
                                        instance['name']].append(
                                        [cpu, instance['hostname']])
                num += 1
            numa_topology[node_id]['memory_data'].append(
                [numa_topology[node_id]['memory_free']])
            numa_topology[node_id]['memory_name'].append('Free')
            numa_topology[node_id]['memory_hostname'].append('Free')
        numa_topology['node_ids'] = sorted(numa_topology.keys())
        color_list = [''.join("%1X" % x) for x in range(1, 16)]
        numa_topology['color'] = {'Free': '#E7E7E7'}
        for instance in instances:
            color = ""
            for i in range(6):
                color += color_list[randint(0, 14)]
            numa_topology['color'][instance['name']] = "#" + color
        context['numa_topology'] = numa_topology
        return context
