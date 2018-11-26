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

from openstack_dashboard import api
from openstack_dashboard.dashboards.admin.hypervisors \
    import tables as project_tables
from openstack_dashboard.dashboards.admin.hypervisors \
    import tabs as project_tabs
import commands
import json

hypervisors = {
    "hypervisors": [
        {
            "hypervisor_hostname": "queens.localdomain",
            "id": 2,
            "numa_topology": [
                {
                    "cpu_usage": 16,
                    "cpuset": [
                        0,
                        1,
                        2,
                        3,
                        4,
                        5,
                        6,
                        7,
                        16,
                        17,
                        18,
                        19,
                        20,
                        21,
                        22,
                        23
                    ],
                    "id": 0,
                    "siblings": [
                        [
                            2,
                            18
                        ],
                        [
                            1,
                            17
                        ],
                        [
                            0,
                            16
                        ],
                        [
                            19,
                            3
                        ],
                        [
                            22,
                            6
                        ],
                        [
                            20,
                            4
                        ],
                        [
                            23,
                            7
                        ],
                        [
                            5,
                            21
                        ]
                    ]
                },
                {
                    "cpu_usage": 4,
                    "cpuset": [
                        8,
                        9,
                        10,
                        11,
                        12,
                        13,
                        14,
                        15,
                        24,
                        25,
                        26,
                        27,
                        28,
                        29,
                        30,
                        31
                    ],
                    "id": 1,
                    "siblings": [
                        [
                            8,
                            24
                        ],
                        [
                            30,
                            14
                        ],
                        [
                            31,
                            15
                        ],
                        [
                            27,
                            11
                        ],
                        [
                            10,
                            26
                        ],
                        [
                            28,
                            12
                        ],
                        [
                            9,
                            25
                        ],
                        [
                            13,
                            29
                        ]
                    ]
                }
            ],
            "servers": [
                {
                    "hostname": "ds4g.s",
                    "memory_mb": 4096,
                    "name": "instance-0000007d",
                    "numa_topology": None,
                    "uuid": "88772395-76cc-486e-a51f-d44bfc5a430e",
                    "vcpus": 4
                },
                {
                    "hostname": "ds4g.d",
                    "memory_mb": 4096,
                    "name": "instance-0000007e",
                    "numa_topology": {
                        "cpu": {
                            "0": [
                                18,
                                2,
                                16,
                                0
                            ]
                        },
                        "memory": {
                            "0": 4096
                        }
                    },
                    "uuid": "43addd57-07df-4fe4-96fd-94b7764f1201",
                    "vcpus": 4
                },
                {
                    "hostname": "ds4g.s.1nodes",
                    "memory_mb": 4096,
                    "name": "instance-0000007f",
                    "numa_topology": {
                        "cpu": {
                            "0": []
                        },
                        "memory": {
                            "0": 4096
                        }
                    },
                    "uuid": "12a193b1-be63-46f4-b168-c0bcf358cda0",
                    "vcpus": 4
                },
                {
                    "hostname": "ds4g.d.1nodes",
                    "memory_mb": 4096,
                    "name": "instance-00000080",
                    "numa_topology": {
                        "cpu": {
                            "0": [
                                19,
                                3,
                                22,
                                6
                            ]
                        },
                        "memory": {
                            "0": 4096
                        }
                    },
                    "uuid": "69accac5-fcb9-49ee-918c-def310817963",
                    "vcpus": 4
                },
                {
                    "hostname": "ds4g.s.2nodes",
                    "memory_mb": 4096,
                    "name": "instance-00000081",
                    "numa_topology": {
                        "cpu": {
                            "0": [],
                            "1": []
                        },
                        "memory": {
                            "0": 2048,
                            "1": 2048
                        }
                    },
                    "uuid": "1d49e82b-f56e-4b97-87fe-a4cafc3f5c59",
                    "vcpus": 4
                },
                {
                    "hostname": "ds4g.d.2nodes",
                    "memory_mb": 4096,
                    "name": "instance-00000082",
                    "numa_topology": {
                        "cpu": {
                            "0": [
                                20,
                                17
                            ],
                            "1": [
                                24,
                                8
                            ]
                        },
                        "memory": {
                            "0": 2048,
                            "1": 2048
                        }
                    },
                    "uuid": "7a56d0ac-6890-4951-888f-b1fbcb59b0df",
                    "vcpus": 4
                }
            ],
            "state": "up",
            "status": "enabled"
        }
    ]
}


zun = {
    "architecture": "x86_64",
    "containers": [
        {
            "hostname": "d1",
            "memory_mb": 4096,
            "name": "da6f643d0458",
            "numa_topology": {
                "cpu": {
                    "0": [
                        1,
                        5,
                        21,
                        17
                    ]
                },
                "memory": {
                    "0": 4096
                }
            },
            "uuid": "f80db274-f5c5-4923-b5ca-4f1a27ef9253",
            "vcpus": 4
        },
        {
            "hostname": "s1",
            "memory_mb": 4096,
            "name": "0e45c5dc7d78",
            "numa_topology": None,
            "uuid": "36d07284-8c6b-4a8a-a689-96b6f1e92790",
            "vcpus": 4
        },
        {
            "hostname": "s2",
            "memory_mb": 4096,
            "name": "897e47ef4fd1",
            "numa_topology": None,
            "uuid": "bd21cfe9-8813-41a8-8da0-0c77fd802f2e",
            "vcpus": 4
        },
        {
            "hostname": "d2",
            "memory_mb": 4096,
            "name": "2fb9126a6817",
            "numa_topology": {
                "cpu": {
                    "0": [
                        20,
                        23,
                        4,
                        18
                    ]
                },
                "memory": {
                    "0": 4096
                }
            },
            "uuid": "c7f3afa0-c7aa-48fa-8385-9f0f06dc5ac1",
            "vcpus": 4
        }
    ],
    "cpu_used": 16.0,
    "cpus": 32,
    "disk_quota_supported": False,
    "disk_total": 442,
    "disk_used": 0,
    "hostname": "rocky115",
    "kernel_version": "3.10.0-693.el7.x86_64",
    "labels": {},
    "links": [
        {
            "href": "http://172.16.25.115/v1/hosts/cf34e105-64df-5a8c-858c-455ff24201d2",
            "rel": "self"
        },
        {
            "href": "http://172.16.25.115/hosts/cf34e105-64df-5a8c-858c-455ff24201d2",
            "rel": "bookmark"
        }
    ],
    "mem_total": 128651,
    "mem_used": 16384,
    "os": "CentOS Linux 7 (Core)",
    "os_type": "linux",
    "runtimes": [
        "runc"
    ],
    "total_containers": 4,
    "uuid": "cf34e105-64df-5a8c-858c-455ff24201d2"
}


# class hypervisor_detail:
#     node_number = len(hypervisors['hypervisors'][0]['numa_topology'])
#     node_detail = []
#     for id in hypervisors['hypervisors'][0]['numa_topology']:
#         node_detail.append({hypervisors['hypervisors'][0]['numa_topology']['id']:
#                                 [{'cpuset': hypervisors['hypervisors'][0]['numa_topology'][id['id']]['cpuset']}]})
class cpu_detail:
    instances_number = len(zun['containers'])+len(hypervisors['hypervisors'][0]['servers'])
    instances_name = []
    for nova in hypervisors['hypervisors'][0]['servers']:
        instances_name.append(nova['name'])
    for container in zun['containers']:
        instances_name.append(container['name'])


class AdminIndexView(tabs.TabbedTableView):
    tab_group_class = project_tabs.HypervisorHostTabs
    template_name = 'admin/hypervisors/index.html'
    page_title = _("All Hypervisors")

    def get_context_data(self, **kwargs):
        context = super(AdminIndexView, self).get_context_data(**kwargs)
        try:
            context["stats"] = api.nova.hypervisor_stats(self.request)
        except Exception:
            exceptions.handle(self.request,
                              _('Unable to retrieve hypervisor statistics.'))

        return context


class AdminDetailView(tables.DataTableView):
    table_class = project_tables.AdminHypervisorInstancesTable
    template_name = 'admin/hypervisors/detail.html'
    page_title = _("Servers")

    def get_data(self):
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
        return instances

    def get_context_data(self, **kwargs):
        context = super(AdminDetailView, self).get_context_data(**kwargs)
        hypervisor_name = self.kwargs['hypervisor'].split('_', 1)[1]
        breadcrumb = [(hypervisor_name, None)]
        context['custom_breadcrumb'] = breadcrumb
        # commands.getoutput('source ~/keystonerc_admin;TOKEN=$(openstack token issue -f value -c id)')
        # hypervisors = commands.getoutput('"curl -g -i -X GET http://172.16.25.115:8774/v2.1/os-hypervisors/rocky115/servers -H "Accept: application/json" -H "User-Agent: python-novaclient" -H "X-Auth-Token: $TOKEN""')
        # hypervisors = json.dumps(hypervisors)
        # hypervisors = hypervisors.replace("null", "None")
        # hypervisors = hypervisors.replace("false", "False")
        # hypervisors = json.loads(hypervisors)
        # commands.getoutput('source ~/keystonerc_admin;TOKEN=$(openstack token issue -f value -c id)')
        # zun = commands.getoutput('curl -g -X GET http://172.16.25.115/container/v1/hosts/rocky115 -H "A"OpenStack-API-Version: container 1.23" -H "User-Agent: None" -H "X-Auth-Token: $TOKEN" | python -m simplejson.tool')
        # zun = json.dumps(zun)
        # zun = hypervisors.replace("null", "None")
        # zun = hypervisors.replace("false", "False")
        # zun = json.loads(zun)
        context['hypervisor_name'] = hypervisor_name
        node0_cpu = []
        node1_cpu = []
        memorydetail = []
        test = []
        if hypervisor_name == hypervisors['hypervisors'][0]['hypervisor_hostname']:
            # instances_number = len(zun['containers']) + len(hypervisors['hypervisors'][0]['servers'])
            for nova in hypervisors['hypervisors'][0]['servers']:
                if nova['numa_topology'] != None:
                    memorydetail.append([[nova['memory_mb']], nova['name']])
                    if len(nova['numa_topology']['cpu']) == 1:
                        for cpu in nova['numa_topology']['cpu']['0']:
                            node0_cpu.append([cpu, nova['name']])
                    elif len(nova["numa_topology"]["cpu"]) == 2:
                        for cpu in nova['numa_topology']['cpu']['0']:
                            node0_cpu.append([cpu, nova['name']])
                        for cpu in nova['numa_topology']['cpu']['1']:
                            node1_cpu.append([cpu, nova['name']])
        if hypervisor_name == zun["hostname"]:
            for container in zun['containers']:
                if container['numa_topology'] != None:
                    memorydetail.append([[container['memory_mb']], container['name']])
                    if len(container['numa_topology']['cpu']) == 1:
                        for cpu in container['numa_topology']['cpu']['0']:
                            node0_cpu.append([cpu, container['name']])
                    elif len(container["numa_topology"]["cpu"]) == 2:
                        for cpu in container['numa_topology']['cpu']['0']:
                            node0_cpu.append([cpu, container['name']])
                        for cpu in container['numa_topology']['cpu']['1']:
                            node1_cpu.append([cpu, container['name']])
        # cpu_number = len(hypervisors['hypervisors']['numa_topology'][0]['cpuset']) + len(hypervisors['hypervisors']['numa_topology'][1]['cpuset'])
        # if len(memorydetail) < cpu_number:
        #     for i in range(cpu_number-len(memorydetail)):
        #         memorydetail.append([0, 0])

        context["node0"] = node0_cpu
        if len(node1_cpu) == 0:
            context["ifnode1"] = -1
        context["node1"] = node1_cpu

        result = dict()
        for elem in node0_cpu:
            if elem[1] not in result:
                result[elem[1]] = [elem]
            else:
                result[elem[1]].append(elem)

        content = dict()
        no = 0
        for key in result:
            content["pane" + str(no)] = result[key]
            no += 1

        context = dict()
        for no in range(0, 8):
            key = "pane" + str(no)
            if key in content:
                context[key] = content[key]
            else:
                context[key] = 0

        if len(memorydetail) < 8:
            for num in range(8 - len(memorydetail)):
                memorydetail.append([[0], 'whatever'])

        memorydetail.append([[zun['mem_total'] - zun['mem_used']], 'free'])
        memory_data = []
        memory_name = []
        for memory in memorydetail:
            memory_data.append(memory[0])
            memory_name.append(memory[1])

        context['memory_data'] = memory_data
        context['memory_name'] = memory_name





        # context["pane0"] = [[0, "hello"], [1, "ok"], [2, "ok"], [3, "ok"]]
        # context['abc'] = [[18, 'instance-0000007e'], [2, 'instance-0000007e'], [16, 'instance-0000007e'], [0, 'instance-0000007e'], [19, 'instance-00000080'], [3, 'instance-00000080'], [22, 'instance-00000080'], [6, 'instance-00000080'], [20, 'instance-00000082'], [17, 'instance-00000082'], [1, 'da6f643d0458'], [5, 'da6f643d0458'], [21, 'da6f643d0458'], [17, 'da6f643d0458'], [20, '2fb9126a6817'], [23, '2fb9126a6817'], [4, '2fb9126a6817'], [18, '2fb9126a6817']]
        # context["pane1"] = [0]
        # context["pane2"] = [0]
        # context["pane3"] = [0]
        # context["pane4"] = [0]
        # context["pane5"] = [0]
        # context["pane6"] = [0]
        # context["pane7"] = [0]
        # context["pane16"] = 50
        return context
